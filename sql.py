from application import app, models
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask import jsonify
from datetime import datetime
import os
from sqlalchemy import ForeignKey
import json

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(app.root_path+"/../", 'test.db')
models.db.init_app(app)

#query to get data from the database
def getJsonObject(key, table, column_list=None):
    try:
        get_table = getattr(models, table)
        result = get_table.query.filter_by(id=key).first()
        data = {}
        if column_list is None:
            column_list = get_table.__table__.columns.keys()

        for column in column_list:
            try:
                get_data = getattr(result, column)
                data[column] = get_data

            except AttributeError:
                return {'error': f"{column} is not a valid column name"}

    except AttributeError:
        return {'error': f"{table} is not a valid table name."}
    return jsonify(data)

# add new user to user table in database
def addUser(user_name, email, password,phone_number):
    if models.user.query.filter_by(email=email).first():
        raise ValueError("User with provided email already exists")
    new_user = models.user(user_name=user_name,email = email,password = password,phone_number = phone_number)
    models.db.session.add(new_user)
    models.db.session.commit()
    models.db.session.close()

# return user data from user table in database as JSON object
def getUserData(email):
    user = models.user.query.filter_by(email=email).first()
    if user:
        user_data = {"user_id":user.user_id ,"user_name":user.user_name ,"email":user.email,"phone_number":user.phone_number,"password":user.password,"risk_tolerence":user.risk_tolerence}
        return jsonify(user_data)
    else:
        return jsonify({'error': 'User not found'})
    
def getUserId(email):
    user = models.user.query.filter_by(email=email).first()
    if user:
        return user.user_id
    else:
        raise ValueError("User Id with email given is not found")
        
def addStock(email, date, ticker, quantity, start_price, current_price, return_percent, return_amount,total):
    userId = getUserId(email)
    
    stock = models.portfolio.query.filter_by(user_id=userId, ticker=ticker).first()
    if stock:
        stock.quantity += quantity
        stock.current_price = current_price
        stock.return_percent = return_percent
        stock.return_amount = return_amount
        stock.total = total
    else:
        new_stock = models.portfolio(user_id=userId, date_added=date, ticker=ticker, quantity=quantity, price_bought=start_price, current_price=current_price, return_percent=return_percent, return_amount=return_amount, total=total)
        models.db.session.add(new_stock)
    models.db.session.commit()
    models.db.session.close()

# update stock in stock table in database, if quantity is 0, delete stock
#add change stock price if have time?
def updateStock(email, ticker, quantity):
    userId = getUserId(email)
    stock = models.portfolio.query.filter_by(user_id=userId, ticker=ticker).first()
    if stock is None:
        raise ValueError("No such stock with this userId and ticker. Should add such a data row first")
    if quantity == 0:
        models.db.session.delete(stock)
    else:
        stock.quantity = quantity
    models.db.session.commit()
    models.db.session.close()

# return stock data from stock table in database as JSON object
def getStockData(email):
    userId = getUserId(email)
    stocks = models.portfolio.query.filter_by(user_id=userId).all()
    if stocks is None:
        return {'error':'No stocks with this user_id yet.'}
    stock_data = {}
    for stock in stocks:
        this_stock_id = str(stock.stock_id)
        stock_data[this_stock_id] = {'user_id': stock.user_id,'date_added': str(stock.date_added),'ticker': stock.ticker,'quantity': stock.quantity,'price_bought': stock.price_bought,'current_price': stock.current_price,'return_percent': stock.return_percent,'return_amount': stock.return_amount,'total': stock.total}
    return stock_data

# return message data from message table in database as JSON object
def getMessages(email):
    userId = getUserId(email)
    messages = models.messages.query.filter_by(user_id = userId).all()
    if messages is None:    
        return {'error':'No messages with this user_id yet.'}
    messages_data = {}
    for message in messages:
        this_message_id = str(message.message_id)
        messages_data[this_message_id] = {'user_id':message.user_id,'body' : message.body,'created_at':message.created_at}
    return messages_data

# add new message to message table in database
def addMessages(messageId, email, message, date):
    userId = getUserId(email)
    existing_message = models.messages.query.filter_by(message_id=messageId).first()
    if existing_message:
        existing_message.body = message
        existing_message.created_at = date
    else:
        new_Message = models.messages(message_id=messageId, user_id=userId, body=message, created_at=date)
        models.db.session.add(new_Message)
    models.db.session.commit()
    models.db.session.close()

with app.app_context():
    models.db.create_all()
