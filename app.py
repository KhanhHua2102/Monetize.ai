from application import app
from flask import jsonify, request
from flask_cors import CORS

import gpt
import stock
import sql
# import datetime
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
    # perform a specific action for when stock information is present
    if promptResult[1]:
        print("Stock information detected in context_data. Performing specific action...\n")
        context_data += 'Q: ' + promptResult[0] + '\nA: '
    # normal bot reply
    else:
        print("No stock information detected in context_data.\n")
        context_data += 'Q: ' + userMessage + '\nA: '

    result = gpt.openAi(context_data)
    context_data += result + '\n\n'
    print(context_data)

    #some testing done for database function, usage can be referenced from here in case of use
    print("debuggggggg")
    try:
        sql.addUser("Ivan","ivan@gmail.com","ivan123","04123")
        # sql.addUser("Henry","henry@gmail.com","henry123","04124")
        # sql.addUser("Long","long@gmail.com","long123","04125")
    except ValueError:
        print("The user with this email already exists. Please try logging in")
    # test = sql.getUserData("ivan@gmail.com").json
    # def addStock(userId, date, ticker, quantity, start_price, current_price, return_percent, return_amount,total):
    # sql.addStock(1, datetime.datetime(2022, 5, 1, 10, 30, 0), 'AAPL', 100, 150.0, 155.0, 3.33, 500.0, 15500.0)
    # sql.addStock(1, datetime.datetime(2022, 5, 1, 10, 35, 0), 'AAPL', 1000, 150.0, 160.0, 33.33, 5000.0, 155000.0)
    # sql.addStock(2, datetime.datetime(2022, 5, 1, 11, 30, 0), 'AAPL', 100, 150.0, 155.0, 3.33, 500.0, 15500.0)

    # def updateStock(userId, ticker, quantity):
    # sql.updateStock(2,"AAPL",1000)
    # sql.updateStock(2,"AAPL",0)

    # getstock = sql.getStockData(1)
    # print(type(getstock))
    # print(getstock)

    # sql.addMessages(1, 1, "Hello world", datetime.datetime(2022, 5, 1))
    # sql.addMessages(2, 1, "No net external force?", datetime.datetime(2022, 5, 2))
    # sql.addMessages(3, 2, "F=ma!", datetime.datetime(2022, 5, 3))
    # sql.addMessages(4, 3, "Python is a snake", datetime.datetime(2022, 5, 4))

    # sql.addMessages(2, 1, "No net external force? Action and reaction force", datetime.datetime(2022, 5, 3))
    # mymessages = sql.getMessages(1)


    print("debuggggg")
    return jsonify({'response': result})
