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
    return openai.Completion.create(
        model="text-davinci-003", prompt="hello can you introduce yourself", temperature=0, max_tokens=7)["choices"][0]["text"]


@app.route('/generate', methods=['POST'])
def generate():
    query = request.json
    print(query)
    print("test")
    print(generate_text("hello can you introduce yourself"))

    return jsonify({'response': generate_text(query)})
