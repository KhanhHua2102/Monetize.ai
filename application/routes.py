from application import app, models
from flask import render_template, redirect, url_for, session, make_response, flash, get_flashed_messages,request,jsonify
from datetime import timedelta
# from flask_paginate import Pagination,get_page_args

from forms import LoginForm, SignupForm
import secrets
import bcrypt
from werkzeug.security import generate_password_hash, check_password_hash

from flask import (flash, make_response, redirect, render_template, request,
                   url_for)
from werkzeug.security import check_password_hash, generate_password_hash

import sql
from application import app
from forms import LoginForm, SignupForm

secrets_key = secrets.token_bytes(32)
app.config["SECRET_KEY"] = secrets_key


@app.route("/")
@app.route("/index")
@app.route("/home")
def index():
    """
    Renders the index.html template if the user is authenticated, 
    otherwise redirects to the login page.
    """
    if "email" in request.cookies:
        return render_template("index.html")
    else:
        return redirect(url_for("login"))


@app.route("/portfolio")
def portfolio():
    """
    Renders the portfolio.html template and fetches user and stock data 
    to be displayed on the page.
    This page is using the toggle menu.
    """
    email = request.cookies.get("email")
    user_data = sql.get_user_data(email)[0]
    portfolio = sql.get_stock_data(email)[0]
    return render_template("portfolio.html", mobileCSS=True, user_data=user_data, portfolio=portfolio)

def message_id_exists(data,message_id):
    for item in data:
        if item["id"] == message_id:
            return True
    return False


@app.route('/history')
def history():
    email = request.cookies.get('email')
    user_id = sql.get_user_id(email)
    search_query = request.args.get('contains')

    user_chats = models.messages.query.filter_by(user_id=user_id)

    return_data = []
    if search_query is None or search_query == "":
        chats_data = user_chats.all()
        
        for i in range(len(chats_data)):
            chat = chats_data[i]

            if not chat.is_bot and i< len(chats_data)-1:
                next_bot_message = "(No message from bot is stored for this message...)"
                next_message = chats_data[i+1]
                if next_message.is_bot:
                    next_bot_message = next_message.body
                    # i+=1
                if not message_id_exists(return_data,chat.message_id) and not message_id_exists(return_data,next_message.message_id):
                    return_data.append({'created_at': chat.created_at, 'body': chat.body , 'id': chat.message_id})
                    return_data.append({'created_at': next_message.created_at, 'body': next_bot_message , 'id':next_message.message_id})

            elif not chat.is_bot and i>=len(chats_data)-1:
                next_bot_message = "(No message from bot is stored for this message...)"
                if not message_id_exists(return_data,chat.message_id):
                    return_data.append({'created_at': chat.created_at, 'body': chat.body ,'id' : chat.message_id})
                    return_data.append({'created_at': chat.created_at, 'body': next_bot_message,'id':chat.message_id} )

            elif chat.is_bot and i>0:
                prev_user_message = "(No message from user is stored for this message...)"
                prev_message = chats_data[i-1]
                if not prev_message.is_bot:
                    prev_user_message = prev_message.body
                if not message_id_exists(return_data,chat.message_id) and not message_id_exists(return_data,prev_message.message_id):
                    return_data.append({'created_at': chat.created_at, 'body': chat.body , 'id': chat.message_id})
                    return_data.append({'created_at': next_message.created_at, 'body': prev_user_message , 'id':prev_message.message_id})

            elif chat.is_bot and i==0:
                prev_user_message = "(No message from user is stored for this message...)"
                if not message_id_exists(return_data,chat.message_id):
                    return_data.append({'created_at': chat.created_at, 'body': chat.body , 'id': chat.message_id})
                    return_data.append({'created_at': chat.created_at, 'body': prev_user_message , 'id':chat.message_id})


    else:
        filtered_chats = user_chats.filter(models.messages.body.contains(search_query)).all()
        print(filtered_chats)
        list_user_chats = user_chats.all()
        for chat_item in filtered_chats:
            # hi = chat_item.message_id
            for i in range(len(list_user_chats)):
                if list_user_chats[i].message_id == chat_item.message_id:
                    if not list_user_chats[i].is_bot and i < len(list_user_chats)-1:
                        next_bot_message = "(No message from bot is stored for this message...)"
                        next_message = list_user_chats[i+1]
                        if next_message.is_bot:
                            next_bot_message = next_message.body
                            # i+=1
                        if not message_id_exists(return_data,chat_item.message_id) and not message_id_exists(return_data,next_message.message_id): 
                            return_data.append({'created_at': chat_item.created_at, 'body': chat_item.body , 'id' : chat_item.message_id})
                            return_data.append({'created_at': next_message.created_at, 'body': next_bot_message , 'id':next_message.message_id})
                    elif not list_user_chats[i].is_bot and i>=len(list_user_chats)-1:
                        next_bot_message = "(No message from bot is stored for this message...)"
                        if not message_id_exists(return_data,chat_item.message_id):
                            return_data.append({'created_at': chat_item.created_at, 'body': chat_item.body , 'id': chat_item.message_id})
                            return_data.append({'created_at': chat.created_at, 'body': next_bot_message , 'id':chat_item.message_id})
                    elif list_user_chats[i].is_bot and i>0:
                        prev_user_message = "(No message from user is stored for this message...)"
                        prev_message = list_user_chats[i-1]
                        if not prev_message.is_bot:
                            prev_user_message = prev_message.body

                        if not message_id_exists(return_data,chat_item.message_id) and not message_id_exists(return_data,prev_message.message_id):
                            return_data.append({'created_at': chat_item.created_at, 'body': prev_user_message , 'id': chat_item.message_id})
                            return_data.append({'created_at': chat_item.created_at, 'body': chat_item.body , 'id': prev_message.message_id})
                    elif chat.is_bot and i==0:
                        prev_user_message = "(No message from user is stored for this message...)"

                        if not message_id_exists(return_data,chat_item.message_id):
                            return_data.append({'created_at': chat_item.created_at, 'body': prev_user_message , 'id': chat_item.message_id})
                            return_data.append({'created_at': chat_item.created_at, 'body': chat_item.body , 'id': chat_item.message_id})

    return render_template('history.html', chats=return_data,search = True)



