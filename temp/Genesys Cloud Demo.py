import PureCloudPlatformClientV2
from PureCloudPlatformClientV2.rest import ApiException

CLIENT_ID = '70b17ec8-5475-47fb-b8fe-f8572f4d2b63'
CLIENT_SECRET = 'r9eNTdKJcHCURIMvDTuQ7b1AyIP8vgWTnwl6KqdjrJU'
ENVIRONMENT = 'https://api.euw2.pure.cloud' # eg. mypurecloud.com


apiclient = PureCloudPlatformClientV2.api_client.ApiClient()
apiclient.host=ENVIRONMENT
apiclient.get_client_credentials_token(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)

# Create Auth API Instance
authApi = PureCloudPlatformClientV2.AuthorizationApi(apiclient)

# Create Rec API Instance
recordApi = PureCloudPlatformClientV2.RecordingApi(apiclient)
conversation_id = 'b938ff7b-d1d3-4e43-9aaf-f8287c839ed8' # str | Conversation ID
max_wait_ms = 5000 # int | The maximum number of milliseconds to wait for the recording to be ready. Must be a positive value. (optional) (default to 5000)
format_id = 'WAV' # str | The desired media format. Valid values:WAV,WEBM,WAV_ULAW,OGG_VORBIS,OGG_OPUS,MP3,NONE. (optional) (default to 'WEBM')
media_formats = ['WAV'] # list[str] | All acceptable media formats. Overrides formatId. Valid values:WAV,WEBM,WAV_ULAW,OGG_VORBIS,OGG_OPUS,MP3. (optional)

try:
    api_response = recordApi.get_conversation_recordings(conversation_id, max_wait_ms=max_wait_ms, format_id=format_id, media_formats=media_formats)
    print(api_response[0].media_uris['0'].media_uri)

except ApiException as e:
    print("Exception when calling RecordingApi->get_conversation_recordings: %s\n" % e)
