import os

base_dir = os.path.abspath(os.path.dirname(__file__))
FLASK_APP = 'app.py'
DEBUG = True

class Config(object):

    # Enter your Open API Key here
    OPENAI_API_KEY = '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'

    FINNHUB_API_KEY = 'ch4k2vpr01quc2n4rj5gch4k2vpr01quc2n4rj60'

    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(base_dir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class ProductionConfig(Config):
    DEBUG = False


class TestingConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(base_dir, 'test.db')
    