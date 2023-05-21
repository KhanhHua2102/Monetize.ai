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
        # Set up the Selenium WebDriver
        self.driver = webdriver.Chrome(executable_path='/Users/khanhhua/Documents/Coding/chromedriver_mac_arm64/chromedriver')
        if not self.driver:
            self.skipTest('Web browser not available')
        else:
            # Configure the application with the testing configuration
            app.config.from_object(TestingConfig)
            with app.app_context():
                # Create the database tables
                db.create_all()
                # Add test data to the database
                s1 = user(user_name='Test User', email='test@example.com', password='password', risk_tolerance='Moderate')
                p1 = portfolio(user_id=1, date_added=datetime.now(), ticker='AAPL', quantity=10, price_bought=150.0, current_price=160.0, return_percent=6.67, return_amount=100.0, total=1600.0)
                m1 = messages(user_id=1, body='Hello', created_at=datetime.now(), is_bot=False)
                db.session.add(s1)
                db.session.add(p1)
                db.session.add(m1)
                db.session.commit()
            # Maximize the browser window and open the application URL
            self.driver.maximize_window()
            self.driver.get('http://localhost:5000/')

    def tearDown(self):
        if self.driver:
            # Close the Selenium WebDriver
            self.driver.close()
            with app.app_context():
                # Delete the test data from the database
                db.session.query(user).delete()
                db.session.query(portfolio).delete()
                db.session.query(messages).delete()
                db.session.commit()
                db.session.remove()

    def test_register(self):
        with app.app_context():
            # Retrieve the first user from the database
            u = user.query.first()
            # Assert that the user's username is 'Test User'
            self.assertEqual(u.user_name, 'Test User', msg='User exists in db')
        # Navigate to the registration page using the Selenium WebDriver
        self.driver.get('http://localhost:5000/register')
        self.driver.implicitly_wait(5)

    def test_password_hashing(self):
        # Define a plain-text password
        password = 'password'
        # Generate a hashed password
        hashed_password = generate_password_hash(password)
        # Assert that the hashed password matches the plain-text password when checked
        self.assertTrue(check_password_hash(hashed_password, password), msg='Password hashing and checking successful')


if __name__ == '__main__':
    # Execute the test suite
    unittest.main(verbosity=2)

