import time
import os
from datetime import datetime
from collections.abc import Generator
from typing import Any, Dict

import oss2
from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage

class UploadFileTool(Tool):
    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage]:
        try:
            # 获取凭证信息
            credentials = self._get_credentials()
            
            # 验证凭证
            self._validate_credentials(credentials)
            
            # 执行文件上传操作
            result = self._upload_file(tool_parameters, credentials)
            
            yield self.create_json_message(result)
        except Exception as e:
            raise ValueError(f"Failed to upload file: {str(e)}")
    
    def _validate_credentials(self, credentials: dict[str, Any]) -> None:
        # 验证必填字段是否存在
        required_fields = ['endpoint', 'bucket', 'access_key_id', 'access_key_secret']
        for field in required_fields:
            if field not in credentials or not credentials[field]:
                raise ValueError(f"Missing required credential: {field}")
    
    def _upload_file(self, parameters: dict[str, Any], credentials: dict[str, Any]) -> dict:
        try:
            # 获取文件路径、目录和其他参数
            file_path = parameters.get('file')
            directory = parameters.get('directory')
            directory_mode = parameters.get('directory_mode', 'no_subdirectory')
            filename = parameters.get('filename')
            filename_mode = parameters.get('filename_mode', 'filename')
            
            # 验证必填参数
            if not file_path:
                raise ValueError("Missing required parameter: file")
            
            if not directory:
                raise ValueError("Missing required parameter: directory")
            
            if not os.path.exists(file_path):
                raise ValueError(f"File not found: {file_path}")
            
            # 生成文件名
            if not filename:
                # 如果用户没有指定文件名，使用时间戳作为文件名
                timestamp = str(int(time.time()))
                # 保留原始文件的扩展名
                _, extension = os.path.splitext(file_path)
                filename = f"{timestamp}{extension}"
            else:
                # 根据filename_mode处理文件名
                if filename_mode == 'filename_timestamp':
                    # 获取原始文件名的基本名称和扩展名
                    base_name, extension = os.path.splitext(filename)
                    timestamp = str(int(time.time()))
                    filename = f"{base_name}_{timestamp}{extension}"
            
            # 根据目录模式生成完整的文件路径
            object_key = self._generate_object_key(directory, directory_mode, filename)
            
            # 创建OSS客户端
            auth = oss2.Auth(credentials['access_key_id'], credentials['access_key_secret'])
            bucket = oss2.Bucket(auth, credentials['endpoint'], credentials['bucket'])
            
            # 上传文件
            bucket.put_object_from_file(object_key, file_path)
            
            # 构建文件URL
            protocol = 'https' if credentials.get('use_https', True) else 'http'
            file_url = f"{protocol}://{credentials['bucket']}.{credentials['endpoint']}/{object_key}"
            
            return {
                "status": "success",
                "file_url": file_url,
                "filename": filename,
                "object_key": object_key,
                "message": "File uploaded successfully"
            }
        except Exception as e:
            raise ValueError(f"Failed to upload file: {str(e)}")
    
    def _generate_object_key(self, directory: str, directory_mode: str, filename: str) -> str:
        """根据目录模式生成完整的对象键"""
        # 确保目录名不以斜杠开头或结尾
        directory = directory.strip('/')
        
        # 基础路径就是一级目录
        base_path = directory
        
        # 根据目录模式添加日期相关的子目录
        if directory_mode == 'yyyy_mm_dd_hierarchy':
            # 年月日层级子目录模式 (一级目录/2025/09/10/目标文件)
            now = datetime.now()
            base_path = os.path.join(directory, str(now.year), f"{now.month:02d}", f"{now.day:02d}")
        elif directory_mode == 'yyyy_mm_dd_combined':
            # 年月日一体子目录模式 (一级目录/20250910/目标文件)
            now = datetime.now()
            base_path = os.path.join(directory, now.strftime('%Y%m%d'))
        # 如果是no_subdirectory模式，则不添加额外的子目录
        
        # 组合完整的对象键
        object_key = os.path.join(base_path, filename)
        
        # 将操作系统路径分隔符替换为OSS使用的斜杠
        return object_key.replace('\\', '/')