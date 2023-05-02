import openai
import config

openai.api_key = config.OPENAI_API_KEY


def open_ai(query):
    print("Starting GPT-3...\n")
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": query}],
        temperature=0.3)
    response = completion.choices[0].message.content
    return response
