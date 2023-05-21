import unittest
import os
from application import app, db
from application.models import user, portfolio, messages
from config import TestingConfig

from datetime import datetime

import sql

class UserModelCase(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()  # create a virtual test environment
        with app.app_context():
            app.config.from_object(TestingConfig)
            db.create_all()  # create tables in the database

            # Update an existing user with the provided email
            user1 = user.query.filter_by(email='test1@mail.com').first()
            user1.user_name = 'user1'
            user1.password = 'password1'
            user1.phone_number = '1234567890'
            user2 = user.query.filter_by(email='test2@mail.com').first()
            user2.user_name = 'user2'
            user2.password = 'password2'
            user2.phone_number = '1234567890'
            user3 = user.query.filter_by(email='test3@mail.com').first()
            user3.user_name = 'user3'
            user3.password = 'password3'
            user3.phone_number = '1234567890'

            

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_user_exists(self):
        with app.app_context():
            u = user.query.filter_by(email='test1@mail.com').first()
            self.assertIsNotNone(u)
            self.assertEqual(u.user_name, 'user1')

    def test_stock_added(self):
        with app.app_context():
            u = user.query.filter_by(email='user1').first()
            stocks = u.portfolio_stocks
            self.assertEqual(len(stocks), 2)

    def test_password_hashing(self):
        password = 'password1'
        u = user.query.filter_by(email='test1@mail.com').first()
        self.assertTrue(u.check_password(password))

    def test_user_login(self):
        response = self.app.post('/login', data=dict(
            email='test1@mail.com',
            password='password1'
        ), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Logged in successfully', response.data)

    def test_user_logout(self):
        response = self.app.get('/logout', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Logged out successfully', response.data)


if __name__ == '__main__':
    unittest.main(verbosity=2)
