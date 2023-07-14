from flask import jsonify, session

from application import app, models
from application.routes import message_id_exists


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
    raise ValueError("Can not update api key in database")


def update_name(email, new_value):
    user = models.user.query.filter_by(email=email).first()
    if user is not None:
        user.user_name = new_value
        models.db.session.commit()
        models.db.session.close()
        return True
    raise ValueError("Can not update name in database")


def update_email(email, new_value):
    user = models.user.query.filter_by(email=email).first()
    if user is not None:
        # modify email in database
        user.email = new_value
        models.db.session.commit()
        models.db.session.close()
        session['email'] = new_value
        return True
    raise ValueError("Can not update email in database")


def update_phone(email, new_value):
    user = models.user.query.filter_by(email=email).first()
    if user is not None:
        user.phone_number = new_value
        models.db.session.commit()
        models.db.session.close()
        return True
    raise ValueError("Can not update phone in database")


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


# return the results chat conversation for user's search in History page
def chat_data_list(user_chats, search_query):
    return_data = []
    if search_query is None or search_query == "":
        chats_data = user_chats.all()

        for i in range(len(chats_data)):
            chat = chats_data[i]

            if not chat.is_bot and i< len(chats_data)-1:
                next_bot_message = "(No message from bot is stored for this message...)"
                next_message = chats_data[i+1]
                if next_message.is_bot:
                    next_bot_message = next_message.body
                    # i+=1
                if not message_id_exists(return_data,chat.message_id) and not message_id_exists(return_data,next_message.message_id):
                    return_data.append({'created_at': chat.created_at, 'body': chat.body , 'id': chat.message_id})
                    return_data.append({'created_at': next_message.created_at, 'body': next_bot_message , 'id':next_message.message_id})

            elif not chat.is_bot and i>=len(chats_data)-1:
                next_bot_message = "(No message from bot is stored for this message...)"
                if not message_id_exists(return_data,chat.message_id):
                    return_data.append({'created_at': chat.created_at, 'body': chat.body ,'id' : chat.message_id})
                    return_data.append({'created_at': chat.created_at, 'body': next_bot_message,'id':chat.message_id} )

            elif chat.is_bot and i>0:
                prev_user_message = "(No message from user is stored for this message...)"
                prev_message = chats_data[i-1]
                if not prev_message.is_bot:
                    prev_user_message = prev_message.body
                if not message_id_exists(return_data,chat.message_id) and not message_id_exists(return_data,prev_message.message_id):
                    return_data.append({'created_at': chat.created_at, 'body': chat.body , 'id': chat.message_id})
                    return_data.append({'created_at': next_message.created_at, 'body': prev_user_message , 'id':prev_message.message_id})

            elif chat.is_bot and i==0:
                prev_user_message = "(No message from user is stored for this message...)"
                if not message_id_exists(return_data,chat.message_id):
                    return_data.append({'created_at': chat.created_at, 'body': chat.body , 'id': chat.message_id})
                    return_data.append({'created_at': chat.created_at, 'body': prev_user_message , 'id':chat.message_id})

    else:
        filtered_chats = user_chats.filter(models.messages.body.contains(search_query)).all()
        print(filtered_chats)
        list_user_chats = user_chats.all()
        for chat_item in filtered_chats:
            # hi = chat_item.message_id
            for i in range(len(list_user_chats)):
                if list_user_chats[i].message_id == chat_item.message_id:
                    if not list_user_chats[i].is_bot and i < len(list_user_chats)-1:
                        next_bot_message = "(No message from bot is stored for this message...)"
                        next_message = list_user_chats[i+1]
                        if next_message.is_bot:
                            next_bot_message = next_message.body
                            # i+=1
                        if not message_id_exists(return_data,chat_item.message_id) and not message_id_exists(return_data,next_message.message_id):
                            return_data.append({'created_at': chat_item.created_at, 'body': chat_item.body , 'id' : chat_item.message_id})
                            return_data.append({'created_at': next_message.created_at, 'body': next_bot_message , 'id':next_message.message_id})
                    elif not list_user_chats[i].is_bot and i>=len(list_user_chats)-1:
                        next_bot_message = "(No message from bot is stored for this message...)"
                        if not message_id_exists(return_data,chat_item.message_id):
                            return_data.append({'created_at': chat_item.created_at, 'body': chat_item.body , 'id': chat_item.message_id})
                            return_data.append({'created_at': chat.created_at, 'body': next_bot_message , 'id':chat_item.message_id})
                    elif list_user_chats[i].is_bot and i>0:
                        prev_user_message = "(No message from user is stored for this message...)"
                        prev_message = list_user_chats[i-1]
                        if not prev_message.is_bot:
                            prev_user_message = prev_message.body

                        if not message_id_exists(return_data,chat_item.message_id) and not message_id_exists(return_data,prev_message.message_id):
                            return_data.append({'created_at': chat_item.created_at, 'body': prev_user_message , 'id': chat_item.message_id})
                            return_data.append({'created_at': chat_item.created_at, 'body': chat_item.body , 'id': prev_message.message_id})
                    elif chat.is_bot and i==0:
                        prev_user_message = "(No message from user is stored for this message...)"

                        if not message_id_exists(return_data,chat_item.message_id):
                            return_data.append({'created_at': chat_item.created_at, 'body': prev_user_message , 'id': chat_item.message_id})
                            return_data.append({'created_at': chat_item.created_at, 'body': chat_item.body , 'id': chat_item.message_id})

    return return_data
