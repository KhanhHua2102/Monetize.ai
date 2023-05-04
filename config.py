import os

base_dir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(base_dir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

# Enter your Open API Key here
OPENAI_API_KEY = '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'
FLASK_APP = 'app.py'
DEBUG = True


    