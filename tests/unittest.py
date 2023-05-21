import unittest
from datetime import datetime

from werkzeug.security import check_password_hash, generate_password_hash

from application import app, db
from application.models import messages, portfolio, user
from config import TestingConfig


class UserModelCase(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()  # create a virtual test environment
        with app.app_context():
            app.config.from_object(TestingConfig)
            db.create_all()  # create tables in the database

            # Add users and stocks to the database for testing
            user1 = user(user_id=1, user_name='user1', email="user1@gmail.com", phone_number="1234567890", password=generate_password_hash("password1"), risk_tolerance="Moderate")
            user2 = user(user_id=2, user_name='user2', email="user2@gmail.com", phone_number="1234567891", password=generate_password_hash("password2"), risk_tolerance="Moderate")
            user3 = user(user_id=3, user_name='user3', email="user3@gmail.com", phone_number="1234567892", password=generate_password_hash("password3"), risk_tolerance="Moderate")
            stock1 = portfolio(id=1, user_id=1, date_added=datetime.now(), ticker='AAPL', quantity=10, price_bought=100, current_price=200, return_percent=100, return_amount=1000, total=2000)
            stock2 = portfolio(id=2, user_id=1, date_added=datetime.now(), ticker='TSLA', quantity=10, price_bought=100, current_price=200, return_percent=100, return_amount=1000, total=2000)
            stock3 = portfolio(id=3, user_id=1, date_added=datetime.now(), ticker='MSFT', quantity=10, price_bought=100, current_price=200, return_percent=100, return_amount=1000, total=2000)

            # Add and commit to the database
            db.session.add(user1)
            db.session.add(user2)
            db.session.add(user3)
            db.session.add(stock1)
            db.session.add(stock2)
            db.session.add(stock3)
            db.session.commit()
            
    # clean up the database after the tests
    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    # Test if the users exist in the database
    def test_user_exists(self):
        with app.app_context():
            user1 = user.query.get(1)
            self.assertIsNotNone(user1)
            self.assertEqual(user1.user_name, 'user1')
            user2 = user.query.get(2)
            self.assertIsNotNone(user2)
            self.assertEqual(user2.user_name, 'user2')
            user3 = user.query.get(3)
            self.assertIsNotNone(user3)
            self.assertEqual(user3.user_name, 'user3')

    # Test if the stocks exist in the database
    def test_stock_exists(self):
        with app.app_context():
            # stocks = portfolio.query.get(1)
            stocks = portfolio.query.filter_by(user_id=1).count()
            self.assertIsNotNone(stocks)
            self.assertEqual(stocks, 3)

    # Test if the password is hashed correctly
    def test_password_added(self):
        with app.app_context():
            u = user.query.get(1)
            password1 = u.password
            self.assertEqual(check_password_hash(password1, "password1"), True)

    # Test if the route to the home page is working
    def test_user_login(self):
        response = self.app.post('/login', data=dict(
            email='test1@mail.com',
            password='password1'
        ), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Go', response.data)
        
    # Test if the route to the logout page is working
    def test_user_logout(self):
        response = self.app.get('/logout', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Enter Your Password', response.data)


if __name__ == '__main__':
    unittest.main(verbosity=2)
