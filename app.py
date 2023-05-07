import logging
import re
from datetime import datetime

from flask import jsonify, request
from flask_cors import CORS

import gpt
import sql
import stock as stk
from application import app

CORS(app)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler('logs/app.log')
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
handler.setFormatter(formatter)
logger.addHandler(handler)


context_data = 'You are a friendly financial chatbot named Monetize.ai. The user will ask you questions, and you will provide polite responses.\n\n'

@app.route('/generate', methods=['POST'])
def generate():
    global context_data
    email = request.cookies.get('email')

    data = request.get_json()
    user_message = data['prompt']
    print("user message received:")
    print(user_message + '\n')

    prompt_recommend = stk.prompt_recomendation(user_message)

    # if user buy stock, we add stock to user's portfolio and reply a bot response with profit information
    if re.search(r'\b(buy|bought)\b', user_message, re.IGNORECASE):
        print("User message contains buy or bought keyword\n")
        
        prompt_result = stk.prompt_profit(user_message)
        start_date, ticker, quantity, start_price, end_price, return_percent, return_amount, total = prompt_result[2]

        # add or update stock in portfolio
        sql.add_stock(email, start_date, ticker, quantity, start_price,
                          end_price, return_percent, return_amount, total)
        logger.info('User ' + email + ' bought ' + str(quantity) + ' shares of ' + ticker + ' at $' + str(start_price) + ' on ' + start_date.strftime('%d-%m-%Y') + ' endprice: ' + str(end_price) + ' return percent: ' + str(return_percent) + ' return amount: ' + str(return_amount) + ' total: ' + str(total))

        context_data += 'Q: ' + prompt_result[0] + '\nA: '

    # if user sell stock, we update user's portfolio and reply a normal bot response
    elif re.search(r'\b(sell|sold)\b', user_message, re.IGNORECASE):
        print("User message contains sell or sold keyword\n")
        
        prompt_result = stk.prompt_profit(user_message)
        start_date, ticker, quantity, start_price, end_price, return_percent, return_amount, total = prompt_result[2]
        
        # update stock in portfolio
        if sql.get_stock_data(email) is not None:
            sql.update_stock(email, ticker, (0 - int(quantity)))
            logger.info('User ' + email + ' sold ' + str(quantity) + ' shares of ' + ticker + ' at $' + str(start_price) + ' on ' + start_date.strftime('%d-%m-%Y') + ' endprice: ' + str(end_price) + ' return percent: ' + str(return_percent) + ' return amount: ' + str(return_amount) + ' total: ' + str(total))

        context_data += "Confirmed that the sell action have been recored in user's portfolio.\nQ: " + user_message + '\nA: '
    # if user ask for stock recommendation, we reply a bot response with stock recommendation
    elif prompt_recommend[1]:
        print("Stock recommendation information detected in context_data\n")
        context_data += 'Q: ' + (prompt_recommend[0]) + '\nA: '
    # normal bot reply
    else:
        print("No stock information detected in context_data\n")
        context_data += 'Q: ' + user_message + '\nA: '

    result = gpt.open_ai_with_info(context_data)
    context_data += result + '\n\n'
    print(context_data)

    # add user message to database
    sql.add_message(email, user_message, datetime.now())
    logger.info('User ' + email + ' asked: ' + user_message)

    # add bot response to database
    sql.add_message(email, result, datetime.now(), True)
    logger.info('Bot responded: ' + result)

    return jsonify({'response': result})

@app.route('/get_messages', methods=['GET', 'POST'])
def get_messages():
    email = request.cookies.get('email')
    messages = sql.get_messages(email)

    if messages is None or len(messages) < 2:
        return jsonify({'messages': ''})
    
    print(messages)
        
    # get 4 last messages into a json object
    msg_result = {}
    for message in range(len(messages)):
        msg_result[str(3 - message)] = messages[str(len(messages) - message - 1)]

    jsonify(msg_result)

    return jsonify({'messages': msg_result})


if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1:5000')

# I bought 200 Apple shares on 12/12/2020, what is my profit?
# I sold 50 Apple shares on 12/12/2021.