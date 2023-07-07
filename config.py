import os
from boto.s3.connection import S3Connection

base_dir = os.path.abspath(os.path.dirname(__file__))
FLASK_APP = 'app.py'
DEBUG = True

class Config(object):

    # Enter your Open API Key here
    OPENAI_API_KEY = os.environ.get(("OPENAI_API_KEY"))
    # FINNHUB_API_KEY = os.environ["FINNHUB_API_KEY"]
    FINNHUB_API_KEY = os.environ.get(("FINNHUB_API_KEY"))


    # OPENAI_API_KEY = os.getenv("OPEN_AI_key")
    # FINNHUB_API_KEY = os.getenv("FINNHUB_API_KEY")

    # S3 = S3Connection(os.environ['OPEN_AI_key'], os.environ['FINNHUB_API_KEY'])
    # OPENAI_API_KEY = S3.get_bucket('OPEN_AI_key')
    # FINNHUB_API_KEY = S3.get_bucket('FINNHUB_API_KEY')

    # FINNHUB_API_KEY = 'ch4k2vpr01quc2n4rj5gch4k2vpr01quc2n4rj60'

    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(base_dir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class ProductionConfig(Config):
    DEBUG = False


class TestingConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(base_dir, 'test.db')
