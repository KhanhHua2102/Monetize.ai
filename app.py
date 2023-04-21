from application import app
from flask import Flask, jsonify, request
from flask_cors import CORS
import config
import openai

openai.api_key = config.OPENAI_API_KEY

CORS(app)

context_data = 'You are a friendly financial chatbot. The user will ask you questions, and you will provide polite responses.\n\n'

@app.route('/generate', methods=['POST'])
def generate():
    print("prompt received")
    data = request.get_json()
    prompt = data['prompt']
    print(prompt)

    global context_data
    context_data += 'Q: ' + prompt + '\nA: '

    def openai_completion(query):
        print("Starting GPT-3\n")
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo", messages=[{"role": "user", "content": query}])
        response = completion.choices[0].message.content
        global context_data
        context_data += response + '\n\n'
        return response

    result = openai_completion(context_data)
    print(context_data)
    return jsonify({'response': result})