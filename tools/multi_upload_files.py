import time
import os
from datetime import datetime
from collections.abc import Generator
from typing import Any, Dict, List

import oss2
from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage
from dify_plugin.file.file import File
from .utils import get_file_type, get_file_extension

class MultiUploadFilesTool(Tool):
    # 最大支持的文件数量
    MAX_FILES = 10
    
    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage]:
        try:
            # 从runtime credentials获取认证信息
            credentials = {
                'endpoint': self.runtime.credentials.get('endpoint'),
                'bucket': self.runtime.credentials.get('bucket'),
                'access_key_id': self.runtime.credentials.get('access_key_id'),
                'access_key_secret': self.runtime.credentials.get('access_key_secret')
            }
            
            # 验证工具参数中的认证信息
            self._validate_credentials(credentials)
            
            # 执行多文件上传操作
            results = self._upload_files(tool_parameters, credentials)
            
            yield self.create_json_message({
                "status": "success",
                "file_urls": [result["file_url"] for result in results],
                "filenames": [result["filename"] for result in results],
                "object_keys": [result["object_key"] for result in results],
                "message": f"Successfully uploaded {len(results)} files"
            })
            
            # 在text中输出成功信息，包含每个文件的类型、大小（M单位）和访问链接
            files = tool_parameters.get('files', [])
            success_message = f"Successfully uploaded {len(results)} files!\n\n"
            
            for i, (file, result) in enumerate(zip(files, results)):
                file_size = 0
                file_type = 'unknown'
                
                # 尝试获取文件大小
                if isinstance(file, File) and hasattr(file, 'blob'):
                    file_size = len(file.blob)
                elif hasattr(file, 'read'):
                    # 保存当前文件指针位置
                    if hasattr(file, 'tell'):
                        current_pos = file.tell()
                    else:
                        current_pos = None
                    
                    # 读取文件内容获取大小
                    content = file.read()
                    file_size = len(content)
                    
                    # 重置文件指针
                    if hasattr(file, 'seek') and current_pos is not None:
                        file.seek(current_pos)
                elif isinstance(file, (str, bytes, os.PathLike)) and os.path.exists(file):
                    file_size = os.path.getsize(file)
                    
                # 尝试获取文件类型
                file_type = get_file_type(file)
                
                # 转换文件大小为MB
                file_size_mb = file_size / (1024 * 1024) if file_size > 0 else 0
                
                # 添加每个文件的信息
                success_message += f"File {i+1}:\n"
                success_message += f"Filename: {result['filename']}\n"
                success_message += f"File type: {file_type}\n"
                success_message += f"File size: {file_size_mb:.2f} MB\n"
                success_message += f"Access URL: {result['file_url']}\n"
                success_message += f"Object key: {result['object_key']}\n\n"
            
            yield self.create_text_message(success_message)
        except Exception as e:
            # 在text中输出失败信息
            yield self.create_text_message(f"Failed to upload files: {str(e)}")
            # 同时抛出异常以保持原有行为
            raise ValueError(f"Failed to upload files: {str(e)}")
    
    def _validate_credentials(self, credentials: dict[str, Any]) -> None:
        # 验证必填字段是否存在
        required_fields = ['endpoint', 'bucket', 'access_key_id', 'access_key_secret']
        for field in required_fields:
            if field not in credentials or not credentials[field]:
                raise ValueError(f"Missing required credential: {field}")
    
    def _upload_files(self, parameters: dict[str, Any], credentials: dict[str, Any]) -> List[Dict]:
        try:
            # 获取文件数组、目录和其他参数
            files = parameters.get('files', [])
            directory = parameters.get('directory')
            directory_mode = parameters.get('directory_mode', 'no_subdirectory')
            filename_mode = parameters.get('filename_mode', 'filename')
            
            # 验证必填参数
            if not files:
                raise ValueError("Missing required parameter: files")
            
            if not directory:
                raise ValueError("Missing required parameter: directory")
            
            # 验证文件数量限制
            if len(files) > self.MAX_FILES:
                raise ValueError(f"Maximum number of files allowed is {self.MAX_FILES}")
            
            # 对directory进行前后去空格处理
            directory = directory.strip()
            # 验证directory规则：禁止以空格、/或\开头
            if directory.startswith(' ') or directory.startswith('/') or directory.startswith('\\'):
                raise ValueError("Directory cannot start with space, / or \\ ")
            
            # 验证认证参数
            required_auth_fields = ['endpoint', 'bucket', 'access_key_id', 'access_key_secret']
            for field in required_auth_fields:
                if field not in credentials or not credentials[field]:
                    raise ValueError(f"Missing required authentication parameter: {field}")
            
            # 创建OSS客户端
            auth = oss2.Auth(credentials['access_key_id'], credentials['access_key_secret'])
            bucket = oss2.Bucket(auth, credentials['endpoint'], credentials['bucket'])
            
            # 上传每个文件
            results = []
            for i, file in enumerate(files):
                try:
                    # 生成文件名
                    source_file_name = "unknown"
                    
                    # 使用上传文件的原始文件名
                    # 如果有多个文件，添加索引以避免文件名冲突
                    base_name = "upload"
                    if len(files) > 1:
                        base_name = f"{base_name}_{i+1}"
                    
                    extension = ".dat"  # 默认扩展名
                    
                    # 尝试从文件对象获取原始文件名和扩展名 - 加强版
                    # 1. 处理dify_plugin的File对象
                    if hasattr(file, 'name') and file.name:
                        original_filename = file.name
                        source_file_name = original_filename
                        file_base_name, file_extension = os.path.splitext(original_filename)
                        if file_extension:
                            extension = file_extension
                            base_name = file_base_name
                    
                    # 2. 尝试从file.filename获取（常见于某些Web框架）
                    elif hasattr(file, 'filename') and file.filename:
                        original_filename = file.filename
                        source_file_name = original_filename
                        file_base_name, file_extension = os.path.splitext(original_filename)
                        if file_extension:
                            extension = file_extension
                            base_name = file_base_name
                    
                    # 3. 尝试从文件内容类型推断扩展名
                    if hasattr(file, 'content_type') and file.content_type:
                        extension = get_file_extension(file)
                    
                    # 4. 额外的检查：确保扩展名是小写的，并且包含点号
                    if extension and not extension.startswith('.'):
                        extension = '.' + extension
                    extension = extension.lower()
                    
                    # 根据filename_mode处理文件名
                    if filename_mode == 'filename_timestamp':
                        # 使用年月日时分秒毫秒格式的时间戳
                        timestamp = datetime.now().strftime('%Y%m%d%H%M%S%f')[:-3]  # 去掉最后三位得到毫秒
                        current_filename = f"{base_name}_{timestamp}{extension}"
                    else:
                        # 使用原始文件名作为默认文件名
                        current_filename = f"{base_name}{extension}"
                    
                    # 根据目录模式生成完整的文件路径
                    object_key = self._generate_object_key(directory, directory_mode, current_filename)
                    
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
                        raise ValueError(f"Failed to upload file {i+1}: {str(e)}")
                    
                    # 构建文件URL
                    protocol = 'https' if credentials.get('use_https', True) else 'http'
                    file_url = f"{protocol}://{credentials['bucket']}.{credentials['endpoint']}/{object_key}"
                    
                    results.append({
                        "status": "success",
                        "file_url": file_url,
                        "filename": current_filename,
                        "object_key": object_key,
                        "message": "File uploaded successfully",
                        "SourceFileName": source_file_name
                    })
                except Exception as e:
                    # 如果单个文件上传失败，记录错误并继续上传其他文件
                    results.append({
                        "status": "error",
                        "error": str(e),
                        "file_index": i
                    })
            
            # 检查是否有上传失败的文件
            failed_uploads = [r for r in results if r.get("status") == "error"]
            if failed_uploads:
                raise ValueError(f"Failed to upload {len(failed_uploads)} files. First error: {failed_uploads[0]['error']}")
            
            return results
        except Exception as e:
            raise ValueError(f"Failed to upload files: {str(e)}")
    
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