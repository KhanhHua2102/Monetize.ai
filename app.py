import re
from datetime import datetime

from flask import jsonify, request
from flask_cors import CORS

import gpt
import sql
import stock as stk
from application import app

CORS(app)

context_data = 'You are a friendly financial chatbot named Monetize.ai. The user will ask you questions, and you will provide polite responses.\n\n'

@app.route('/generate', methods=['POST'])
def generate():
    global context_data
    email = request.cookies.get('email')

    data = request.get_json()
    user_message = data['prompt']
    print("user message received:")
    print(user_message + '\n')

    # if user buy stock, we add stock to user's portfolio and reply a bot response with profit information
    if re.search(r'\b(buy|bought)\b', user_message, re.IGNORECASE):
        print("User message contains buy or bought keyword")
        
        prompt_result = stk.prompt_profit(user_message)
        start_date, ticker, quantity, start_price, end_price, return_percent, return_amount, total = prompt_result[2]

        # add or update stock in portfolio
        sql.add_stock(email, start_date, ticker, quantity, start_price,
                          end_price, return_percent, return_amount, total)
        
        context_data += 'Q: ' + prompt_result[0] + '\nA: '

    # if user sell stock, we update user's portfolio and reply a normal bot response
    elif re.search(r'\b(sell|sold)\b', user_message, re.IGNORECASE):
        print("User message contains sell or sold keyword")
        
        prompt_result = stk.prompt_profit(user_message)
        start_date, ticker, quantity, start_price, end_price, return_percent, return_amount, total = prompt_result[2]
        
        # update stock in portfolio
        if sql.get_stock_data(email) is not None:
            sql.update_stock(email, ticker, (0 - int(quantity)))
        
        context_data += 'Q: ' + prompt_result[0] + '\nA: '
    
    
    # normal bot response
    else:
        print("No stock information detected in context_data.\n")
        context_data += 'Q: ' + user_message + '\nA: '

    result = gpt.open_ai_with_user_info(context_data)
    context_data += result + '\n\n'
    print(context_data)

    # add user message to database
    sql.add_message(email, user_message, datetime.now())

    # add bot response to database
    sql.add_message(email, result, datetime.now())

    return jsonify({'response': result})

# I bought 200 Apple shares on 12/12/2020, what is my profit?
# I sold 50 Apple shares on 12/12/2021.

@app.route('/get_messages', methods=['GET', 'POST'])
def get_messages():
    email = request.cookies.get('email')
    messages = sql.get_messages(email)

    if len(messages) < 2:
        return jsonify({'messages': {}})
        
    # get 4 last messages into a json object
    msg_result = {}
    for message in range(4):
        msg_result[str(3 - message)] = messages[str(len(messages) - message - 1)]

    jsonify(msg_result)

    return jsonify({'messages': msg_result})


if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1:5000')
