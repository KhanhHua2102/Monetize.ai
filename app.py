from application import app
from flask import jsonify, request
from flask_cors import CORS

import gpt
import stock
import sql
import datetime

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
        # add stock to database
        stock_data = promptResult[2]
        email = request.COOKIES.get('email')
        sql.addStock(email, *stock_data[1])
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

    # sql.addMessages(1,"hoanglongn01@gmail.com","hello man",datetime.datetime.now())
    # sql.addMessages(2,"hoanglongn01@gmail.com","another hello",datetime.datetime.now())
    # sql.addMessages(3,"henry@gmail.com","Message 3 from henry",datetime.datetime.now())
    # sql.addMessages(4,"henry@gmail.com","Message 4 from henry",datetime.datetime.now())
    # sql.addMessages(5,"motherfucker123@gmail.com","Message 5 from mother fucker",datetime.datetime.now())
    sql.addMessages(1,"ivan@gmail.com","hello world",datetime.datetime.now())
    sql.addMessages(2,"ivan@gmail.com","hello world2",datetime.datetime.now())
    sql.addMessages(3,"ivan@gmail.com","hello world3",datetime.datetime.now())
    sql.addMessages(4,"ivan@gmail.com","hello world4",datetime.datetime.now())
    sql.addMessages(5,"ivan@gmail.com","hello world5",datetime.datetime.now())
    sql.addMessages(6,"ivan@gmail.com","hello world6",datetime.datetime.now())
    sql.addMessages(7,"ivan@gmail.com","hello world7",datetime.datetime.now())
    sql.addMessages(8,"ivan@gmail.com","hello world8",datetime.datetime.now())
    sql.addMessages(9,"ivan@gmail.com","hello world9",datetime.datetime.now())
    sql.addMessages(10,"ivan@gmail.com","hello world10",datetime.datetime.now())
    sql.addMessages(11,"ivan@gmail.com","hello world11",datetime.datetime.now())
    sql.addMessages(12,"ivan@gmail.com","hello world12",datetime.datetime.now())
    sql.addMessages(13,"dick@gmail.com","hello world13 from dick",datetime.datetime.now())
    sql.addMessages(14,"dick@gmail.com","hello world14 from dick",datetime.datetime.now())
    sql.addMessages(15,"dick@gmail.com","hello world15 from dick",datetime.datetime.now())


    return jsonify({'response': result})
