import os
import re
from urllib.parse import urlparse, unquote
from typing import Any, Dict, Optional, Generator
from dify_plugin.entities.tool import ToolInvokeMessage

import oss2
from oss2 import Auth, Bucket

from dify_plugin.interfaces.tool import Tool, ToolProvider
from .utils import get_extension_from_content_type


class GetFilesByUrlsTool(Tool):
    def _invoke(self, tool_parameters: Dict[str, Any]) -> Generator[ToolInvokeMessage, None, None]:
        try:
            # 验证工具参数中的认证信息
            self._validate_credentials()
            
            # 获取文件URLs
            file_urls = tool_parameters.get('file_urls')
            
            if not file_urls:
                raise ValueError("Missing required parameter: file_urls")
            
            # 分割URLs（使用分号分隔）
            urls = [url.strip() for url in file_urls.split(';') if url.strip()]
            
            if not urls:
                raise ValueError("No valid URLs provided")
            
            # 批量下载文件
            downloaded_files = []
            total_size = 0
            
            for url in urls:
                try:
                    result = self._get_file_by_url(url)
                    downloaded_files.append(result)
                    total_size += result['file_size']
                    
                    # 提取文件扩展名
                    _, extension = os.path.splitext(result['filename'])
                    if not extension:
                        # 如果没有扩展名，根据content_type使用utils函数推断
                        extension = get_extension_from_content_type(result['content_type'])
                    
                    # 构建文件元数据
                    file_metadata = {
                        'filename': result['filename'],
                        'content_type': result['content_type'],
                        'size': result['file_size'],
                        'mime_type': result['content_type'],
                        'extension': extension
                    }
                    
                    # 如果是图片类型，添加特定标志
                    if result['content_type'].startswith('image/'):
                        file_metadata['is_image'] = True
                        file_metadata['display_as_image'] = True
                        file_metadata['type'] = 'image'
                    
                    # 返回文件内容
                    yield self.create_blob_message(
                        result['file_content'],
                        file_metadata
                    )
                    
                except Exception as e:
                    # 单个文件下载失败时，记录错误但继续处理其他文件
                    yield self.create_text_message(f"Failed to download file from {url}: {str(e)}")
            
            # 输出批量下载结果摘要
            total_size_mb = total_size / (1024 * 1024) if total_size > 0 else 0
            success_count = len(downloaded_files)
            summary_message = f"Batch download completed:\nSuccessfully downloaded: {success_count} files\nTotal size: {total_size_mb:.2f} MB"
            yield self.create_text_message(summary_message)
            
        except Exception as e:
            yield self.create_text_message(f"Batch download failed: {str(e)}")
    
    def _validate_credentials(self) -> None:
        # 验证必填字段是否存在
        required_fields = ['endpoint', 'bucket', 'access_key_id', 'access_key_secret']
        for field in required_fields:
            if not self.runtime.credentials.get(field):
                raise ValueError(f"Missing required credential: {field}")
    
    def _get_file_by_url(self, file_url: str) -> dict:
        try:
            if not file_url:
                raise ValueError("File URL cannot be empty")
            
            # 获取认证参数
            credentials = {
                'endpoint': self.runtime.credentials.get('endpoint'),
                'bucket': self.runtime.credentials.get('bucket'),
                'access_key_id': self.runtime.credentials.get('access_key_id'),
                'access_key_secret': self.runtime.credentials.get('access_key_secret')
            }
            
            # 解析URL获取bucket、endpoint和object_key
            bucket, endpoint, object_key = self._parse_oss_url(file_url)
            
            # 如果URL中的bucket与凭证中的bucket不一致，使用URL中的bucket
            if bucket and bucket != credentials['bucket']:
                bucket_name = bucket
            else:
                bucket_name = credentials['bucket']
            
            # 创建OSS客户端，处理endpoint协议
            endpoint_url = endpoint if endpoint else credentials['endpoint']
            if not endpoint_url.startswith(('http://', 'https://')):
                endpoint_url = f"http://{endpoint_url}"
            auth = oss2.Auth(credentials['access_key_id'], credentials['access_key_secret'])
            bucket = oss2.Bucket(auth, endpoint_url, bucket_name)
            
            # 获取文件内容
            result = bucket.get_object(object_key)
            file_content = result.read()
            
            # 获取文件大小
            file_size = len(file_content)
            
            # 获取文件类型
            content_type = result.headers.get('Content-Type', 'application/octet-stream')
            
            # 获取文件名
            filename = os.path.basename(object_key)
            
            # 返回结果字典
            return {
                'file_content': file_content,
                'filename': filename,
                'content_type': content_type,
                'file_size': file_size
            }
        except Exception as e:
            error_message = f"Failed to retrieve file: {str(e)}"
            raise ValueError(error_message)
    
    def _parse_oss_url(self, url: str) -> tuple:
        """
        解析OSS URL，支持标准格式和自定义域名格式
        标准格式: https://bucket.endpoint/object_key
        自定义域名格式: https://custom-domain/object_key
        """
        parsed_url = urlparse(url)
        
        # 处理URL编码
        object_key = unquote(parsed_url.path.lstrip('/'))
        
        # 如果是标准OSS URL格式 (bucket.endpoint)
        if parsed_url.hostname and '.' in parsed_url.hostname:
            parts = parsed_url.hostname.split('.', 1)
            if len(parts) == 2:
                bucket_name = parts[0]
                endpoint = parts[1]
                return (bucket_name, endpoint, object_key)
        
        # 对于自定义域名格式，需要额外的endpoint或bucket验证
        # 此处仅返回None作为bucket和endpoint，由调用方处理
        return None, None, object_key