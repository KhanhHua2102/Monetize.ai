from application import app
from flask import render_template

@app.route('/')
@app.route('/AboutUs')
def AboutUs():
    return render_template('AboutUs.html')

@app.route('/HelpCenter')
def HelpCenter():
    return render_template('HelpCenter.html')

@app.route('/History')
def History():
    return render_template('History.html')
@app.route("/")
@app.route("/index")
@app.route("/home")
def index():
    return render_template('chat-screen.html')

@app.route("/portfolio")
def portfolio():
    return render_template('portfolio.html')

# @app.route("/history")
# def history():
#     return render_template('history.html')

# @app.route("/settings")
# def settings():
#     return render_template('settings.html')

# @app.route("/aboutUs")
# def aboutUs():
#     return render_template('aboutUs.html')

# @app.route("/logOut")
# def logOut():
#     return render_template('logOut.html')
