from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
import os
import time
from dotenv import load_dotenv
from prompts import generate_message  # Ensure this returns a motivational message string

# Load environment variables from .env file
load_dotenv()

# Initialize Slack WebClient
client = WebClient(token=os.environ["SLACK_BOT_TOKEN"])

def send_morning_messages():
    try:
        # ✅ Send motivational message to each real (non-bot, active) user
        users = client.users_list()["members"]
        for user in users:
            if not user.get("is_bot") and not user.get("deleted"):
                uid = user["id"]
                message = generate_message()

                try:
                    client.chat_postMessage(channel=uid, text=message)
                    print(f"✅ Sent message to {uid}")
                    time.sleep(1.2)  # Rate limiting buffer
                except SlackApiError as e:
                    print(f"❌ Error sending DM to {uid}: {e.response['error']}")

        # ✅ Find the channel ID dynamically using the channel name
        channel_id = None
        channels = client.conversations_list(types="public_channel")["channels"]
        for ch in channels:
            if ch["name"] == "well-being":
                channel_id = ch["id"]
                break

        if not channel_id:
            print("❌ Channel 'well-being' not found.")
            return

        # ✅ Post poll message to the channel
        poll_text = (
            "📊 *Daily Poll:* How are you feeling today?\n"
            "React with:\n"
            "🟢 Good\n😐 Okay\n🔴 Not great"
        )
        response = client.chat_postMessage(channel=channel_id, text=poll_text)

        # ✅ Add emoji reactions to the poll for users to vote
        ts = response["ts"]
        emojis = ["large_green_circle", "neutral_face", "red_circle"]
        for emoji in emojis:
            try:
                client.reactions_add(channel=channel_id, timestamp=ts, name=emoji)
                time.sleep(0.8)  # Slight delay between emoji adds
            except SlackApiError as e:
                print(f"❌ Error adding emoji :{emoji}: - {e.response['error']}")

        print("✅ Poll and private messages sent successfully.")

    except SlackApiError as e:
        print(f"❌ Slack API Error: {e.response['error']}")

if __name__ == "__main__":
    send_morning_messages()