from flask import flash, redirect, render_template, session, url_for
from flask_login import login_user, logout_user
from werkzeug.security import check_password_hash

import sql
from forms import LoginForm


class UserController():

    def login():
        form = LoginForm()
        if form.validate_on_submit():
            email = form.email.data
            password = form.password.data
            user = sql.get_user_data(email)
            if not user or user == (None, None):
                flash("User not found", "error")
                print("User not found")
                return redirect(url_for("login"))
            else:
                if not check_password_hash(user[0].password, password):
                    flash("Incorrect Password", "error")
                    print("Incorrect Password")
                    return redirect(url_for("login"))
                else:
                    print("Login successfully")
                    session['email'] = email
                    login_user(user[0])
                    return render_template("index.html")
        
        return render_template("login.html", form=form)
    

    def logout():
        logout_user()
        return redirect(url_for("login"))