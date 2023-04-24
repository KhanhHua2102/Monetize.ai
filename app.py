from application import app,routes
from flask import Flask, jsonify, request, redirect,url_for,render_template
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import config
from datetime import datetime
import openai
import os
import yfinance as yf
from dateutil import parser
from application import models


openai.api_key = config.OPENAI_API_KEY

CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(app.root_path+"/../", 'test.db')

models.db.init_app(app)

@app.route('/generate', methods=['POST'])
def generate():
    print("prompt received")
    data = request.get_json()
    prompt = data['prompt']
    print(prompt)

    def openai_completion(query):
        print("Starting GPT-3\n")
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo", messages=[{"role": "user", "content": query}])
        response = completion.choices[0].message.content
        print("GPT-3 response: " + response)
        return response
    
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




