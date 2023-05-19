import unittest, os
from application import app, db
from application.models import user, portfolio, messages

import sql

class UserModelCase(unittest.TestCase):

    def setUp(self):
        basedir = os.path.abspath(os.path.dirname(__file__))
        app.config['SQLALCHEMY_DATABASE_URI'] = \
            'sqlite:///' + os.path.join(basedir, 'test.db')
        self.app = app.test_client() # create a virtual test environment
        db.create_all() # create tables in the database

        user1 = sql.add_user(user_name='user1', email='test1@mail.com', password='password1', phone_number='1234567890')
        user2 = sql.add_user(user_name='user2', email='test2@mail.com', password='password2', phone_number='1234567890')
        user3 = sql.add_user(user_name='user3', email='test3@mail.com', password='password3', phone_number='1234567890')

        stock1_user1 = sql.add_stock(email='user1', date='2020-01-01', ticker='AAPL', quantity=10, start_price=100, current_price=200, return_percent=100, return_amount=1000, total=2000)
        stock2_user1 = sql.add_stock(email='user1', date='2020-01-01', ticker='TSLA', quantity=10, start_price=100, current_price=200, return_percent=100, return_amount=1000, total=2000)

        db.session.add(user1)
        db.session.add(user2)
        db.session.add(user3)
        db.session.add(stock1_user1)
        db.session.add(stock2_user1)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        

if __name__ == '__main__':
    unittest.main(verbosity=2)