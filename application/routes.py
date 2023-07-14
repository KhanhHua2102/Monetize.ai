import secrets

from flask import redirect, render_template, request, session, url_for
from flask_login import current_user, login_required
from werkzeug.security import generate_password_hash

import sql
from application import app, models
from application.UserController import UserController
from forms import SignupForm

secrets_key = secrets.token_bytes(32)
app.config["SECRET_KEY"] = secrets_key


@app.route("/")
@app.route("/index")
@app.route("/home")
@login_required
def index():
    """
    Renders the index.html template if the user is authenticated, 
    otherwise redirects to the login page.
    """
    return render_template("index.html")
    

@app.route("/login", methods=["GET", "POST"])
def login():
    """
    Renders the login.html template and handles the login form submission.
    On successful login, sets an email in flask session and redirects to the index page.
    Password is hashed and checked against the hashed password in the database.
    """
    if not current_user.is_authenticated:
        return UserController.login()
    return render_template("index.html")


@app.route("/logout", methods=["GET", "POST"])
def logout():
    """
    Handles the logout functionality and redirecting to the login page.
    """
    return UserController.logout()


@app.route("/signup", methods=["GET", "POST"])
def signup():
    """
    Renders the signup.html template and handles the signup form submission.
    On successful signup, adds the user to the database (password is hashed before storing) and redirects to the login page.
    """
    form = SignupForm()
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        phone = form.phone.data 
        password = form.password.data
        
        ## HASH PASSWORD
        hashed_password = generate_password_hash(password)

        try:
            sql.add_user(name, email, hashed_password, phone)
        except ValueError as e:
            error_message = str(e)
            return render_template("signup.html", form=form, error_message=error_message)
        return redirect(url_for("login"))
    return render_template("signup.html", form=form)


@app.route("/portfolio")
@login_required
def portfolio():
    """
    Renders the portfolio.html template and fetches user and stock data 
    to be displayed on the page.
    This page is using the toggle menu.
    """
    email = session.get('email')
    user_data = sql.get_user_data(email)[0]
    
    stock_data = sql.get_stock_data(email)
    if stock_data is not None:
        portfolio = stock_data[0]

    if user_data is not None and portfolio is not None:
        return render_template("portfolio.html", mobileCSS=True, user_data=user_data, portfolio=portfolio)
    else:
        return render_template("portfolio.html", mobileCSS=True,user_data = "" , portfolio = "")

def message_id_exists(data,message_id):
    for item in data:
        if item["id"] == message_id:
            return True
    return False


@app.route('/history')
@login_required
def history():
    """
    renders the history.html template. either displays all messages or only messages that contain a search query. 
    transform into appropriate format list to give to frontend to display.
    """ 
    email = session.get('email')
    user_id = sql.get_user_id(email)
    
    search_query = request.args.get('contains')
    user_chats = models.messages.query.filter_by(user_id=user_id)

    return_data = sql.chat_data_list(user_chats, search_query)

    return render_template('history.html', chats=return_data, search=True)


@app.route("/settings")
@login_required
def settings():
    """
    Renders the settings.html template and fetches user data to be displayed on the page.
    """
    email = session.get('email')
    user_data = sql.get_user_data(email)[0]

    if user_data is not None:
        return render_template("settings.html", mobileCSS=False, user_data=user_data)
    
    return render_template("settings.html", mobileCSS=False, user_data = "")


@app.route("/help")
def help():
    """
    Renders the help.html template.
    """
    return render_template("help.html", mobileCSS=False)


@app.route("/about-us")
def aboutUs():
    """
    Renders the about-us.html template.
    """
    return render_template("about-us.html", mobileCSS=False)

