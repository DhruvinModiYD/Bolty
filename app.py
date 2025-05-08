from slack_bolt import App
from slack_bolt.adapter.flask import SlackRequestHandler
from flask import Flask, request
from dotenv import load_dotenv
import os
from slack_sdk.errors import SlackApiError
from sheet_utils import log_action

# Load environment variables
load_dotenv()

# Initialize Slack Bolt App
app = App(
    token=os.environ["SLACK_BOT_TOKEN"],
    signing_secret=os.environ["SLACK_SIGNING_SECRET"]
)

flask_app = Flask(__name__)
handler = SlackRequestHandler(app)

# ✅ Root route for health check
@flask_app.route("/", methods=["GET"])
def health_check():
    return "Slack bot is running!", 200

# ✅ Respond to any direct message
@app.event("message")
def handle_any_message(event, say):
    user = event.get("user")
    channel = event.get("channel")
    subtype = event.get("subtype")
    channel_type = event.get("channel_type")

    if subtype is None and user and channel_type == "im":
        try:
            say(
                channel=channel,
                text=f"Hey <@{user}> 👋, how are you doing today?\nHere are some things I can help you with:",
                blocks=[
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": f"Hey <@{user}> 👋, how are you doing today?\nHere are some things I can help you with:"
                        }
                    },
                    {
                        "type": "actions",
                        "elements": [
                            {
                                "type": "button",
                                "text": {"type": "plain_text", "text": "Tell me a joke 🎃"},
                                "action_id": "joke_button"
                            },
                            {
                                "type": "button",
                                "text": {"type": "plain_text", "text": "Send a calming quote 🧘"},
                                "action_id": "quote_button"
                            },
                            {
                                "type": "button",
                                "text": {"type": "plain_text", "text": "Wellness summary 📊"},
                                "action_id": "summary_button"
                            }
                        ]
                    }
                ]
            )
        except SlackApiError as e:
            print(f"❌ Slack API error in DM reply: {e.response['error']}")

# ✅ Button: Tell a joke
@app.action("joke_button")
def handle_joke_button(ack, body, client):
    ack()
    user_id = body["user"]["id"]
    channel_id = body["channel"]["id"]
    try:
        client.chat_postMessage(
            channel=channel_id,
            text=f"Here's a joke for you <@{user_id}>: Why don’t scientists trust atoms? Because they make up everything!"
        )
        log_action(user_id, "Clicked 'Tell me a joke'")
    except SlackApiError as e:
        print(f"❌ Error sending joke: {e.response['error']}")

# ✅ Button: Send a calming quote
@app.action("quote_button")
def handle_quote_button(ack, body, client):
    ack()
    user_id = body["user"]["id"]
    channel_id = body["channel"]["id"]
    try:
        client.chat_postMessage(
            channel=channel_id,
            text=f"Here's something calming, <@{user_id}>: 'This too shall pass.'"
        )
        log_action(user_id, "Clicked 'Send a calming quote'")
    except SlackApiError as e:
        print(f"❌ Error sending quote: {e.response['error']}")

# ✅ Button: Wellness summary
@app.action("summary_button")
def handle_summary_button(ack, body, client):
    ack()
    user_id = body["user"]["id"]
    channel_id = body["channel"]["id"]
    try:
        client.chat_postMessage(
            channel=channel_id,
            text=f"Here's your wellness summary, <@{user_id}>.\n(This is a placeholder summary.)"
        )
        log_action(user_id, "Clicked 'Wellness summary'")
    except SlackApiError as e:
        print(f"❌ Error sending summary: {e.response['error']}")

# ✅ Slack routes
@flask_app.route("/slack/events", methods=["POST"])
def slack_events():
    return handler.handle(request)

@flask_app.route("/slack/interactions", methods=["POST"])
def slack_interactions():
    return handler.handle(request)

if __name__ == "__main__":
    flask_app.run(port=3000)