# @app.route('/history')
# def history():
#     email = request.cookies.get('email')
#     user_id = sql.get_user_id(email)
#     search_query = request.args.get('contains')
#     all_chats = models.messages.query.filter_by(user_id=user_id)
#     # complete_chat = all_chats.all()
#     # if search_query is None or search_query == "":
#     #     chats_data = [{"created_at": chat.created_at, "body": chat.body} for chat in complete_chat]
#     #     print("hereeee")
#     #     return render_template('history.html', chats=complete_chat , search = False)

#     # for chat in complete_chat:
#     #     print(chat.body)
#     if search_query is not None and search_query != "": 
#         all_chats = all_chats.filter(models.messages.body.contains(search_query))

#         # print(chat.body)
#     chats_data = []
#     complete_chat = all_chats.all()

#     for i in range(len(all_chats.all())):
#         print(complete_chat[i].body)
#     i =0
#     for i in range(len(all_chats.all())):
#         chat = complete_chat[i]
#         print(i)
#         print("This is the chat:")
#         print(chat.body)
    
#         # Check if the current chat is a bot message
#         if not chat.is_bot:
#             # Print the current user message
#             print("User Message:", chat.body,"\n")
#             print(chat.message_id)
            
#             next_bot_message = "(No message from bot is stored for this message...)"
#             # Find the next bot message from the same user
#             # for j in range(i+1, len(complete_chat)):
#             #     next_message = all_chats[j]
#             #     print("Next Message in database: ",next_message)
#             #     # print(next_message)
#             #     if next_message.is_bot:
#             #         # print("Next Bot Message:", next_message.body)
#             #         next_bot_message = next_message.body
#             #         break  # Stop searching for next user message
#             print(i+1)
#             next_message = complete_chat[i+1]
#             print(next_message.body)
#             if next_message.is_bot:
#                 next_bot_message = next_message.body
#                 i+=1
#             print("Response from Bot:", next_bot_message)
#             # print(next_bot_message)
#             chats_data.append({'created_at': chat.created_at, 'body': chat.body})
#             chats_data.append({'created_at': chat.created_at, 'body': next_bot_message})

#         elif chat.is_bot:
#             # Print the current user message
#             print("Bot Message:", chat.body,"\n")

#             previous_user_message = "(No message from user is stored for this response...)"
#             #Find the previous user message from the same user
#             # for j in range(i-1,0,-1):
#             #     previous_message = all_chats[j]
#             #     # print("Previous Message from user : ",previous_message)
#             #     if previous_message.is_bot:
#             #         print("Previous User Message:", previous_message.body)
#             #         previous_user_message = previous_message.body
#             #         break

#             if i != 0:
#                 previous_message = complete_chat[i-1]
#                 if not previous_message.is_bot:
#                     previous_user_message = previous_message.body
            
#             chats_data.append({'created_at': chat.created_at, 'body': previous_user_message})
#             chats_data.append({'created_at': chat.created_at, 'body': chat.body})
#     print(len(chats_data))
#     print(chats_data)
#     return render_template('history.html',chats=chats_data,search = True)

# @app.route('/get_history', methods=['GET']) 
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

    print(chats[-1].body)
    chats_data = [{'created_at': chat.created_at, 'body': chat.body} for chat in chats]


    # image_url = url_for('static', filename='img/line.png')
    return jsonify(chats_data = chats_data)




@app.route("/settings")
def settings():
    """
    Renders the settings.html template and fetches user data to be displayed on the page.
    """
    email = request.cookies.get("email")
    user_data = sql.get_user_data(email)[0]
    return render_template("settings.html", mobileCSS=False, user_data=user_data)


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


@app.route("/login", methods=["GET", "POST"])
def login():
    """
    Renders the login.html template and handles the login form submission.
    On successful login, sets an email cookie and redirects to the index page.
    Password is hashed and checked against the hashed password in the database.
    """
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
    """
    Handles the logout functionality by deleting the email cookie and redirecting to the login page.
    """
    response = make_response(redirect(url_for("login")))
    response.delete_cookie("email")
    return response


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

