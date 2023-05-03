from application import app
from flask import jsonify, request
from flask_cors import CORS
import re

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
    user_message = data['prompt']
    print("user message received:")
    print(user_message + '\n')

    prompt_result = stock.prompt_profit(user_message)
    start_date, ticker, quantity, start_price, end_price, return_percent, return_amount, total = prompt_result[2]
    buy_sell = prompt_result[3]
    # perform a specific action for when stock information is present
    # if user's message contain sell or sold keyword, we update their portfolio and reply a normal bot response
    if buy_sell == 'sell':
        if sql.get_stock_data(email) is not None:
            sql.update_stock(email, ticker, 0 - quantity)
        context_data += 'Q: ' + user_message + '\nA: '
    elif prompt_result[1]:  # add stock to user's portfolio and answer with profit
        print("Stock information detected in context_data. Performing specific action...\n")
        context_data += 'Q: ' + prompt_result[0] + '\nA: '

        # add stock to database
        if sql.get_stock_data(email) is None:
            sql.add_stock(email, start_date, ticker, quantity, start_price,
                          end_price, return_percent, return_amount, total)
        else:
            sql.update_stock(email, ticker, quantity)

    # normal bot reply
    else:
        print("No stock information detected in context_data.\n")
        context_data += 'Q: ' + user_message + '\nA: '

    result = gpt.open_ai(context_data)
    context_data += result + '\n\n'
    print(context_data)

    return jsonify({'response': result})

# I bought 200 apple shares on 12/12/2020, what is my profit?
# I sold 20 apple shares on 12/12/2021.
