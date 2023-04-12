from application import app
from flask import Flask, jsonify, request
from flask_cors import CORS
import config
import openai

openai.api_key = config.OPENAI_API_KEY

app = Flask(__name__)
CORS(app)

# how can i create virtual enrionment in flask app?


@app.route('/generate', methods=['POST'])
def generate():
    print("received request\n-")

    def openai_completion(query):
        print("Starting GPT-3\n")

        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo", messages=[{"role": "user", "content": query}])
        response = completion.choices[0].message.content

        # completion = openai.Completion.create(model="ada", prompt="Hello world")
        # response = completion.choices[0].text

        return response

    if request.is_json:
        print("prompt received")
        data = request.get_json()
        prompt = data['prompt']
        print(prompt)

        result = openai_completion(prompt)
        print(result)

        return jsonify({'response': result})
    else:
        return jsonify({'error': 'Invalid request'})



# https://www.youtube.com/watch?v=G3PctszbrrE
# https: // github.com/OthersideAI/chronology/tree/main/demo
