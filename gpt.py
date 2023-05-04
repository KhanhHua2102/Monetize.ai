import openai

import config
from flask import request
import sql

openai.api_key = config.OPENAI_API_KEY


def open_ai(query):
    print("Starting GPT-3...\n")
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": query}],
        temperature=0.3)
    response = completion.choices[0].message.content
    return response

def open_ai_with_user_info(query):
    print("Starting GPT-3...\n")
    email = request.cookies.get('email')
    user_data = sql.get_user_data(email)
    query = "\nUser information: \nUsername: " + user_data[0] + "\nEmail: " + user_data[1] + "\Phone number: " + str(user_data[2]) + "\n" + query
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": query}],
        temperature=0.3)
    response = completion.choices[0].message.content
    return response
