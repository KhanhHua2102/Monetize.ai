import logging
import re
from datetime import datetime

import openai
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
    """Generates a response to a user message from chat screen

    Returns:
        response: The response from the API in JSON format
    """
    try:
        global context_data
        email = request.cookies.get('email')

        data = request.get_json()
        user_message = data['prompt']
        print("user message received:")
        print(user_message + '\n')

        # if user message contains reset, we reset the context
        if re.search(r'reset', user_message, re.IGNORECASE):
            context_data = 'You are a friendly financial chatbot named Monetize.ai. The user will ask you questions, and you will provide polite responses.\n\n'
            return jsonify({'response': "Chatbot's context cleared."})

        # decide which prompt to use based on user message
        with open('prompt.txt', 'r') as prompt:
            prompt_input = prompt.read()
            prompt_output = gpt.open_ai_with_info(prompt_input + user_message, 0)
            print("\nprompt output:", prompt_output + '\n')
            prompt_output = prompt_output.replace(".", "")
            prompt_output = prompt_output.strip().split(' ')
            if prompt_output[0].strip() == 'output:':
                prompt_output = prompt_output[1:]
            case = prompt_output[0].strip()
            print("case:", case + '\n')
            output_data = prompt_output[1:]
            print(output_data)

        # if user buy stock, we add stock to user's portfolio and reply a bot response with profit information
        if case == 'buy':
            print("User message contains buy or bought keyword\n")
            
            prompt_result = stk.prompt_profit(output_data)
            start_date, ticker, quantity, start_price, end_price, return_percent, return_amount, total = prompt_result[1]

            print(start_date, ticker, quantity, start_price, end_price, return_percent, return_amount, total)

            # add or update stock in portfolio
            sql.add_stock(email, start_date, ticker, quantity, start_price,
                            end_price, return_percent, return_amount, total)
            logger.info('User ' + email + ' bought ' + str(quantity) + ' shares of ' + ticker + ' at $' + str(start_price) + ' on ' + start_date.strftime('%d-%m-%Y') + ' endprice: ' + str(end_price) + ' return percent: ' + str(return_percent) + ' return amount: ' + str(return_amount) + ' total: ' + str(total))

            context_data += 'Q: ' + prompt_result[0] + '\nA: '

        # if user sell stock, we update user's portfolio and reply a normal bot response
        elif case == 'sell':
            print("User message contains sell or sold keyword\n")
            
            prompt_result = stk.prompt_profit(output_data)
            start_date, ticker, quantity, start_price, end_price, return_percent, return_amount, total = prompt_result[1]
            
            print(start_date, ticker, quantity, start_price, end_price, return_percent, return_amount, total)
            
            # update stock in portfolio
            if sql.get_stock_data(email) is not None:
                sql.update_stock(email, ticker, (0 - int(quantity)))
                logger.info('User ' + email + ' sold ' + str(quantity) + ' shares of ' + ticker + ' at $' + str(start_price) + ' on ' + start_date.strftime('%d-%m-%Y') + ' endprice: ' + str(end_price) + ' return percent: ' + str(return_percent) + ' return amount: ' + str(return_amount) + ' total: ' + str(total))

            context_data += f'Please confirm to the user that the sell action have been recored in their portfolio.\n{prompt_result[0]}\nQ: {user_message}\nA: '
        
        # if user want to rebalance portfolio, we reply a suggestion of rebalance
        elif case == 'rebalance':
            print("User message contains rebalance or rebalancing keyword\n")
            context_data += f"Using the user's portfolio and risk tolerance above, suggest them a rebalance the quantity of stock base on the risk tolerance using only their current holding stocks. Suggest user the target percentage and details the quantity of buy or sell to achieve that rebalancing.\n"
            context_data += 'Q: ' + user_message + '\nA: '
        
        # if user ask for stock recommendation, we reply a bot response with stock recommendation
        elif case == 'recommendation':
            print("Stock recommendation information detected in context_data\n")
            ticker = output_data[0].strip()
            prompt_recomendation = stk.prompt_recomendation(ticker)
            context_data += 'Q: ' + (prompt_recomendation) + '\nA: '
            print(context_data)

        elif case == 'target':
            print("User message contains price target or target keyword\n")
            price_target = stk.stock_price_target(output_data)
            context_data += f'Using this price target to answer user message: {price_target}\nQ: {user_message}\nA: '
            print(context_data)

        # user want to change risk tolerance
        elif case == 'risk':
            print("User message contains risk tolerance keyword\n")
            risk_tolerance = output_data[0].strip()
            # update user's risk tolerance
            sql.update_risk_tolerance(email, risk_tolerance)
            logger.info('User ' + email + ' changed risk tolerance to ' + risk_tolerance)
            context_data += 'Please confirmed to the user that risk tolerance has been changed for them.\nA: '

        # normal bot reply
        elif case == 'normal':
            print("No stock information detected in context_data\n")
            context_data += 'Q: ' + user_message + '\nA: '
        
        result = gpt.open_ai_with_info(context_data)
        context_data += result + '\n\n'

        # add user message to database
        sql.add_message(email, user_message, datetime.now(), False)
        logger.info('User ' + email + ' asked: ' + user_message)

        # add bot response to database
        sql.add_message(email, result, datetime.now(), True)
        logger.info('Bot responded: ' + result)

        return jsonify({'response': result})

    except openai.error.RateLimitError:
        return jsonify({'response': 'Sorry, chatbot is currently overloaded. Please try again after a few seconds.'})

@app.route('/get_messages', methods=['GET', 'POST'])
def get_messages():
    """Get recent messages from database and return to frontend

    Returns:
        json: recent messages
    """

    email = request.cookies.get('email')
    messages = sql.get_messages(email)[1]
    messages_len = len(messages)

    if messages is None or messages_len < 2:
        return jsonify({'messages': ''})

    if messages[str(messages_len - 1)]['is_bot']:
        messages_len = len(messages)
    else:
        messages_len = len(messages) - 1

    # get 2 last messages into a json object
    msg_result = {}
    msg_result['0'] = messages[str(messages_len - 2)]
    msg_result['1'] = messages[str(messages_len - 1)]

    jsonify(msg_result)

    return jsonify({'messages': msg_result})

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1:5001')