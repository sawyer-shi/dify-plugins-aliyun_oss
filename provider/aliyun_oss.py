from oss2 import Auth, Bucket
from oss2.exceptions import OssError
from typing import Any, Dict

# 修复导入错误
# ToolProvider 类在 dify_plugin.interfaces.tool 模块中
from dify_plugin.interfaces.tool import ToolProvider
from dify_plugin.errors.tool import ToolProviderCredentialValidationError


class AliyunOssProvider(ToolProvider):
    def _validate_credentials(self, credentials: Dict[str, Any]) -> None:
        try:
            # 1. 检查必要凭据是否存在
            required_fields = ['access_key_id', 'access_key_secret', 'endpoint', 'bucket']
            for field in required_fields:
                if not credentials.get(field):
                    raise ToolProviderCredentialValidationError(f"{field} 不能为空")

            # 2. 验证directory和filename格式
            if 'directory' in credentials and credentials['directory']:
                dir_value = credentials['directory']
                if dir_value.startswith((' ', '/', '\\')):
                    raise ToolProviderCredentialValidationError("directory不能以空格、/或\\开头")

            if 'filename' in credentials and credentials['filename']:
                file_value = credentials['filename']
                if file_value.startswith((' ', '/', '\\')):
                    raise ToolProviderCredentialValidationError("filename不能以空格、/或\\开头")

            # 3. 创建认证对象
            auth = Auth(credentials['access_key_id'], credentials['access_key_secret'])
            bucket = Bucket(auth, credentials['endpoint'], credentials['bucket'])

            # 4. 进行远程校验，设置较短的超时时间以避免在验证阶段长时间阻塞
            timeout = int(credentials.get('timeout', 10) or 10)
            bucket.get_bucket_info()

        except OssError as e:
            error_code = e.status
            if error_code == 403:
                raise ToolProviderCredentialValidationError("无效的Access Key ID或Secret Access Key")
            elif error_code == 404:
                raise ToolProviderCredentialValidationError("Bucket不存在")
            elif error_code == 401:
                raise ToolProviderCredentialValidationError("拒绝访问，请检查凭据权限")
            else:
                raise ToolProviderCredentialValidationError(f"OSS验证失败: {str(e)}")
        except Exception as e:
            raise ToolProviderCredentialValidationError(f"凭据验证发生未知错误: {str(e)}")
