from application import app, models
from flask_sqlalchemy import SQLAlchemy
from flask import jsonify
from datetime import datetime
import os

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
    os.path.join(app.root_path+"/../", 'test.db')
models.db.init_app(app)


def get_json_object(key, table, column_list=None):
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
    get_json_object()


def addStock(userId, ticker, vol, price, date):
    pass


def updateStock(user, ticker, vol, price, date):
    pass


def addMessages():
    pass


def commit_database_portfolio(formatted_prompt):
    quantity, stock_type, date_added, price_bought, current_price, return_percent, return_amount, total = formatted_prompt.split(
        " ")
    date_added_format = datetime.strptime(date_added, '%d/%m/20%y').date()
    new_portfolio = models.portfolio1(stock_type=stock_type, date_added=date_added_format, quantity=quantity, price_bought=float(
        price_bought), current_price=float(current_price), return_percent=float(return_percent), return_amount=float(return_amount), total=float(total))
    models.db.session.add(new_portfolio)
    models.db.session.commit()
    models.db.session.close()


with app.app_context():
    models.db.create_all()

