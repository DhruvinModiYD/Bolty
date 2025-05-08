import os
import time
import random
import schedule # type: ignore
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from dotenv import load_dotenv
from prompts import polls, generate_affirmation

# Load environment variables
load_dotenv()
client = WebClient(token=os.environ["SLACK_BOT_TOKEN"])

def send_affirmation_to_all_users():
    try:
        users = client.users_list()["members"]
        for user in users:
            if not user.get("is_bot") and not user.get("deleted") and user.get("id"):
                try:
                    affirmation = generate_affirmation()
                    client.chat_postMessage(channel=user["id"], text=affirmation)
                    time.sleep(0.8)
                except SlackApiError as e:
                    print(f"⚠️ DM to {user['id']} failed: {e.response['error']}")
        print("✅ Affirmations sent to all users.")
    except SlackApiError as e:
        print(f"❌ Error fetching users: {e.response['error']}")

def send_poll_to_channel():
    try:
        poll = random.choice(polls)
        question = poll["question"]
        options = poll["options"]
        results = poll["results"]

        # Get channel ID
        channels = client.conversations_list(types="public_channel")["channels"]
        channel_id = next((ch["id"] for ch in channels if ch["name"] == "well-being"), None)
        if not channel_id:
            print("❌ Channel 'well-being' not found.")
            return

        # Format and post the poll
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

        print("✅ Poll sent successfully.\n⏳ Waiting 60s for reactions...")
        time.sleep(60)

        # Fetch emoji reactions
        message_data = client.reactions_get(channel=channel_id, timestamp=ts)["message"]
        reactions = message_data.get("reactions", [])
        top_emoji = max(reactions, key=lambda r: r["count"])["name"] if reactions else None

        # Post result
        if top_emoji in results:
            result_text = results[top_emoji]
            client.chat_postMessage(channel=channel_id, text=f"🗳️ *Poll Result:* {result_text}")
        else:
            client.chat_postMessage(channel=channel_id, text="📉 Not enough reactions to evaluate the poll.")

    except SlackApiError as e:
        print(f"❌ Slack API Error: {e.response['error']}")

# Schedule tasks
schedule.every().day.at("08:00").do(send_affirmation_to_all_users)
schedule.every().day.at("09:00").do(send_poll_to_channel)

print("✅ Scheduler is running... (Affirmations @ 8AM, Polls @ 9AM)")
while True:
    schedule.run_pending()
    time.sleep(30)