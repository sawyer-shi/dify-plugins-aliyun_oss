import time
import os
from datetime import datetime
from collections.abc import Generator
from typing import Any, Dict

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
            
            # 在text中输出成功信息，包含文件类型、大小（M单位）和访问链接
            file = tool_parameters.get('file')
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
            if hasattr(file, 'name'):
                _, extension = os.path.splitext(file.name)
                if extension:
                    file_type = extension.lower()[1:]  # 移除点号
            
            # 转换文件大小为MB
            file_size_mb = file_size / (1024 * 1024) if file_size > 0 else 0
            
            # 使用单独的字符串格式化 - 英文消息
            success_message = "File uploaded successfully!\n"
            success_message += f"Filename: {result['filename']}\n"
            success_message += f"File type: {file_type}\n"
            success_message += f"File size: {file_size_mb:.2f} MB\n"
            success_message += f"Access URL: {result['file_url']}\n"
            success_message += f"Object key: {result['object_key']}"
            yield self.create_text_message(success_message)
        except Exception as e:
            # 在text中输出失败信息 - 英文消息
            yield self.create_text_message(f"Failed to upload file: {str(e)}")
            # 同时抛出异常以保持原有行为
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
            source_file_name = "unknown"
            if not filename:
                # 如果用户没有指定文件名，使用上传文件的原始文件名
                base_name = "upload"
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
                    content_type = file.content_type
                    # 内容类型到扩展名的映射表
                    content_type_map = {
                        # 图片格式
                        'image/jpeg': '.jpg',
                        'image/png': '.png',
                        'image/gif': '.gif',
                        'image/bmp': '.bmp',
                        'image/webp': '.webp',
                        'image/svg+xml': '.svg',
                        'image/tiff': '.tiff',
                        'image/x-icon': '.ico',
                        'image/heic': '.heic',
                        
                        # 音频格式
                        'audio/mpeg': '.mp3',
                        'audio/wav': '.wav',
                        'audio/ogg': '.ogg',
                        'audio/flac': '.flac',
                        'audio/aac': '.aac',
                        'audio/m4a': '.m4a',
                        'audio/mp4': '.mp4',
                        
                        # 视频格式
                        'video/mp4': '.mp4',
                        'video/mov': '.mov',
                        'video/avi': '.avi',
                        'video/x-msvideo': '.avi',
                        'video/x-ms-wmv': '.wmv',
                        'video/webm': '.webm',
                        'video/mpeg': '.mpg',
                        'video/quicktime': '.mov',
                        'video/x-matroska': '.mkv',
                        
                        # 文档格式
                        'application/pdf': '.pdf',
                        'application/msword': '.doc',
                        'application/vnd.openxmlformats-officedocument.wordprocessingml.document': '.docx',
                        'application/vnd.ms-excel': '.xls',
                        'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet': '.xlsx',
                        'application/vnd.ms-powerpoint': '.ppt',
                        'application/vnd.openxmlformats-officedocument.presentationml.presentation': '.pptx',
                        'application/rtf': '.rtf',
                        'application/vnd.oasis.opendocument.text': '.odt',
                        'application/vnd.oasis.opendocument.spreadsheet': '.ods',
                        'application/vnd.oasis.opendocument.presentation': '.odp',
                        
                        # 文本格式
                        'text/plain': '.txt',
                        'text/csv': '.csv',
                        'application/json': '.json',
                        'application/xml': '.xml',
                        'text/xml': '.xml',
                        'text/html': '.html',
                        'text/css': '.css',
                        'application/javascript': '.js',
                        'text/markdown': '.md',
                        
                        # 压缩格式
                        'application/zip': '.zip',
                        'application/gzip': '.gz',
                        'application/x-rar-compressed': '.rar',
                        'application/x-7z-compressed': '.7z',
                        'application/x-tar': '.tar',
                        'application/x-bzip2': '.bz2',
                        
                        # 可执行文件
                        'application/x-msdownload': '.exe',
                        'application/vnd.android.package-archive': '.apk',
                        'application/java-archive': '.jar',
                        'application/x-shockwave-flash': '.swf',
                        
                        # 代码文件
                        'text/x-python': '.py',
                        'text/x-java-source': '.java',
                        'text/x-c++src': '.cpp',
                        'text/x-csrc': '.c',
                        'text/x-csharp': '.cs',
                        'text/x-ruby': '.rb',
                        'text/x-go': '.go',
                        'text/x-rustsrc': '.rs',
                        'text/x-swift': '.swift',
                        'application/x-php': '.php'
                    }
                    
                    # 直接匹配内容类型
                    if content_type in content_type_map:
                        extension = content_type_map[content_type]
                    else:
                        # 尝试匹配内容类型的前缀（例如 'application/vnd.openxmlformats-officedocument.'）
                        for ct, ext in content_type_map.items():
                            if content_type.startswith(ct):
                                extension = ext
                                break
                
                # 4. 额外的检查：确保扩展名是小写的，并且包含点号
                if extension and not extension.startswith('.'):
                    extension = '.' + extension
                extension = extension.lower()
                
                # 根据filename_mode处理文件名
                if filename_mode == 'filename_timestamp':
                    # 使用年月日时分秒毫秒格式的时间戳
                    timestamp = datetime.now().strftime('%Y%m%d%H%M%S%f')[:-3]  # 去掉最后三位得到毫秒
                    filename = f"{base_name}_{timestamp}{extension}"
                else:
                    # 使用原始文件名作为默认文件名
                    filename = f"{base_name}{extension}"
            else:
                # 如果用户指定了文件名，将其作为源文件名
                source_file_name = filename
                # 获取用户指定文件名的基本名称和扩展名
                base_name, extension = os.path.splitext(filename)
                
                # 如果用户指定的文件名没有扩展名，尝试从原始文件获取扩展名
                if not extension:
                    # 尝试从文件对象获取原始文件的扩展名
                    original_extension = ""  
                    # 1. 处理dify_plugin的File对象
                    if hasattr(file, 'name') and file.name:
                        _, original_extension = os.path.splitext(file.name)
                    # 2. 尝试从file.filename获取
                    elif hasattr(file, 'filename') and file.filename:
                        _, original_extension = os.path.splitext(file.filename)
                    # 3. 如果找到了原始扩展名，使用它
                    if original_extension:
                        extension = original_extension
                    # 4. 确保扩展名是小写的，并且包含点号
                    if extension and not extension.startswith('.'):
                        extension = '.' + extension
                    extension = extension.lower()
                        
                # 根据filename_mode处理文件名
                if filename_mode == 'filename_timestamp':
                    # 使用年月日时分秒毫秒格式的时间戳
                    timestamp = datetime.now().strftime('%Y%m%d%H%M%S%f')[:-3]  # 去掉最后三位得到毫秒
                    filename = f"{base_name}_{timestamp}{extension}" 
                elif extension:
                    # 确保文件名包含扩展名
                    filename = f"{base_name}{extension}"
            
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
                "message": "File uploaded successfully",
                "SourceFileName": source_file_name
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