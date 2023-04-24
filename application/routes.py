from application import app,models
from flask import render_template
# from app import portfolio1


@app.route("/")
@app.route("/index")
@app.route("/home")
def index():
    return render_template('index.html')

@app.route("/portfolio")
def portfolio():
    return render_template('portfolio.html', menuCss=True)

@app.route('/history')
def history():
    return render_template('history.html')


@app.route("/portfolio",methods = ['GET'])
def portfolio():
    myportfolio = models.portfolio1.query.order_by(models.portfolio1.date_added).all()
    return render_template('portfolio.html',myportfolio=myportfolio)

# myportfolio = portfolio1.query.order_by(portfolio1.date_added).all()

# @app.route("/settings")
# def settings():
#     return render_template('settings.html')

@app.route('/aboutUs')
def aboutUs():
    return render_template('about-us.html')

@app.route('/help')
def help():
    return render_template('help.html')

# @app.route("/logOut")
# def logOut():
#     return render_template('logOut.html')
