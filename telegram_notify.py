#!/usr/bin/python3

import requests
import os
from dotenv import load_dotenv

load_dotenv()

telegram_token = os.getenv('TELEGRAM_TOKEN')
chat_id = os.getenv('TELEGRAM_CHAT_ID')


def send_notification(projects):
    # Construct message
    if projects is not None:
        if projects.get('Active Projects') > 1:
            message = f"❕*You Have {projects['Active Projects']} Active Projects On The Intranet.*\n\n"
        if projects.get('Active Projects') == 1:
            message = f"❕*You Have {projects['Active Projects']} Active Project On The Intranet.*\n\n"
        else:
            message = f"❕*There Are No Active Projects On The Intranet.*\n\n"
        # Add project details to message
        for project in projects:
            count = 1
            if project == f'task-{count}':
                message += f"📌 *Project Name:* {projects[project]['name']}\n\n"
                message += f" 📆 *Start Date:* {projects[project]['start_date']} at {projects[project]['start_time']}\n"
                message += f"⏰ *Deadline:* {projects[project]['deadline_date']} by {projects[project]['deadline_time']}\n"
                message += f"📊 *Progress:* {projects[project]['progress']}\n"
                message += f"🔗 [View project on the Intranet]({projects[project]['link']})\n\n"
                count += 1
        url = f"https://api.telegram.org/bot{telegram_token}/sendMessage"
        data = {"chat_id": chat_id, "text": message, "parse_mode": "Markdown"}
        headers = {"Content-Type": "application/json", "cache-control": "no-cache"}

        try:
            response = requests.post(url, headers=headers, json=data)
            response.raise_for_status()
            print(f"Notification sent to Telegram chat {chat_id}")
        except requests.exceptions.RequestException as e:
            print(f"Error sending notification: {e}")
        