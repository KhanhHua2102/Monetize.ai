from flask import jsonify, make_response, render_template, redirect, url_for

from application import app, models


# query to get data from the database
def get_json_object(key, table, column_list=None):
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
def add_user(user_name, email, password, phone_number):
    if models.user.query.filter_by(email=email).first():
        raise ValueError("User with provided email already exists")
    new_user = models.user(user_name=user_name, email=email,
                           password=password, phone_number=phone_number, risk_tolerance='Moderate')
    models.db.session.add(new_user)
    models.db.session.commit()
    models.db.session.close()


# return user data from user table in database as JSON object
def get_user_data(email):
    user = models.user.query.filter_by(email=email).first()
    if user is not None:
        return user, [user.user_name, user.email, user.phone_number, user.risk_tolerance]
    return None, None


# check if user has an API key
def check_api_key(email):
    user = models.user.query.filter_by(email=email).first()
    if user is not None:
        print(user.openai_key)
        return user.openai_key is not None
    

# update user's API key
def update_api_key(email, key):
    user = models.user.query.filter_by(email=email).first()
    if user is not None:
        user.openai_key = key
        models.db.session.commit()
        models.db.session.close()
        return True
    return False


def update_name(email, new_value):
    user = models.user.query.filter_by(email=email).first()
    if user is not None:
        user.user_name = new_value
        models.db.session.commit()
        models.db.session.close()
        return True
    return False


def update_email(email, new_value):
    user = models.user.query.filter_by(email=email).first()
    if user is not None:
        # modify email in database
        user.email = new_value
        models.db.session.commit()
        models.db.session.close()

        # modify email cookie in browser
        response = make_response(render_template("settings.html"))
        response.delete_cookie(key='email')
        response.set_cookie(key="email", value=new_value)
        print("cookie changed")
        return response

    return False


def update_phone(email, new_value):
    user = models.user.query.filter_by(email=email).first()
    if user is not None:
        user.phone_number = new_value
        models.db.session.commit()
        models.db.session.close()
        return True
    return False


# check if user has enough queries left
def check_query_count(email):
    user = models.user.query.filter_by(email=email).first()
    if user is not None:
        return user.query_count > 0
    return False


# reduce user's query count by 1
def reduce_query_count(email):
    user = models.user.query.filter_by(email=email).first()
    if user is not None:
        user.query_count -= 1
        models.db.session.commit()
        models.db.session.close()
        return True
    return False


# get user's ID
def get_user_id(email):
    user = models.user.query.filter_by(email=email).first()
    if user:
        return user.user_id
    else:
        return None


# add new stock record to portfolio table
def add_stock(email, date, ticker, quantity, start_price, current_price, return_percent, return_amount, total):
    user_id = get_user_id(email)

    quantity = float(quantity)
    start_price = float(start_price)
    current_price = float(current_price)
    return_percent = float(return_percent)
    return_amount = float(return_amount)
    total = float(total)

    stock = models.portfolio.query.filter_by(
        user_id=user_id, ticker=ticker, date_added=date).first()
    if stock:
        stock.quantity += quantity
        stock.current_price = current_price
        stock.return_percent = return_percent
        stock.return_amount = return_amount
        stock.total = total
    else:
        new_stock = models.portfolio(user_id=user_id, date_added=date, ticker=ticker, quantity=quantity, price_bought=start_price,
                                     current_price=current_price, return_percent=return_percent, return_amount=return_amount, total=total)
        models.db.session.add(new_stock)
    models.db.session.commit()
    models.db.session.close()


# update stock in stock table in database, if quantity is 0, delete stock
# add change stock price if have time?
def update_stock(email, ticker, quantity):
    user_id = get_user_id(email)
    stock = models.portfolio.query.filter_by(
        user_id=user_id, ticker=ticker).first()
    if stock is None:
        raise ValueError(
            "No such stock with this userId and ticker. Should add such a data row first")
    if quantity == 0:
        models.db.session.delete(stock)
    else:
        stock.quantity = str(int(stock.quantity) + int(quantity))
    models.db.session.commit()
    models.db.session.close()


# reset stock table in database
def reset_portfolio(email):
    user_id = get_user_id(email)
    stocks = models.portfolio.query.filter_by(user_id=user_id).all()
    for stock in stocks:
        models.db.session.delete(stock)
    models.db.session.commit()
    models.db.session.close()


# return stock data from stock table in database as JSON object
def get_stock_data(email):
    user_id = get_user_id(email)
    stocks = models.portfolio.query.filter_by(user_id=user_id).order_by(models.portfolio.date_added).all()

    if stocks is None:
        return None
    
    stock_data = []
    for stock in stocks:
        stock_data.append([stock.date_added.strftime('%d-%m-%Y'), stock.ticker, stock.quantity, stock.price_bought, stock.current_price, stock.return_percent, stock.return_amount, stock.total])

    return stocks, stock_data


# return message data from message table in database as JSON object
def get_messages(email):
    user_id = get_user_id(email)
    messages = models.messages.query.filter_by(user_id=user_id).all()
    
    if messages is None:
        return {'error': 'No messages with this user_id yet.'}
    
    messages_data = {}
    idx = 0
    for message in messages:
        # this_message_id = str(message.message_id)
        messages_data[str(idx)] = {'body': message.body, 'created_at': message.created_at, 'is_bot': message.is_bot}
        idx +=1
    
    return messages, messages_data


# add new message to message table in database
def add_message(email, message, date, is_bot=False):
    user_id = get_user_id(email)
    existing_message = models.messages.query.filter_by(
        user_id=user_id, body=message).first()
    if not existing_message:
        print(message)
        new_message = models.messages(user_id=user_id, body=message, created_at=date, is_bot=is_bot)
        models.db.session.add(new_message)
    models.db.session.commit()
    models.db.session.close()


# update user's risk tolerance in user table in database
def update_risk_tolerance(email, risk_tolerance):
    user_id = get_user_id(email)
    user = models.user.query.filter_by(user_id=user_id).first()
    if user is None:
        raise ValueError("No such user with this userId. Should add such a data row first")
    user.risk_tolerance = risk_tolerance
    models.db.session.commit()
    models.db.session.close()

with app.app_context():
    models.db.create_all()
