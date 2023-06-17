import os

base_dir = os.path.abspath(os.path.dirname(__file__))
FLASK_APP = 'app.py'
DEBUG = True

class Config(object):

    # Enter your Open API Key here
    OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]

    FINNHUB_API_KEY = os.environ["FINNHUB_API_KEY"]

    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(base_dir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class ProductionConfig(Config):
    DEBUG = False


class TestingConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(base_dir, 'test.db')
    