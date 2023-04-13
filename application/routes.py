from application import app
from flask import render_template

@app.route("/")
@app.route("/index")
@app.route("/home")
def index():
    return render_template('chat-screen.html')

@app.route("/portfolio")
def porfolio():
    return render_template('portfolio.html')
