from flask import Flask, render_template
import PureCloudPlatformClientV2
import json

app = Flask(__name__)


@app.route("/")
def index():
    client_id = "a5208453-0f8c-47f7-a4d7-f7819a82a72c"
    client_secret = "ncusIp3wWDcAFG6MDPFiWUJMdOQ8roudR2k5AhJLND8"

    region = PureCloudPlatformClientV2.PureCloudRegionHosts.ap_northeast_1
    PureCloudPlatformClientV2.configuration.host = region.get_api_host()
    apiclient = (
        PureCloudPlatformClientV2.api_client.ApiClient().get_client_credentials_token(
            client_id, client_secret
        )
    )

    # users_Api = PureCloudPlatformClientV2.UsersApi(apiclient)
    # rec_Api = PureCloudPlatformClientV2.RecordingApi(apiclient)
    conv_Api = PureCloudPlatformClientV2.ConversationsApi(apiclient)

    # response = users_Api.get_user("ee55c231-3ed3-4779-9500-f0c0e143f66c").to_json()
    # conversation_id=["b1cd6a97-bbdd-4ba8-b755-4418fae8a654"]
    # conversation_id.append("895134b8-99ac-46ce-9700-6b89437008d3")
    # response = conv_Api.get_analytics_conversations_details(id=conversation_id).to_json()
    # response = conv_Api.get_conversations_messages().to_json()

    body = PureCloudPlatformClientV2.ConversationQuery()
    body.interval = "2023-08-01T16:00:00.000Z/2023-08-07T16:00:00.000Z"
    response = conv_Api.post_analytics_conversations_details_query(body).to_json()

    data = json.loads(response)
    return render_template("index.html", data=data["conversations"])


@app.route("/home")
def home():
    return render_template("home.html")


if __name__ == "__main__":
    app.run(port=2020, host="127.0.0.1", debug=True)
