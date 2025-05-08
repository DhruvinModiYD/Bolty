# sheet_utils.py
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
import os

def log_action(user_id, action_desc):
    try:
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        creds = ServiceAccountCredentials.from_json_keyfile_name("gcred.json", scope)
        client = gspread.authorize(creds)

        sheet = client.open("Slack_bot_logs").sheet1
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        sheet.append_row([now, user_id, action_desc])
    except Exception as e:
        print(f"Logging Error: {e}")
