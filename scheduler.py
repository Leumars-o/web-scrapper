""" This module is responsible for scheduling the execution of the functions
    in the program.
    The functions are executed at a specific time of the day
"""

import genai as genai
import random
import json
import intranet_login as intranet
import telegram_notify as telegram
from apscheduler.schedulers.background import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger


def execute_intranet():
    """ This function is responsible for executing the intranet function

    Returns:
        _type_: dict
                The projects from the intranet module
    """
    # Get projects from intranet
    projects = intranet.main()
    # send project notification to telegram
    telegram.send_project(projects)


def execute_quiz():
    """ This function is responsible for executing the quiz function

    Returns:
        _type_: dict
                The quiz from the genai module
    """
    # Generate a quiz question
    quiz = genai.prompt_model(genai.prompts, 0)
    # send quiz to telegram
    telegram.send_quiz(quiz)


def execute_fact():
    """ This function is responsible for executing the fact function

    Returns:
        _type_: dict
                The fact from the genai module
    """
    # Get a fact
    fact = genai.prompt_model(genai.prompts, 1)
    # send fact to telegram
    telegram.send_message(fact, 'Fact')


def execute_quote():
    """ This function is responsible for executing the quote function

    Returns:
        _type_: dict
                The quote from the genai module
    """
    # Get a quote
    quote = genai.prompt_model(genai.prompts, 2)
    # send quote to telegram
    telegram.send_message(quote, 'Quote')
    


# Generate a random number
random_number = random.randint(0, 2)

# Create a list of functions to execute
functions = [execute_quiz, execute_fact, execute_quote]

# Create triggers for the scheduler
trigger_projects = CronTrigger(hour = '16', minute = '*', second = '0')
trigger_ai = CronTrigger(hour = '16', minute = '*', second = '1')

# Create the scheduler
scheduler = BlockingScheduler()
scheduler.add_job(execute_intranet, trigger_projects)
scheduler.add_job(functions[random_number], trigger_ai)

# Start the scheduler
scheduler.start()
