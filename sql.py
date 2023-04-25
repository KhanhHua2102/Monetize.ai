from application import app, models
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask import jsonify
from datetime import datetime
import os

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
    os.path.join(app.root_path+"/../", 'test.db')
models.db.init_app(app)


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


def addUser(userId, email, password):
    getJsonObject()

# add new stock to stock table in database


def addStock(userId, date, ticker, quantity, start_price, current_price, return_percent, return_amount):
    pass

# update stock in stock table in database


def updateStock(userId, ticker, quantity):
    pass

# add new message to message table in database


def addMessages(messageId, userId, message, date):
    pass


def addPortfolio(formatted_prompt):
    [date, ticker, quantity, start_price, current_price,
        return_percent, return_amount, total] = formatted_prompt
    # date_added_format = datetime.strptime(date, '%d/%m/20%y').date()
    new_portfolio = models.portfolio(date_added=date, stock_type=ticker, quantity=quantity, price_bought=float(
        start_price), current_price=float(current_price), return_percent=float(return_percent), return_amount=float(return_amount), total=float(total))
    models.db.session.add(new_portfolio)
    models.db.session.commit()
    models.db.session.close()


with app.app_context():
    models.db.create_all()
