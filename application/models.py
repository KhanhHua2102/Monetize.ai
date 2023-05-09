from application import app
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime
from sqlalchemy import ForeignKey

db = SQLAlchemy()

# Initialize Flask-Migrate
migrate = Migrate(app, db)

class portfolio(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer,db.ForeignKey('user.user_id'),nullable = False)
    date_added = db.Column(db.DateTime, nullable=False)
    ticker = db.Column(db.String(10), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price_bought = db.Column(db.Float, nullable=False)
    current_price = db.Column(db.Float, nullable=False)
    return_percent = db.Column(db.Float, nullable=False)
    return_amount = db.Column(db.Float, nullable=False)
    total = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return '<portfolio %r>' % self.id
    
class user(db.Model):
    __tablename__ = 'user'
    user_id = db.Column(db.Integer,primary_key = True)
    user_name = db.Column(db.String(100),nullable = False)
    email = db.Column(db.String(10),nullable = False)
    phone_number = db.Column(db.Unicode(255))
    password = db.Column(db.String(20),nullable = False)
    risk_tolerence = db.Column(db.String(10),default = "Medium")

    def __repr__(self):
        return '<user %r>' % self.user_id
    
class messages(db.Model):
    message_id = db.Column(db.Integer,primary_key = True)
    user_id = db.Column(db.Integer,db.ForeignKey('user.user_id'),nullable = False)
    body = db.Column(db.Text,nullable = False)
    created_at = db.Column(db.DateTime,nullable =False)

    def __repr__(self):
        return '<messages %r>' % self.message_id


