import unittest
from datetime import datetime

from selenium import webdriver
from werkzeug.security import check_password_hash, generate_password_hash

from config import TestingConfig
from application import app, db
from application.models import messages, portfolio, user


class SystemTest(unittest.TestCase):
    driver = None

    def setUp(self):
        self.driver = webdriver.Chrome(executable_path='/Users/khanhhua/Documents/Coding/chromedriver_mac_arm64/chromedriver')
        if not self.driver:
            self.skipTest('Web browser not available')
        else:
            app.config.from_object(TestingConfig)
            with app.app_context():
                db.create_all()
                s1 = user(user_name='Test User', email='test@example.com', password='password', risk_tolerance='Moderate')
                p1 = portfolio(user_id=1, date_added=datetime.now(), ticker='AAPL', quantity=10, price_bought=150.0, current_price=160.0, return_percent=6.67, return_amount=100.0, total=1600.0)
                m1 = messages(user_id=1, body='Hello', created_at=datetime.now(), is_bot=False)
                db.session.add(s1)
                db.session.add(p1)
                db.session.add(m1)
                db.session.commit()
            self.driver.maximize_window()
            self.driver.get('http://localhost:5000/')

    def tearDown(self):
        if self.driver:
            self.driver.close()
            with app.app_context():
                db.session.query(user).delete()
                db.session.query(portfolio).delete()
                db.session.query(messages).delete()
                db.session.commit()
                db.session.remove()

    def test_register(self):
        with app.app_context():
            u = user.query.first()
            self.assertEqual(u.user_name, 'Test User', msg='User exists in db')
        self.driver.get('http://localhost:5000/register')
        self.driver.implicitly_wait(5)

    def test_password_hashing(self):
        password = 'password'
        hashed_password = generate_password_hash(password)
        self.assertTrue(check_password_hash(hashed_password, password), msg='Password hashing and checking successful')


if __name__ == '__main__':
    unittest.main(verbosity=2)
