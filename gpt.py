import requests
from application import app
from flask import Flask, jsonify, request
from flask_cors import CORS
import config
import openai

openai.api_key = config.OPENAI_API_KEY

app = Flask(__name__)
CORS(app)

response = openai.Completion.create(
    model="text-davinci-003", prompt="Say this is a test", temperature=0, max_tokens=7)


def generate_text(query):
    openai.api_key = config.OPENAI_API_KEY

    response = openai.Completion.create(
        model="text-davinci-003",
        prompt="how is your day my friend\n",
        temperature=0,
        max_tokens=100,
        top_p=1,
        frequency_penalty=0.0,
        presence_penalty=0.0,
        stop=["\n"]
    )

    return response


@app.route('/generate', methods=['POST'])
def generate():
    query = request.json['query']
    print(query)
    result = generate_text(query)
    print(result)

    return jsonify({'response': result})


# https://www.youtube.com/watch?v=G3PctszbrrE
# https: // github.com/OthersideAI/chronology/tree/main/demo
