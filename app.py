from application import app,routes,models
from flask import Flask, jsonify, request, redirect,url_for,render_template
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import config
from datetime import datetime
import openai
import os
import yfinance as yf
from dateutil import parser


openai.api_key = config.OPENAI_API_KEY

CORS(app)

context_data = 'You are a friendly financial chatbot. The user will ask you questions, and you will provide polite responses.\n\n'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(app.root_path+"/../", 'test.db')

models.db.init_app(app)

def get_json_object(key,table,column_list=None):
    try:
        get_table = getattr(models,table)
        result = get_table.query.filter_by(id = key).first()
        data = {}
        if column_list is None:
            column_list = get_table.__table__.columns.keys()

        print(type(column_list))
        print(column_list)

        for column in column_list:
            try:
                get_data =  getattr(result, column)
                data[column] = get_data

            except AttributeError:
                return {'error':f"{column} is not a valid column name"}


    except AttributeError:
        return {'error': f"{table} is not a valid table name."}
    return jsonify(data)
    # return jsonify({'response',data})

# add new user to user table in database


def addUser(userId, email, password):
    get_json_object()

def addStock(userId, ticker, vol, price, date):
    pass

def updateStock(user, ticker, vol, price, date):
    pass

def addMessages():
    pass

@app.route('/generate', methods=['POST'])
def generate():
    print("prompt received")
    data = request.get_json()
    prompt = data['prompt']
    print(prompt)

    global context_data
    context_data += 'Q: ' + prompt + '\nA: '

    def openai_completion(query):
        print("Starting GPT-3\n")
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo", messages=[{"role": "user", "content": query}])
        response = completion.choices[0].message.content
        global context_data
        context_data += response + '\n\n'
        return response
    
    def addingstock(thisprompt):
        stock_context = "Based on a user's input, you have to determine if they want to add stocks to their portfolio. Return 'False' if they don't want to add stocks if their input is irrelevant to stocks. You should also return 'False' if their information does include the stock name, date added, the quantity of stock and bought price. Otherwise please return 'True'. For all query strictly return either True or False only and nothing else. The user input is:"
        query = stock_context+'"'+thisprompt+'"'
        response = openai_completion(query)
        if response == "True":
            return True
        return False

    def commit_database_portfolio(formatted_prompt):
        quantity,stock_type,date_added,price_bought,current_price, return_percent,return_amount,total = formatted_prompt.split(" ")
        date_added_format = datetime.strptime(date_added,'%d/%m/20%y').date()
        new_portfolio = models.portfolio1(stock_type=stock_type,date_added=date_added_format,quantity=quantity,price_bought=float(price_bought),current_price=float(current_price),return_percent=float(return_percent),return_amount=float(return_amount),total=float(total))
        models.db.session.add(new_portfolio)
        models.db.session.commit()
        models.db.session.close()


    result = openai_completion(prompt)

    return jsonify({'response': result})

with app.app_context():
    models.db.create_all()

