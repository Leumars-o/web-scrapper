""" This program is responsible for generating the questions and answers for the quiz.

    Returns:
        _type_: dict
"""
import os
import sys
import json
import random
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv('GENAI_API_KEY'))

random_number = random.randint(0, 3)

# Quiz Prompt Structure
structure = '{\
"question" : " ",\
"options" : ["", "", "", ""],\
"explanation" : "" (200 chars max),\
"correct_option_id" : \
}'

languages = [
  "python",
  "javascript",
  "c",
  "bash"
]

# Prompt Configuration
prompts = [
  f"Generate an interesting quiz question for {languages[random_number]} in the format: {structure}",
  f"Give me a unique programming fun fact on {languages[random_number]} (max response lenght: 1 paragraph)",
  "Give me an inspirational quote for a programmer"
]

# Model Configuration
generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 64,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
}

# Create the model
model = genai.GenerativeModel(
  model_name="gemini-1.5-pro",
  generation_config=generation_config,
  # safety_settings = Adjust safety settings
  # See https://ai.google.dev/gemini-api/docs/safety-settings
)

# Start a chat session
chat_session = model.start_chat(
  history=[]
)
# Prompt the model
def prompt_model(prompts, prompt_index):
  # Send the prompt to the model
  response = chat_session.send_message(prompts[prompt_index])
  # Clean up the response
  response_data = response.text.replace("```json", "").replace("}\n```", "}").strip()

  if prompt_index == 0:
    # Convert the response type to dict
    response_clean = eval(response_data)
    # Return the response dict
    return (response_clean)
  else:
    return (response_data)
