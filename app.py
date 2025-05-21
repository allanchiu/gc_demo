from flask import Flask, render_template

app = Flask(__name__)  # 实例化并命名为app实例


import PureCloudPlatformClientV2
from PureCloudPlatformClientV2.rest import ApiException

CLIENT_ID = "70b17ec8-5475-47fb-b8fe-f8572f4d2b63"
CLIENT_SECRET = "r9eNTdKJcHCURIMvDTuQ7b1AyIP8vgWTnwl6KqdjrJU"
ENVIRONMENT = "https://api.euw2.pure.cloud"  # eg. mypurecloud.com


apiclient = PureCloudPlatformClientV2.api_client.ApiClient()
apiclient.host = ENVIRONMENT
apiclient.get_client_credentials_token(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)

# Create Conversation API Instance
conversationApi = PureCloudPlatformClientV2.ConversationsApi(apiclient)

# Create Rec API Instance
recordApi = PureCloudPlatformClientV2.RecordingApi(apiclient)


@app.route("/")
def index():
    return "Hello World!"


@app.route("/conversations")
def get_conversations():
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
        return(conversations)
    except ApiException as e:
        print("Exception when calling ConversationApi %s\n" % e)


@app.route("/play_recording")
def pay_recording():
    conversation_id = "b938ff7b-d1d3-4e43-9aaf-f8287c839ed8"  # str | Conversation ID
    max_wait_ms = 5000  # int | The maximum number of milliseconds to wait for the recording to be ready. Must be a positive value. (optional) (default to 5000)
    format_id = "WAV"  # str | The desired media format. Valid values:WAV,WEBM,WAV_ULAW,OGG_VORBIS,OGG_OPUS,MP3,NONE. (optional) (default to 'WEBM')
    media_formats = [
        "WAV"
    ]  # list[str] | All acceptable media formats. Overrides formatId. Valid values:WAV,WEBM,WAV_ULAW,OGG_VORBIS,OGG_OPUS,MP3. (optional)

    try:
        api_response = recordApi.get_conversation_recordings(
            conversation_id,
            max_wait_ms=max_wait_ms,
            format_id=format_id,
            media_formats=media_formats,
        )
        uri = api_response[0].media_uris["0"].media_uri
        return render_template("recording.html", data=uri)

    except ApiException as e:
        print(
            "Exception when calling RecordingApi->get_conversation_recordings: %s\n" % e
        )


if __name__ == "__main__":
    app.run(port=2020, host="127.0.0.1", debug=True)
