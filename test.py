from application import app
from flask import Flask, jsonify, request
from flask_cors import CORS
import config
import openai
import yfinance as yf
openai.api_key = config.OPENAI_API_KEY

CORS(app)


@app.route('/generate1', methods=['POST'])
def generate():
    print("prompt received")
    data = request.get_json()
    prompt = data['prompt']
    print(prompt)

    def openai_completion(query):
        print("Starting GPT-3\n")
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo", messages=[{"role": "user", "content": query}])
        response = completion.choices[0].message.content
        print("GPT-3 response: " + response)
        return response

    result = openai_completion(prompt)
    return jsonify({'response': result})
