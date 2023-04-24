from application import app
from flask import render_template

@app.route("/")
@app.route("/index")
@app.route("/home")
def index():
    return render_template('index.html')

@app.route('/portfolio')
def portfolio():
    return render_template('portfolio.html')

@app.route('/history')
def history():
    return render_template('history.html')

@app.route("/settings")
def settings():
    return render_template('settings.html', menuCss=True)

@app.route('/help')
def help():
    return render_template('help.html')

@app.route('/about-us')
def aboutUs():
    return render_template('about-us.html')

@app.route("/login")
def login():
    return render_template('login.html')

@app.route("/logOut")
def logOut():
    return render_template('signup.html')
