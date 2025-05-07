from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
import os
import time
import random
from dotenv import load_dotenv
from prompts import polls, generate_affirmation

# Load secrets from .env file
load_dotenv()

client = WebClient(token=os.environ["SLACK_BOT_TOKEN"])

def send_poll():
    try:
        # Pick a random poll from the bank
        poll = random.choice(polls)
        question = poll["question"]
        options = poll["options"]

        # Find channel ID from name
        channel_id = None
        result = client.conversations_list(types="public_channel,private_channel")
        for ch in result["channels"]:
            if ch["name"] == os.environ["CHANNEL_NAME"]:
                channel_id = ch["id"]
                break

        if not channel_id:
            print("❌ Channel not found.")
            return

        # Send the poll to the channel
        poll_text = f"{question}\n\n" + "\n".join([f"{emoji} = {desc}" for emoji, desc in options.items()])
        response = client.chat_postMessage(channel=channel_id, text=poll_text)
        ts = response["ts"]  # Timestamp to track reactions

        # Add emoji reactions to the message
        for emoji in options:
            try:
                client.reactions_add(channel=channel_id, timestamp=ts, name=emoji)
                time.sleep(0.8)
            except SlackApiError as e:
                print(f"⚠️ Error adding emoji :{emoji}: - {e.response['error']}")

        print("✅ Poll sent successfully.")

        # Simulated wait for reactions to come in (in real usage, use event-based or delay)
        print("⏳ Waiting for reactions...")
        time.sleep(10)

        # Get message reactions from Slack
        message = client.reactions_get(channel=channel_id, timestamp=ts)["message"]
        reactions = message.get("reactions", [])

        # Tally votes
        max_count = 0
        winner = None
        low_energy_users = []

        for r in reactions:
            name = r["name"]
            count = r["count"]
            users = r.get("users", [])

            if count > max_count:
                max_count = count
                winner = name

            if name in poll.get("low_energy_emojis", []):
                low_energy_users.extend(users)

        # Post summary in channel
        summary_text = poll["results"].get(winner, "Thanks for participating!")
        client.chat_postMessage(channel=channel_id, text=f"📢 *Poll Result:* {summary_text}")

        # Send affirmations to low-energy users
        sent = set()
        for uid in low_energy_users:
            if uid not in sent:
                affirmation = generate_affirmation()
                try:
                    client.chat_postMessage(channel=uid, text=affirmation)
                    sent.add(uid)
                except SlackApiError as e:
                    print(f"❌ DM to {uid} failed: {e.response['error']}")

        print("✅ Affirmations sent to low-energy responders.")

    except SlackApiError as e:
        print(f"❌ Slack API Error: {e.response['error']}")

if __name__ == "__main__":
    send_poll()