from application import app
from flask import jsonify, request
from flask_cors import CORS

import gpt
import stock
import sql
# import json

CORS(app)


context_data = 'You are a friendly financial chatbot. The user will ask you questions, and you will provide polite responses.\n\n'


@app.route('/generate', methods=['POST'])
def generate():
    global context_data
    print("user message received:")
    data = request.get_json()
    userMessage = data['prompt']
    print(userMessage + '\n')

    promptResult = stock.promptProfit(userMessage)
    promtRecommendation = stock.promptReccomendation(userMessage)
    # perform a specific action for when stock information is present
    if promptResult[1]:
        print("Stock information detected in context_data. Performing specific action...\n")
        context_data += 'Q: ' + promptResult[0] + '\nA: '
    # normal bot reply
    elif promtRecommendation == True:
        print("Stock recommendation information detected in context_data. Performing specific action...\n")
        context_data += 'Q: ' + userMessage + '\nA: '
    else:
        print("No stock information detected in context_data.\n")
        context_data += 'Q: ' + userMessage + '\nA: '

    result = gpt.openAi(context_data)
    context_data += result + '\n\n'
    print(context_data)

    return jsonify({'response': result})
