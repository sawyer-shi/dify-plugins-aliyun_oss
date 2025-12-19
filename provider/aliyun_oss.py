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

            # 2. 验证directory和filename格式 (保持不变)
            if 'directory' in credentials and credentials['directory']:
                dir_value = credentials['directory']
                if dir_value.startswith((' ', '/', '\\')):
                    raise ToolProviderCredentialValidationError("directory不能以空格、/或\\开头")

            if 'filename' in credentials and credentials['filename']:
                file_value = credentials['filename']
                if file_value.startswith((' ', '/', '\\')):
                    raise ToolProviderCredentialValidationError("filename不能以空格、/或\\开头")

            # 3. 创建认证对象
            # 建议增加对 CName 的支持，防止 endpoint 填写自定义域名时出错，但这里先保持原样
            auth = Auth(credentials['access_key_id'], credentials['access_key_secret'])
            # connect_timeout 设置连接超时
            bucket = Bucket(auth, credentials['endpoint'], credentials['bucket'], connect_timeout=10)

            # 4. 进行远程校验
            # 使用 list_objects(max_keys=1) 替代 get_bucket_info()
            # 即使 bucket 为空，这也会返回一个成功的结果 (200 OK)，且权限要求更符合常规业务
            bucket.list_objects(max_keys=1)

        except OssError as e:
            error_code = e.status
            error_msg = e.message if hasattr(e, 'message') else str(e) # 获取更详细的错误信息
            
            if error_code == 403:
                # 细化错误提示
                raise ToolProviderCredentialValidationError(
                    f"无效的Access Key ID或Secret Access Key。详情: {error_msg}"
                )
            elif error_code == 404:
                raise ToolProviderCredentialValidationError(f"Bucket '{credentials['bucket']}' 不存在或 Endpoint 错误")
            elif error_code == 401:
                raise ToolProviderCredentialValidationError("认证失败: AccessKey ID 或 Secret 错误")
            else:
                raise ToolProviderCredentialValidationError(f"OSS验证失败 [{error_code}]: {error_msg}")
        except Exception as e:
            raise ToolProviderCredentialValidationError(f"凭据验证发生未知错误: {str(e)}")
