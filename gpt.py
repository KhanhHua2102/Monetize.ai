from application import app
from flask import Flask, jsonify, request
from flask_cors import CORS
import config
import openai

openai.api_key = config.OPENAI_API_KEY

app = Flask(__name__)
CORS(app)

@app.route('/generate', methods=['POST'])
def generate():
    def openai_completion(query):
        print("Starting GPT-3\n")

        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo", messages=[{"role": "user", "content": query}])
        response = completion.choices[0].message.content

        # completion = openai.Completion.create(model="ada", prompt="Hello world")
        # response = completion.choices[0].text

        print("GPT-3 response: " + response)
        return response

    if request.is_json:
        print("prompt received")
        data = request.get_json()
        prompt = data['prompt']
        print(prompt)

        result = openai_completion(prompt)

        return jsonify({'response': result})
    else:
        return jsonify({'error': 'Invalid request'})