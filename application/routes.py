from application import app, models
from flask import render_template, redirect, url_for, session, make_response, flash, get_flashed_messages,request,jsonify
from datetime import timedelta
from flask_paginate import Pagination,get_page_args

from forms import LoginForm, SignupForm
import secrets
import bcrypt
from werkzeug.security import generate_password_hash, check_password_hash

from flask import (flash, make_response, redirect, render_template, request,
                   url_for)

import sql
from application import app
from forms import LoginForm, SignupForm

secrets_key = secrets.token_bytes(32)
app.config["SECRET_KEY"] = secrets_key


@app.route("/")
@app.route("/index")
@app.route("/home")
def index():
    if "email" in request.cookies:
        return render_template("index.html")
    else:
        return redirect(url_for("login"))


@app.route("/portfolio")
def portfolio():
    email = request.cookies.get("email")
    user_data = sql.get_user_data(email)[0]
    portfolio = sql.get_stock_data(email)[0]
    return render_template("portfolio.html", mobileCSS=True, user_data=user_data, portfolio=portfolio)


# @app.route('/history')
# def history():
#     # chats_test = models.messages.query.all().paginate(per_page=3)
#     email = request.cookies.get('email')
#     page = request.args.get('page',1,type=int)
#     # mypage_num = int(request.args.get('mypage_num'))

#     if request.args.get('mypage_num') is None:
#         mypage_num = 5
#     else:
#         mypage_num = int(request.args.get('mypage_num'))
#     print(email)
#     user_id = sql.getUserId(email)
#     chats = models.messages.query.filter_by(user_id=user_id)
#     # chats_test = models.messages.query.all().paginate(per_page=3)
#     chats_test = models.messages.query.filter_by(user_id=user_id).paginate(page=page,per_page = mypage_num)

#     print(chats_test.items)
#     return render_template('history.html',chats=chats_test)


@app.route('/history')
def history():
    email = request.cookies.get('email')
    user_id = sql.get_user_id(email)
    search_query = request.args.get('contains')
    chats = models.messages.query.filter_by(user_id=user_id)
    if search_query is None:
        search_query = ""
    if search_query:
        chats = chats.filter(models.messages.body.contains(search_query))


    if search_query:
        chats = chats.filter(models.messages.body.contains(search_query))
    return render_template('history.html',chats=chats)

@app.route('/get_history', methods=['GET']) 
def get_history():
    email = request.cookies.get('email')
    user_id = sql.get_user_id(email)
    search_query = request.args.get('contains')
    chats = models.messages.query.filter_by(user_id=user_id)
    if search_query is None:
        search_query = ""
    if search_query:
        chats = chats.filter(models.messages.body.contains(search_query))


    if search_query:
        chats = chats.filter(models.messages.body.contains(search_query))
    chats_data = [{'created_at': chat.created_at, 'body': chat.body} for chat in chats]
    return jsonify(chats_data)




@app.route("/settings")
def settings():
    email = request.cookies.get("email")
    user_data = sql.get_user_data(email)[0]
    return render_template("settings.html", mobileCSS=False, user_data=user_data)


@app.route("/help")
def help():
    return render_template("help.html", mobileCSS=False)


@app.route("/about-us")
def aboutUs():
    return render_template("about-us.html", mobileCSS=False)


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        user_data = sql.get_user_data(email)
        if not user_data or user_data is None:
            flash("User not found", "error")
            return redirect(url_for("login"))

        if not check_password_hash(user_data[0].password, password):
            flash("Incorrect Password", "error")
            return redirect(url_for("login"))

        # Add the email cookie
        response = make_response(redirect(url_for("index")))
        response.set_cookie("email", email)

        return response

    return render_template("login.html", form=form)


@app.route("/logout", methods=["GET", "POST"])
def logout():
    response = make_response(redirect(url_for("login")))
    response.delete_cookie("email")
    return response


@app.route("/signup", methods=["GET", "POST"])
def signup():
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
            sql.add_user(name, email, hashed_password, phone)
        except ValueError as e:
            error_message = str(e)
            return render_template("signup.html", form=form, error_message=error_message)
        return redirect(url_for("login"))
    return render_template("signup.html", form=form)

# def search():
#     string = request.args.get('contains')

#     if string:
#         chats = models.messages.query.filter(models.messages.body.contains(string))
#     else:
#         chats = models.messages.query.all()
#     return render_template('history.html',chats = chats)



## HASH PASSWORD FUNCTION USING BCRYPT
def hash_password(password):
    password = bytes(password, 'utf-8')
    salt = bytes('$2b$12$kfVMHDkl3udwMUIvngFwI.', 'utf-8')
    hashed = bcrypt.hashpw(password, salt)
    return hashed.decode('utf-8')

