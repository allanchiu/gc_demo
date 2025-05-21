import PureCloudPlatformClientV2
from PureCloudPlatformClientV2.rest import ApiException

CLIENT_ID = "70b17ec8-5475-47fb-b8fe-f8572f4d2b63"
CLIENT_SECRET = "r9eNTdKJcHCURIMvDTuQ7b1AyIP8vgWTnwl6KqdjrJU"
ENVIRONMENT = "https://api.euw2.pure.cloud"  # eg. mypurecloud.com


apiclient = PureCloudPlatformClientV2.api_client.ApiClient()
apiclient.host = ENVIRONMENT
apiclient.get_client_credentials_token(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)

# Create Rec API Instance
recordApi = PureCloudPlatformClientV2.RecordingApi(apiclient)

# Create Conversation API Instance
conversationApi = PureCloudPlatformClientV2.ConversationsApi(apiclient)


body = PureCloudPlatformClientV2.ConversationQuery()
segmentFilter = PureCloudPlatformClientV2.SegmentDetailQueryFilter()

predicte01 = PureCloudPlatformClientV2.SegmentDetailQueryPredicate()
predicte01.type = "dimension"
predicte01.dimension = "direction"
predicte01.operator = "matches"
predicte01.value = "inbound"
segmentFilter.predicates = [predicte01]
segmentFilter.type = "or"
body.segment_filters = [segmentFilter]
body.interval = "2025-04-10T00:00:00.000Z/2025-04-10T23:59:59.999Z"


try:
    api_response = conversationApi.post_analytics_conversations_details_query(body)
    response = api_response.to_dict()
    conversations = response["conversations"]
    total_hits = response["total_hits"]
    for i in range(0, total_hits):
        print(response["conversations"][i]["conversation_id"])
except ApiException as e:
    print("Exception when calling ConversationApi %s\n" % e)
