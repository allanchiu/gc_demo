import PureCloudPlatformClientV2
from PureCloudPlatformClientV2.rest import ApiException
import time

# 替换为你的客户端ID和客户端密钥
client_id = '70b17ec8-5475-47fb-b8fe-f8572f4d2b63'
client_secret = 'r9eNTdKJcHCURIMvDTuQ7b1AyIP8vgWTnwl6KqdjrJUT'

# 设置区域为 EUW2（欧洲-西部2）
environment = 'euw2.pure.cloud'

# 创建 API 客户端实例
api_client = PureCloudPlatformClientV2(api_client=PureCloudPlatformClientV2.ApiClient(environment))

# 使用 Client ID 和 Client Secret 设置认证
api_client.configuration.set_client_credentials(client_id, client_secret)

# 获取 Access Token
try:
    response = api_client.oauth.get_client_token()
    access_token = response.access_token
    print("Successfully obtained access token:", access_token)
except ApiException as e:
    print("Error getting access token:", e)
    exit(1)
