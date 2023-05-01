from application import app
from flask import jsonify, request
from flask_cors import CORS

import gpt
import stock
import sql

CORS(app)

context_data = 'You are a friendly financial chatbot. The user will ask you questions, and you will provide polite responses.\n\n'

@app.route('/generate', methods=['POST'])
def generate():
    global context_data
    email = request.cookies.get('email')

    data = request.get_json()
    userMessage = data['prompt']
    print("user message received:")
    print(userMessage + '\n')

    promptResult = stock.promptProfit(userMessage)
    # perform a specific action for when stock information is present
    if promptResult[1]:
        print("Stock information detected in context_data. Performing specific action...\n")
        context_data += 'Q: ' + promptResult[0] + '\nA: '
        # add stock to database
        start_date, ticker, num_shares, start_price, end_price, return_percent, return_amount, total = promptResult[2]
        print(promptResult[2])
        sql.addStock(email, start_date, ticker, num_shares, start_price, end_price, return_percent, return_amount, total)

    # normal bot reply
    else:
        print("No stock information detected in context_data.\n")
        context_data += 'Q: ' + userMessage + '\nA: '

    result = gpt.openAi(context_data)
    context_data += result + '\n\n'
    print(context_data)

    return jsonify({'response': result})

# I bought 200 apple shares on 12/12/2020, what is my profit?
