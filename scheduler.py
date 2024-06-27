
import genai as genai
import random
import json
import intranet_login as intranet
import telegram_notify as telegram
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler, BlockingScheduler

random_number = random.randint(0, 2)

functions = ['execute_quiz', 'execute_fact', 'execute_quote']

def execute_intranet():
    # Get projects from intranet
    projects = intranet.main()
    # send project notification to telegram
    telegram.send_project(projects)

    job_id.remove()
    scheduler.shutdown(wait=False)


def execute_quiz():
    # Generate a quiz question
    quiz = genai.prompt_model(genai.prompts, 0)
    # send quiz to telegram
    telegram.send_quiz(quiz)

    # job_id.remove()
    # scheduler.shutdown(wait=False)

def execute_fact():
    # Get a fact
    fact = genai.prompt_model(genai.prompts, 1)
    # send fact to telegram
    telegram.send_message(fact, 'Fact')

    # job_id.remove()
    # scheduler.shutdown(wait=False)

def execute_quote():
    # Get a quote
    quote = genai.prompt_model(genai.prompts, 2)
    # send quote to telegram
    telegram.send_message(quote, 'Quote')
    
    # job_id.remove()
    # scheduler.shutdown(wait=False)

scheduler = BlockingScheduler()
job_id = scheduler.add_job(execute_intranet, 'interval', seconds = 5)
# scheduler.add_job(eval(functions[random_number]), 'interval', minutes = 1)

scheduler.start()
