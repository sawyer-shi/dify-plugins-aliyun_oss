import os
import re
import os
from collections.abc import Generator
from typing import Any, Dict

import oss2
from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage

class GetFileByUrlTool(Tool):
    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage]:
        try:
            # 获取凭证信息
            credentials = self._get_credentials()
            
            # 验证凭证
            self._validate_credentials(credentials)
            
            # 执行文件获取操作
            result = self._get_file_by_url(tool_parameters, credentials)
            
            yield self.create_json_message(result)
        except Exception as e:
            raise ValueError(f"Failed to retrieve file: {str(e)}")
    
    def _validate_credentials(self, credentials: dict[str, Any]) -> None:
        # 验证必填字段是否存在
        required_fields = ['endpoint', 'bucket', 'access_key_id', 'access_key_secret']
        for field in required_fields:
            if field not in credentials or not credentials[field]:
                raise ValueError(f"Missing required credential: {field}")
    
    def _get_file_by_url(self, parameters: dict[str, Any], credentials: dict[str, Any]) -> dict:
        try:
            # 获取文件URL
            file_url = parameters.get('file_url')
            
            if not file_url:
                raise ValueError("Missing required parameter: file_url")
            
            # 解析URL获取bucket、endpoint和object_key
            bucket, endpoint, object_key = self._parse_oss_url(file_url)
            
            # 如果URL中的bucket与凭证中的bucket不一致，使用URL中的bucket
            if bucket and bucket != credentials['bucket']:
                bucket_name = bucket
            else:
                bucket_name = credentials['bucket']
            
            # 创建OSS客户端
            auth = oss2.Auth(credentials['access_key_id'], credentials['access_key_secret'])
            bucket = oss2.Bucket(auth, endpoint, bucket_name)
            
            # 获取文件内容
            result = bucket.get_object(object_key)
            file_content = result.read()
            
            # 获取文件名
            filename = os.path.basename(object_key)
            
            return {
                "status": "success",
                "filename": filename,
                "file_content": file_content.decode('utf-8', errors='ignore'),
                "message": "File retrieved successfully"
            }
        except Exception as e:
            raise ValueError(f"Failed to retrieve file: {str(e)}")
    
    def _parse_oss_url(self, url: str) -> tuple:
        # 匹配OSS URL格式：https://bucket.endpoint/object_key
        pattern = r'https?://([^.]+)\.([^/]+)/(.*)'
        match = re.match(pattern, url)
        
        if match:
            bucket = match.group(1)
            endpoint = match.group(2)
            object_key = match.group(3)
            return bucket, endpoint, object_key
        
        # 如果URL格式不符合预期，抛出异常
        raise ValueError(f"Invalid OSS URL format: {url}")