from flask import Flask, render_template, request
import time

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
    conversation_list = []
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

    # 获取日期参数
    start_time = request.args.get('start_time')
    end_time = request.args.get('end_time')

    if start_time and end_time:
        # 转换日期格式
        start_time_iso = start_time + '.000Z'
        end_time_iso = end_time + '.999Z'
        body.interval = f"{start_time_iso}/{end_time_iso}"
    else:
        # 返回空值
        return render_template("conversation.html", data=conversation_list)

    try:
        api_response = conversationApi.post_analytics_conversations_details_query(body)
        response = api_response.to_dict()
        conversations = response["conversations"]
        total_hits = response["total_hits"]
        if total_hits > 0:
            for i in range(0, total_hits):
                conversation_list.append(conversations[i])
            return render_template("conversation.html", data=conversation_list)
        else:
            return "no conversation"
    except ApiException as e:
        print("Exception when calling ConversationApi %s\n" % e)


@app.route("/play_recording")
def play_recording():
    conversation_id = request.args.get("conversation_id")  # str | Conversation ID
    max_wait_ms = 5000  # int | The maximum number of milliseconds to wait for the recording to be ready. Must be a positive value. (optional) (default to 5000)
    format_id = "WAV"  # str | The desired media format. Valid values:WAV,WEBM,WAV_ULAW,OGG_VORBIS,OGG_OPUS,MP3,NONE. (optional) (default to 'WEBM')
    media_formats = [
        "WAV"
    ]  # list[str] | All acceptable media formats. Overrides formatId. Valid values:WAV,WEBM,WAV_ULAW,OGG_VORBIS,OGG_OPUS,MP3. (optional)

    try:
        for i in range(0, 2):
            api_response = recordApi.get_conversation_recordings(
                conversation_id,
                max_wait_ms=max_wait_ms,
                format_id=format_id,
                media_formats=media_formats,
            )
            if api_response != []:
                uri = api_response[0].media_uris["0"].media_uri
                return render_template("recording.html", data=uri)
            time.sleep(3)

        return "no recording"

    except ApiException as e:
        if e.status == 403 or e.status == 404:
            return "no recording"
        print(
            "Exception when calling RecordingApi->get_conversation_recordings: %s\n" % e
        )


if __name__ == "__main__":
    app.run(port=2020, host="127.0.0.1", debug=True)
