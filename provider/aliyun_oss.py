from typing import Any

import oss2
from typing import Any
from dify_plugin import ToolProvider
from dify_plugin.errors.tool import ToolProviderCredentialValidationError


class AliyunOssProvider(ToolProvider):
    def _validate_credentials(self, credentials: dict[str, Any]) -> None:
        try:
            # 验证必填字段是否存在
            required_fields = ['endpoint', 'bucket', 'access_key_id', 'access_key_secret']
            for field in required_fields:
                if field not in credentials or not credentials[field]:
                    raise ToolProviderCredentialValidationError(f"Missing required credential: {field}")
            
            # 使用oss2创建认证对象进行实际验证
            auth = oss2.Auth(credentials['access_key_id'], credentials['access_key_secret'])
            
            bucket = oss2.Bucket(auth, credentials['endpoint'], credentials['bucket'])
            
            # 尝试获取Bucket信息以验证凭证有效性
            bucket.get_bucket_info()
        except oss2.exceptions.OssError as e:
            raise ToolProviderCredentialValidationError(f"OSS validation failed: {str(e)}")
        except Exception as e:
            raise ToolProviderCredentialValidationError(str(e))
