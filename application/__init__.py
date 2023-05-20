from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from config import Config

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)

from application import models, routes