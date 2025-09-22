import time
import os
from datetime import datetime
from collections.abc import Generator
from typing import Any, Dict
import time

import oss2
from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage
from dify_plugin.file.file import File

class UploadFileTool(Tool):
    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage]:
        try:
            # 验证工具参数中的认证信息
            self._validate_credentials(tool_parameters)
            
            # 执行文件上传操作
            result = self._upload_file(tool_parameters, tool_parameters)
            
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
            # 获取文件对象、目录和其他参数
            file = parameters.get('file')
            directory = parameters.get('directory')
            directory_mode = parameters.get('directory_mode', 'no_subdirectory')
            filename = parameters.get('filename')
            filename_mode = parameters.get('filename_mode', 'filename')
            
            # 验证必填参数
            if not file:
                raise ValueError("Missing required parameter: file")
            
            if not directory:
                raise ValueError("Missing required parameter: directory")
            
            # 验证认证参数
            required_auth_fields = ['endpoint', 'bucket', 'access_key_id', 'access_key_secret']
            for field in required_auth_fields:
                if field not in parameters or not parameters[field]:
                    raise ValueError(f"Missing required authentication parameter: {field}")
            
            # 生成文件名
            if not filename:
                # 如果用户没有指定文件名，使用上传文件的原始文件名
                if hasattr(file, 'name'):
                    original_filename = file.name
                    _, extension = os.path.splitext(original_filename)
                else:
                    # 如果无法获取原始文件名，使用时间戳作为文件名
                    timestamp = str(int(time.time()))
                    extension = ''
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
            
            # 上传文件 - 统一处理文件对象或文件路径
            try:
                # 处理dify_plugin的File对象
                if isinstance(file, File):
                    # 获取文件内容
                    file_content = file.blob
                    # 上传文件内容
                    bucket.put_object(object_key, file_content)
                # 尝试作为普通文件对象处理
                elif hasattr(file, 'read'):
                    # 重置文件指针到开头
                    if hasattr(file, 'seek'):
                        file.seek(0)
                    # 读取文件内容
                    file_content = file.read()
                    # 上传文件内容
                    bucket.put_object(object_key, file_content)
                else:
                    # 尝试作为文件路径处理
                    if isinstance(file, (str, bytes, os.PathLike)):
                        bucket.put_object_from_file(object_key, file)
                    else:
                        # 如果是File对象但没有read方法，尝试获取其内容
                        raise ValueError(f"Unsupported file type: {type(file)}. Expected file-like object or path.")
            except Exception as e:
                raise ValueError(f"Failed to upload file: {str(e)}")
            
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