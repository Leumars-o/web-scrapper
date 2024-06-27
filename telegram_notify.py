#!/usr/bin/python3

import requests
import os
import json
from dotenv import load_dotenv

load_dotenv()

base_url = "https://api.telegram.org/bot"
telegram_token = os.getenv('TELEGRAM_TOKEN')
chat_id = os.getenv('TELEGRAM_CHAT_ID')


# Send Active Projects to Telegram
def send_project(projects):
    # Construct message 
    if projects is not None:
        if 'evaluation_quiz' in projects:
            message = f"❕*Evaluation Quiz {projects['evaluation_quiz']} is available on the intranet*\n\n"
        elif projects.get('Active Projects') > 1:
            message = f"❕*You Have {projects['Active Projects']} Active Projects On The Intranet.*\n\n"
        elif projects.get('Active Projects') == 1:
            message = f"❕*You Have {projects['Active Projects']} Active Project On The Intranet.*\n\n"
        else:
            message = f"❕*There Are No Active Projects On The Intranet.*\n\n"
            
        # Add project details to message
        if projects.get('Active Projects') > 0:
            for project in projects:
                count = 1
                if project == f'task-{count}':
                    message += f"📌 *Project Name:* {projects[project]['name']}\n\n"
                    message += f" 📆 *Start Date:* {projects[project]['start_date']} at {projects[project]['start_time']}\n"
                    message += f"⏰ *Deadline:* {projects[project]['deadline_date']} by {projects[project]['deadline_time']}\n"
                    message += f"📊 *Progress:* {projects[project]['progress']}\n"
                    message += f"🔗 [View project on the Intranet]({projects[project]['link']})\n\n"
                    count += 1
        url = f"{base_url}{telegram_token}/sendMessage"
        data = {"chat_id": chat_id, "text": message, "parse_mode": "Markdown"}
        headers = {"Content-Type": "application/json", "cache-control": "no-cache"}

        try:
            response = requests.post(url, headers=headers, json=data)
            response.raise_for_status()
            print(f"Projects sent to Telegram chat {chat_id}")
        except requests.exceptions.RequestException as e:
            print(f"Error sending projects: {e}")


def send_quiz(quiz):
    
    question = quiz['question']
    options = json.dumps(quiz['options'])
    correct_option_id = quiz['correct_option_id']
    explanation = quiz['explanation']

    parameters = {
    "chat_id" : os.getenv("TELEGRAM_CHAT_ID"),
    "question": f"🤔💻 *Question of the Day:* \n\n{question}",
    "options": options,
    "correct_option_id": correct_option_id,
    "explanation": explanation,
    "type" : "quiz"
    }

    url = f"{base_url}{telegram_token}/sendPoll"
    response = requests.post(url, data=parameters)
    print(response.status_code)


def send_message(message, msg_type):
    # Construct message
    if message is not None:
        if msg_type == 'Fact':
            message = f"📜 *Here's An Interesting Fact:* \n\n{message}"
        elif msg_type == 'Quote':
            message = f"📜 *Programming Quote of the Day:* \n\n{message}"

    url = f"{base_url}{telegram_token}/sendMessage"
    data = {"chat_id": chat_id, "text": message, "parse_mode": "Markdown"}
    headers = {"Content-Type": "application/json", "cache-control": "no-cache"}

    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        print(f"Message sent to Telegram chat {chat_id}")
    except requests.exceptions.RequestException as e:
        print(f"Error sending message: {e}")
