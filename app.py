import logging
import re
from datetime import datetime

from flask import jsonify, request
from flask_cors import CORS

import gpt
import sql
import datetime

# import json
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

    global context_data
    email = request.cookies.get('email')

    data = request.get_json()
    user_message = data['prompt']
    print("user message received:")
    print(user_message + '\n')

    prompt_recommend = stk.prompt_recomendation(user_message)

    # if user buy stock, we add stock to user's portfolio and reply a bot response with profit information
    if re.search(r'\b(buy|bought|caculate|profit)\b', user_message, re.IGNORECASE):
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
    
    # if user want to rebalance portfolio, we reply a suggestion of rebalance
    elif re.search(r'\b(rebalance|rebalancing)\b', user_message, re.IGNORECASE):
        print("User message contains rebalance or rebalancing keyword\n")
        risk_tolerance = 'moderate'
        context_data += f"Using the user's portfolio above, suggest them a rebalance the quantity of stock base on the {risk_tolerance} risk tolerance using only their current holding stocks. Suggest user the target percentage and details the quantity of buy or sell to achieve that rebalance.\n"
        context_data += 'Q: ' + user_message + '\nA: '
    
    
    # if user want to rebalance portfolio, we reply a suggestion of rebalance
    elif re.search(r'\b(rebalance|rebalancing)\b', user_message, re.IGNORECASE):
        print("User message contains rebalance or rebalancing keyword\n")
        risk_tolerance = 'moderate'
        context_data += f"Using the user's portfolio above, suggest them a rebalance the quantity of stock base on the {risk_tolerance} risk tolerance using only their current holding stocks. Suggest user the target percentage and details the quantity of buy or sell to achieve that rebalance.\n"
        context_data += 'Q: ' + user_message + '\nA: '
    
    # if user ask for stock recommendation, we reply a bot response with stock recommendation
    elif prompt_recommend[1]:
        print("Stock recommendation information detected in context_data\n")
        context_data += 'Q: ' + (prompt_recommend[0]) + '\nA: '

    # user want to change risk tolerance
    elif re.search(r'\b((?!what|[\?\s])risk tolerance)\b', user_message, re.IGNORECASE) and re.search(r'\b(high|aggressive|moderate|medium|low|conservative)\b', user_message, re.IGNORECASE):
        print("User message contains risk tolerance keyword\n")
        if re.search(r'\b(high|aggressive)\b', user_message, re.IGNORECASE):
            print("User message contains high or aggressive keyword\n")
            risk_tolerance = 'High'
        elif re.search(r'\b(moderate|medium)\b', user_message, re.IGNORECASE):
            print("User message contains moderate or medium keyword\n")
            risk_tolerance = 'Moderate'
        elif re.search(r'\b(low|conservative)\b', user_message, re.IGNORECASE):
            print("User message contains low or conservative keyword\n")
            risk_tolerance = 'Low'
        # update user's risk tolerance
        sql.update_risk_tolerance(email, risk_tolerance)
        logger.info('User ' + email + ' changed risk tolerance to ' + risk_tolerance)
        context_data += 'Please confirmed to the user that risk tolerance has been changed for them.\nA: '

    # normal bot reply
    else:
        print("No stock information detected in context_data\n")
        context_data += 'Q: ' + user_message + '\nA: '

    result = gpt.open_ai_with_info(context_data)
    context_data += result + '\n\n'

    # sql.add_message(1,"hoanglongn01@gmail.com","hello man",datetime.datetime.now())
    # sql.add_message(2,"hoanglongn01@gmail.com","another hello",datetime.datetime.now())
    # sql.add_message(3,"henry@gmail.com","Message 3 from henry",datetime.datetime.now())
    # sql.add_message(4,"henry@gmail.com","Message 4 from henry",datetime.datetime.now())
    # sql.add_message(5,"motherfucker123@gmail.com","Message 5 from mother fucker",datetime.datetime.now())
    sql.add_message("new@gmail.com","hello world",datetime.datetime.now())
    sql.add_message("new@gmail.com","hello world2",datetime.datetime.now())
    sql.add_message("new@gmail.com","hello world3",datetime.datetime.now())
    sql.add_message("new@gmail.com","hello world4",datetime.datetime.now())
    sql.add_message("new@gmail.com","hello world5",datetime.datetime.now())
    sql.add_message("new@gmail.com","hello world6",datetime.datetime.now())
    sql.add_message("new@gmail.com","hello world7",datetime.datetime.now())
    sql.add_message("new@gmail.com","hello world8",datetime.datetime.now())
    sql.add_message("new@gmail.com","hello world9",datetime.datetime.now())
    sql.add_message("new@gmail.com","hello world10",datetime.datetime.now())
    sql.add_message("new@gmail.com","hello world11",datetime.datetime.now())
    sql.add_message("new@gmail.com","hello world12",datetime.datetime.now())

    sql.add_message("new@gmail.com","heyy",datetime.datetime.now())
    sql.add_message("new@gmail.com","Hello! How can I assist you today?",datetime.datetime.now(),True)
    sql.add_message("new@gmail.com","I want you to have a look at here",datetime.datetime.now())
    sql.add_message("new@gmail.com","Sure, what would you like me to look at?",datetime.datetime.now(),True)

    sql.add_message("new@gmail.com","can you write me a paragraph on a topic with at least 100 words",datetime.datetime.now())
    sql.add_message("new@gmail.com","Certainly! How about we discuss the importance of financial planning? Financial planning is a crucial aspect of anyone's life, regardless of their income or financial status. It involves setting financial goals, creating a budget, and making investments that align with those goals. By creating a financial plan, individuals can ensure that they are making the most of their money and working towards a secure financial future. One of the key benefits of financial planning is that it allows individuals to prioritize their spending. By creating a budget, individuals can track their expenses and identify areas where they may be overspending. This can help them make adjustments and allocate their money more effectively. Additionally, financial planning can help individuals save for important milestones, such as retirement or a child's education. Another important aspect of financial planning is investing. By making smart investments, individuals can grow their wealth and achieve their financial goals more quickly. However, investing can be complex, and it's important to seek guidance from a financial advisor or do thorough research before making any investment decisions. In conclusion, financial planning is a crucial aspect of anyone's life. By setting financial goals, creating a budget, and making smart investments, individuals can ensure that they are making the most of their money and working towards a secure financial future.",datetime.datetime.now(),True)

    # sql.add_message(13,"dick@gmail.com","hello world13 from dick",datetime.datetime.now())
    # sql.add_message(14,"dick@gmail.com","hello world14 from dick",datetime.datetime.now())
    # sql.add_message(15,"dick@gmail.com","hello world15 from dick",datetime.datetime.now())

    # add user message to database
    # sql.add_message(email, user_message, datetime.now(), False)
    # logger.info('User ' + email + ' asked: ' + user_message)

    # add bot response to database
    # sql.add_message(email, result, datetime.now(), True)
    # logger.info('Bot responded: ' + result)

    return jsonify({'response': result})

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

# @app.route('/get_history')
# def get_history():
#     email = request.cookies.get('email')
#     user_id = sql.get_user_id(email)
#     search_query = request.args.get('contains')
#     chats = models.messages.query.filter_by(user_id=user_id)
#     if search_query is None:
#         search_query = ""
#     if search_query:
#         chats = chats.filter(models.messages.body.contains(search_query))


#     if search_query:
#         chats = chats.filter(models.messages.body.contains(search_query))
#     return jsonify(chats)

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1:5001')