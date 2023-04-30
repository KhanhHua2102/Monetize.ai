from application import app, models
from flask import render_template, redirect, url_for, session, make_response
from datetime import timedelta

from forms import LoginForm, SignupForm
import secrets
import sql

secrets_key = secrets.token_bytes(32)
app.config['SECRET_KEY'] = secrets_key


@app.route("/")
@app.route("/index")
@app.route("/home")
def index():
    if'email' in session:
        return render_template('index.html')
    else:
        return redirect(url_for('login'))

@app.route('/portfolio')
def portfolio():
    myportfolio = models.portfolio.query.order_by(models.portfolio.date_added).all()
    return render_template('portfolio.html', mobileCSS=True, portfolio=myportfolio)

@app.route('/history')
def history():
    return render_template('history.html')

@app.route("/settings")
def settings():
    return render_template('settings.html')

@app.route('/help')
def help():
    return render_template('help.html')

@app.route('/about-us')
def aboutUs():
    return render_template('about-us.html')

@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        session['email'] = form.email.data
        session.permanent = True  # make the session cookie permanent
        app.permanent_session_lifetime = timedelta(days=1)
         # Add the email cookie
        response = make_response(redirect(url_for('index')))
        response.set_cookie('email', form.email.data)
        return response
        
    return render_template('login.html',form=form)

@app.route("/logOut", methods=['GET', 'POST'])
def logOut():
    session.pop('email', None)
    form = LoginForm()
    response = make_response(render_template('login.html',form=form))
    response.delete_cookie('email')
    return response


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        
        return redirect(url_for('login'))
    return render_template('signup.html', form=form)

