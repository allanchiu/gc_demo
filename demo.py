import PureCloudPlatformClientV2
import json

client_id = "a5208453-0f8c-47f7-a4d7-f7819a82a72c"
client_secret = "ncusIp3wWDcAFG6MDPFiWUJMdOQ8roudR2k5AhJLND8"

region = PureCloudPlatformClientV2.PureCloudRegionHosts.ap_northeast_1
PureCloudPlatformClientV2.configuration.host = region.get_api_host()
apiclient = (
    PureCloudPlatformClientV2.api_client.ApiClient().get_client_credentials_token(
        client_id, client_secret
    )
)

conv_Api = PureCloudPlatformClientV2.ConversationsApi(apiclient)

body=PureCloudPlatformClientV2.ConversationQuery()
body.interval = "2023-07-04T16:00:00.000Z/2023-07-07T16:00:00.000Z"
Predicate = PureCloudPlatformClientV2.ConversationDetailQueryPredicate()
CF=PureCloudPlatformClientV2.ConversationDetailQueryFilter()

Predicate.type='metric'
Predicate.metric='tAnswered'
Predicate.operator='gt'
Predicate.value=100000
CF.predicates.append(Predicate)
body.conversation_filters.append(CF)
response = conv_Api.post_analytics_conversations_details_query(body).to_json()

data = json.loads(response)

for item in data["conversations"]:
    print(item['conversation_id'])
