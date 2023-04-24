from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class chat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    prompt = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    response = db.Column(db.String(400), nullable=False)

    def __repr__(self):
        return '<chat %r>' % self.id
    
class portfolio1(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    stock_type = db.Column(db.String(10),nullable=False)
    date_added = db.Column(db.DateTime,nullable=False)
    current_date = db.Column(db.DateTime,default = datetime.utcnow)
    quantity = db.Column(db.Integer,nullable=False)
    price_bought = db.Column(db.Float,nullable=False)
    current_price = db.Column(db.Float,nullable=False)
    return_percent = db.Column(db.Float,nullable=False)
    return_amount = db.Column(db.Float,nullable=False)
    total = db.Column(db.Float,nullable=False)

    def __repr__(self):
        return '<portfolio %r>' % self.id