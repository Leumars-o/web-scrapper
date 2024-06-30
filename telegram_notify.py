""" This module sends messages to a Telegram chat using the Telegram Bot API.
"""

import requests
import os
import json
from dotenv import load_dotenv


# Load environment variables
load_dotenv()
telegram_token = os.getenv('TELEGRAM_TOKEN')
chat_id = os.getenv('TELEGRAM_CHAT_ID')

# Set base url
base_url = "https://api.telegram.org/bot"

# Send Active Projects to Telegram
def send_project(projects):
    """ This function is responsible for sending active projects to Telegram

    Args:
        projects (_type_): dict
                            The projects from the intranet module
    """
    # Construct message 
    if projects is not None:
        if 'evaluation_quiz' in projects:
            quiz_id = int(projects['evaluation_quiz']) - 11
            message = f"❕*Evaluation Quiz {quiz_id} is available on the intranet*\n\n"
        elif projects.get('Active Projects') > 1:
            message = f"❕*You Have {projects['Active Projects']} Active Projects On The Intranet.*\n\n"
        elif projects.get('Active Projects') == 1:
            message = f"❕*You Have {projects['Active Projects']} Active Project On The Intranet.*\n\n"
        else:
            message = f"❕*There Are No Active Projects On The Intranet.*\n\n"
            
        # Add project details to message
        if projects.get('Active Projects') > 0:
            count = 1
            for project in projects:
                if project == f"task-{count}":
                    message += f"📌 *Project:* {projects[project]['name']}\n\n"
                    message += f" 📆 *Start Date:* {projects[project]['start_date']} at {projects[project]['start_time']}\n"
                    if projects[project]['deadline_time'] is None:
                        message += f"⏰ *Deadline:* {projects[project]['deadline_date']}\n"
                    else:
                        message += f"⏰ *Deadline:* {projects[project]['deadline_date']} by {projects[project]['deadline_time']}\n"
                    message += f"📊 *Progress:* {projects[project]['progress']}\n"
                    message += f"🔗 [View project on the Intranet]({projects[project]['link']})\n\n"
                    count += 1
        
        # Send message to Telegram chat
        url = f"{base_url}{telegram_token}/sendMessage"
        data = {"chat_id": chat_id, "text": message, "parse_mode": "Markdown"}
        headers = {"Content-Type": "application/json", "cache-control": "no-cache"}

        try:
            response = requests.post(url, headers=headers, json=data)
            response.raise_for_status()
            print(f"Projects sent to Telegram chat {chat_id}")
        except requests.exceptions.RequestException as e:
            print(f"Error sending projects: {e}")

# Send Quiz to Telegram
def send_quiz(quiz):
    """ This function is responsible for sending a quiz to Telegram

    Args:
        quiz (_type_): dict
                        The quiz from the genai module
    """
    
    # Construct quiz
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

    # Send quiz to Telegram
    url = f"{base_url}{telegram_token}/sendPoll"
    response = requests.post(url, data=parameters)
    print(response.status_code)

# Send Fact to Telegram
def send_message(message, msg_type):
    """ This function is responsible for sending a 'Fact' to Telegram

    Args:
        message (_type_): string
        msg_type (_type_): string
    """
    # Construct message
    if message is not None:
        if msg_type == 'Fact':
            message = f"📜 *Here's An Interesting Fact:* \n\n{message}"
        elif msg_type == 'Quote':
            message = f"📜 *Programming Quote of the Day:* \n\n{message}"

    # Send message to Telegram chat
    url = f"{base_url}{telegram_token}/sendMessage"
    data = {"chat_id": chat_id, "text": message, "parse_mode": "Markdown"}
    headers = {"Content-Type": "application/json", "cache-control": "no-cache"}

    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        print(f"Message sent to Telegram chat {chat_id}")
    except requests.exceptions.RequestException as e:
        print(f"Error sending message: {e}")
