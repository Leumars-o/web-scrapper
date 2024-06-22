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
            message = f"**There are {projects['Active Projects']} active projects in the intranet.**\n\n"
        if projects.get('Active Projects') == 1:
            message = f"**There is {projects['Active Projects']} active project in the intranet.**\n\n"
        else:
            message = f"**There are no active projects in the intranet.**\n\n"
        # Add project details to message
        for project in projects:
            count = 1
            if project == f'task-{count}':
                message += f"- **Project Name:**\n {projects[project]['name']}\n"
                message += f"- **Start Date:** {projects[project]['start_date']} {projects[project]['start_time']}\n"
                message += f"- **Deadline Date:** {projects[project]['deadline_date']} {projects[project]['deadline_time']}\n"
                message += f"- **Progress:** {projects[project]['progress']}\n\n"
                message += f"View Project on the [intranet]({projects[project]['link']})\n"
                count += 1
        url = f"https://api.telegram.org/bot{telegram_token}/sendMessage"
        data = {"chat_id": chat_id, "text": message}
        headers = {"Content-Type": "application/json", "cache-control": "no-cache"}

        try:
            response = requests.post(url, headers=headers, json=data)
            response.raise_for_status()
            print(f"Notification sent to Telegram chat {chat_id}")
        except requests.exceptions.RequestException as e:
            print(f"Error sending notification: {e}")
        