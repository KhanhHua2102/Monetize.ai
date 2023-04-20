from application import app
from flask import render_template


@app.route("/")
@app.route("/index")
@app.route("/home")
def index():
    return render_template('index.html', index=True)


@app.route('/aboutUs')
def aboutUs():
    return render_template('about-us.html', index=True)


@app.route('/helpCenter')
def helpCenter():
    return render_template('help-center.html', index=True)


@app.route('/history')
def history():
    return render_template('history.html', index=True)


@app.route("/portfolio")
def portfolio():
    return render_template('portfolio.html')


# @app.route("/settings")
# def settings():
#     return render_template('settings.html')

# @app.route("/logOut")
# def logOut():
#     return render_template('logOut.html')
