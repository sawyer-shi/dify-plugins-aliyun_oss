import os
import re
from urllib.parse import urlparse, unquote
from typing import Any, Dict, Optional, Generator
from dify_plugin.entities.tool import ToolInvokeMessage
import requests

from dify_plugin.interfaces.tool import Tool, ToolProvider
from .utils import get_extension_from_content_type


class GetPublicFileByUrlTool(Tool):
    def _invoke(self, tool_parameters: Dict[str, Any]) -> Generator[ToolInvokeMessage, None, None]:
        try:
            # 获取文件URL
            file_url = tool_parameters.get('file_url')
            
            if not file_url:
                raise ValueError("Missing required parameter: file_url")
            
            # 下载公开文件
            result = self._get_public_file_by_url(file_url)
            
            # 提取文件扩展名
            _, extension = os.path.splitext(result['filename'])
            if not extension:
                # 如果没有扩展名，根据content_type使用utils函数推断
                extension = get_extension_from_content_type(result['content_type'])
            
            # 构建文件元数据，确保包含支持图片显示的所有必要属性
            file_metadata = {
                'filename': result['filename'],
                'content_type': result['content_type'],
                'size': result['file_size'],
                'mime_type': result['content_type'],
                'extension': extension
            }
            
            # 如果是图片类型，添加特定标志以确保在Dify页面正常显示
            if result['content_type'].startswith('image/'):
                file_metadata['is_image'] = True
                file_metadata['display_as_image'] = True
                file_metadata['type'] = 'image'
            
            # 使用create_blob_message返回文件内容
            yield self.create_blob_message(
                result['file_content'],
                file_metadata
            )
            
            # 在text中输出成功消息、文件大小和类型，文件大小以MB为单位
            file_size_mb = result['file_size'] / (1024 * 1024) if result['file_size'] > 0 else 0
            success_message = f"Public file downloaded successfully: {result['filename']}\nFile size: {file_size_mb:.2f} MB\nFile type: {result['content_type']}"
            yield self.create_text_message(success_message)
        except Exception as e:
            # 失败时在text中输出错误信息
            yield self.create_text_message(f"Failed to download public file: {str(e)}")
    
    def _get_public_file_by_url(self, file_url: str) -> dict:
        try:
            if not file_url:
                raise ValueError("File URL cannot be empty")
            
            # 验证URL格式
            parsed_url = urlparse(file_url)
            if not parsed_url.scheme or not parsed_url.netloc:
                raise ValueError("Invalid URL format")
            
            # 设置请求头，模拟浏览器访问
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            
            # 发送HTTP请求获取文件
            response = requests.get(file_url, headers=headers, timeout=30)
            response.raise_for_status()  # 检查HTTP错误
            
            # 获取文件内容
            file_content = response.content
            
            # 获取文件大小
            file_size = len(file_content)
            
            # 获取文件类型，优先从Content-Type头获取
            content_type = response.headers.get('Content-Type', 'application/octet-stream')
            
            # 如果Content-Type包含字符集信息，只保留MIME类型
            if ';' in content_type:
                content_type = content_type.split(';')[0].strip()
            
            # 尝试从URL中获取文件名
            filename = os.path.basename(unquote(parsed_url.path))
            
            # 如果URL中没有文件名，尝试从Content-Disposition头获取
            if not filename:
                content_disposition = response.headers.get('Content-Disposition', '')
                if 'filename=' in content_disposition:
                    filename_match = re.search(r'filename[*]?=["\']?([^"\';\s]+)', content_disposition)
                    if filename_match:
                        filename = filename_match.group(1)
            
            # 如果仍然没有文件名，使用默认名称
            if not filename:
                filename = 'downloaded_file'
                # 根据content_type使用utils函数添加扩展名
                extension = get_extension_from_content_type(content_type)
                filename += extension
            
            # 返回结果字典
            return {
                'file_content': file_content,
                'filename': filename,
                'content_type': content_type,
                'file_size': file_size
            }
        except requests.exceptions.RequestException as e:
            error_message = f"Failed to retrieve file from URL: {str(e)}"
            raise ValueError(error_message)
        except Exception as e:
            error_message = f"Unexpected error while retrieving file: {str(e)}"
            raise ValueError(error_message)