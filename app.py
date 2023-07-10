import datetime
import logging
from datetime import datetime

import openai
from flask import jsonify, request
from flask_cors import CORS

import open_ai_call
import sql
import stock as stk
from application import app

CORS(app)


context_data = 'You are a friendly financial chatbot named Monetize.ai. The user will ask you questions, and you will provide polite responses.\n\n'

# Create a message list to pass into GPT-3
messages = [{}]


def record(role, message):
    """
    Record messages into a global variable

    Args:
        role (string): user or assistant
        message (string): message content
    """
    global messages
    messages.append({"role": role, "content": message})


@app.route('/generate', methods=['POST'])
def generate():
    """
    Generates a response to a user message from chat screen.
    First use davinci_003 text completion model to analyze the user's input, then use the output to decide which case scenario.
    Depend on each case, different processing will be done including calling other APIs for external data.
    These data will be used to make GPT-3.5 chat completion call to generate a response to the user.

    Returns:
        response: The response from the API in JSON format
    """
    try:
        global messages
        email = request.cookies.get('email')

        data = request.get_json()
        user_message = data['prompt']
        print("user message received:")
        print(user_message + '\n')


        # decide which action to use based on user message input
        with open('prompt.txt', 'r') as prompt:
            prompt_input = prompt.read()
            result = open_ai_call.davinci_003(prompt_input + user_message + "\nOutput: |", 0)
            
            output_list = result.split(' ')
            case = output_list[0]
            print("case:", case)
            output_data = output_list[1:]
            print("output data: ", output_data)

        # if user buy stock, we add stock to user's portfolio and reply a bot response with profit information
        if case == 'buy':
            print("User bought stock\n")
            
            prompt_result = stk.prompt_profit(output_data)
            start_date, ticker, quantity, start_price, end_price, return_percent, return_amount, total = prompt_result[1]

            # add or update stock in portfolio
            sql.add_stock(email, start_date, ticker, quantity, start_price,
                            end_price, return_percent, return_amount, total)

            record("user", prompt_result[0])

        # if user sell stock, we update user's portfolio and reply a normal bot response
        elif case == 'sell':
            print("\nUser sold stock\n")
            
            prompt_result = stk.prompt_profit(output_data)
            start_date, ticker, quantity, start_price, end_price, return_percent, return_amount, total = prompt_result[1]
            
            # update stock in portfolio
            if sql.get_stock_data(email) is not None:
                sql.update_stock(email, ticker, (0 - int(quantity)))

            record("user", prompt_result[0])

        # user want to receive portfolio rebalancing suggestion
        elif case == 'rebalance':
            print("\nSuggest user portfolio rebalancing\n")
            query = "Using the my portfolio and risk tolerance above, suggest me a rebalance the quantity of stock base on the risk tolerance using only my current holding stocks. Suggest with the target percentage and details the quantity of buy or sell to achieve that rebalancing."
            
            record("user", query)
        
        # user want to receive stock recommendation
        elif case == 'recommendation':
            print("\nGive user stock recommendations\n")
            ticker = output_data[0].strip()
            prompt_recomendation = stk.prompt_recomendation(ticker)
            
            record("user", prompt_recomendation)

        # user want to know stock target price
        elif case == 'target':
            print("\nGive user stock price target\n")
            ticker = output_data[0].strip()
            price_target = stk.stock_price_target(ticker)
            query = f'This is the up-to-date price target: {price_target} for {ticker}. Using the price target to give me an answer: {user_message}'
            
            record("user", query)

        # user want to change risk tolerance
        elif case == 'risk':
            print("\nChange user's risk tolerance\n")
            risk_tolerance = output_data[0].strip()
            
            # update user's risk tolerance
            sql.update_risk_tolerance(email, risk_tolerance)
            
            record("user", user_message)

        # if user message contains reset, we reset the context
        elif user_message == 'reset':
            print("\nReset chatbot's context\n")
            messages = [{}]
            return jsonify({'response': "Chatbot's context cleared."})

        # user want to reset portfolio
        elif case == 'reset_portfolio':
            print("\nReset user's portfolio\n")
            # reset user's portfolio
            sql.reset_portfolio(email)
            return jsonify({'response': "Your portfolio has been reset."})

        # normal bot reply
        else:
            print("\nReply with normal chatbot response\n")
            record("user", user_message)
        
        result = open_ai_call.gpt_with_info(messages)
        record("assistant", result)

        # add user message to database
        sql.add_message(email, user_message, datetime.now(), False)

        # add bot response to database
        sql.add_message(email, result, datetime.now(), True)

        return jsonify({'response': result})

    except openai.error.RateLimitError:
        return jsonify({'response': 'Sorry, chatbot is currently overloaded. Please try again after a few seconds.'})


@app.route('/get_messages', methods=['GET', 'POST'])
def get_messages():
    """
    Get recent 2 messages from database and return to frontend for display

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


@app.route('/update_openai_key', methods=['POST'])
def update_openai_key():
    """
    Update OpenAI key

    Args:
        key (string): new OpenAI key
    """
    data = request.get_json()

    print(data)

    email = request.cookies.get('email')
    key = data['key']
    print("user key received:")
    print(key + '\n')

    print("updating key\n")
    update_success = open_ai_call.update_openai_key(email, key)
    
    if update_success:
        print("key updated\n")
        return jsonify({'response': 'success'})
    else:
        return jsonify({'response': 'error'})
    

@app.route('/update_field', methods=['POST'])
def update_field():
    data = request.get_json()
    print(data)
    field = data['field']
    new_value = data['newValue']

    try:
        if field == 'name':
            sql.update_name(request.cookies.get('email'), new_value)
        elif field == 'email':
            sql.update_email(request.cookies.get('email'), new_value)
        elif field == 'phone':
            sql.update_phone(request.cookies.get('email'), new_value)
    except:
        print("error in app.py")
        return jsonify({'response': 'error'})

    return jsonify({'response': 'success'})


if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1:5001')