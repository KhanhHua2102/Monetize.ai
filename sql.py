from application import app, models
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask import jsonify
from datetime import datetime
import os
from sqlalchemy import ForeignKey

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

        print(type(column_list))
        print(column_list)

        for column in column_list:
            try:
                get_data = getattr(result, column)
                data[column] = get_data

            except AttributeError:
                return {'error': f"{column} is not a valid column name"}

    except AttributeError:
        return {'error': f"{table} is not a valid table name."}
    return jsonify(data)
    # return jsonify({'response',data})

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
        user_data = {"user_id":user.user_id ,"user_name":user.user_name ,"email":user.email,"phone_number":user.phonenumber,"password":user.password,"risk_tolerence":user.risk_tolerence}
        return jsonify(user_data)
    else:
        return jsonify({'error': 'User not found'})

#haven't added the check whether the stock already exist or not
def addStock(userId, date, ticker, quantity, start_price, current_price, return_percent, return_amount,total):
    new_Stock = models.user(user_id = userId,date_added = date, ticker = ticker,quantity = quantity, price_bought = start_price,current_price = current_price, return_percent = return_percent ,return_amount = return_amount,total = total)
    models.db.session.add(new_Stock)
    models.db.session.commit()
    models.db.session.close()

# update stock in stock table in database, if quantity is 0, delete stock
#haven't debugged
def updateStock(userId, ticker, quantity):
    stock = models.portfolio.query.filter_by(user_id=userId, ticker=ticker).first()
    if stock is None:
        return {'error':'No such stock with this userId and ticker. Should add such a data row first'}
    if quantity == 0:
        models.db.session.delete(stock)
    else:
        stock.quantity = quantity
    models.db.session.commit()

# return stock data from stock table in database as JSON object
#haven't debugged
def getStockData(user_id):
    stocks = models.portfolio.query.filter_by(user_id=user_id).all()
    stock_data = {}
    for stock in stocks:
        this_stock_id = str(stock.stock_id)
        stock_data[this_stock_id] = {'user_id': stock.user_id,'date_added': str(stock.date_added),'ticker': stock.ticker,'quantity': stock.quantity,'price_bought': stock.price_bought,'current_price': stock.current_price,'return_percent': stock.return_percent,'return_amount': stock.return_amount,'total': stock.total}
    return stock_data

# return message data from message table in database as JSON object
#haven't debugged
def getMessages(user_id):
    messages = models.messages.query.filter_by(user_id = user_id).all()
    messages_data = {}
    for message in messages:
        this_message_id = str(message.message_id)
        messages_data[this_message_id] = {'user_id':message.user_id,'body' : message.body,'created_at':message.created_at}
    return messages_data

# add new message to message table in database
#haven't debugged
def addMessages(messageId, userId, message, date):
    new_Message = models.messages(message_id = messageId,user_id = userId,body = message, created_at = date)
    models.db.session.add(new_Message)
    models.db.session.commit()
    models.db.session.close()


#replaced by addStock
# def addPortfolio(formatted_prompt):
#     [date, ticker, quantity, start_price, current_price,return_percent, return_amount, total] = formatted_prompt
#     # date_added_format = datetime.strptime(date, '%d/%m/20%y').date()
#     new_portfolio = models.portfolio(date_added=date, stock_type=ticker, quantity=quantity, price_bought=float(start_price), current_price=float(current_price), return_percent=float(return_percent), return_amount=float(return_amount), total=float(total))
#     models.db.session.add(new_portfolio)
#     models.db.session.commit()
#     models.db.session.close()


with app.app_context():
    models.db.create_all()
