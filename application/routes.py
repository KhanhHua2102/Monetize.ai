from application import app
from flask import render_template

@app.route("/")
@app.route("/index")
def index():
    return "<h1>hello world</h1>"

