import os
import time
import random
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from dotenv import load_dotenv
from prompts import polls, generate_affirmation

# Load environment variables
load_dotenv()
client = WebClient(token=os.environ["SLACK_BOT_TOKEN"])

# Get channel ID for 'well-being'
def get_wellbeing_channel_id():
    try:
        channels = client.conversations_list(types="public_channel")["channels"]
        return next((ch["id"] for ch in channels if ch["name"] == "well-being"), None)
    except SlackApiError as e:
        print(f"❌ Error fetching channels: {e.response['error']}")
        return None

# Send an affirmation to all members in the channel
def send_affirmations(channel_id):
    try:
        members = client.conversations_members(channel=channel_id)["members"]
        for user_id in members:
            # Ignore bots
            user_info = client.users_info(user=user_id)["user"]
            if not user_info.get("is_bot") and not user_info.get("deleted"):
                affirmation = generate_affirmation()
                try:
                    client.chat_postMessage(channel=user_id, text=affirmation)
                    time.sleep(0.8)
                except SlackApiError as e:
                    print(f"⚠️ Couldn't DM {user_id}: {e.response['error']}")
        print("✅ Affirmations sent to all channel members.")
    except SlackApiError as e:
        print(f"❌ Failed to get members from channel: {e.response['error']}")

# Send a poll to the channel
def send_poll(channel_id):
    try:
        poll = random.choice(polls)
        question = poll["question"]
        options = poll["options"]
        results = poll["results"]

        # Post the poll
        poll_text = f"*📊 {question}*\n"
        for emoji, label in options.items():
            poll_text += f":{emoji}: = {label}\n"

        response = client.chat_postMessage(channel=channel_id, text=poll_text)
        ts = response["ts"]

        # Add emoji reactions
        for emoji in options:
            try:
                client.reactions_add(channel=channel_id, timestamp=ts, name=emoji)
                time.sleep(0.8)
            except SlackApiError as e:
                print(f"⚠️ Error adding emoji :{emoji}: - {e.response['error']}")

        print("✅ Poll posted. Waiting 30 seconds for reactions...")
        time.sleep(30)

        # Get reactions and compute result
        message_data = client.reactions_get(channel=channel_id, timestamp=ts)["message"]
        reactions = message_data.get("reactions", [])
        top_emoji = max(reactions, key=lambda r: r["count"])["name"] if reactions else None

        if top_emoji and top_emoji in results:
            result_text = results[top_emoji]
            client.chat_postMessage(channel=channel_id, text=f"🗳️ *Poll Result:* {result_text}")
        else:
            client.chat_postMessage(channel=channel_id, text="📉 Not enough reactions to evaluate the poll.")

    except SlackApiError as e:
        print(f"❌ Slack API Error in poll: {e.response['error']}")

# MAIN DEMO RUN
if __name__ == "__main__":
    channel_id = get_wellbeing_channel_id()
    if channel_id:
        print("🚀 Running demo...")
        send_affirmations(channel_id)
        send_poll(channel_id)
    else:
        print("❌ 'well-being' channel not found.")
