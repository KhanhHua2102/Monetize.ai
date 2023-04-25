from application import app
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime

db = SQLAlchemy()

# Initialize Flask-Migrate
migrate = Migrate(app, db)

class chat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    prompt = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    response = db.Column(db.String(400), nullable=False)

    def __repr__(self):
        return '<chat %r>' % self.id


class portfolio(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_added = db.Column(db.DateTime, nullable=False)
    stock_type = db.Column(db.String(10), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price_bought = db.Column(db.Float, nullable=False)
    current_price = db.Column(db.Float, nullable=False)
    return_percent = db.Column(db.Float, nullable=False)
    return_amount = db.Column(db.Float, nullable=False)
    total = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return '<portfolio %r>' % self.id
