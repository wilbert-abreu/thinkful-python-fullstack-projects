from flask import render_template, flash, request, redirect, url_for
from slack_clone import app
from .models import session, User, File, Channel
from flask_login import login_required, current_user, login_user, logout_user
from werkzeug.security import check_password_hash, generate_password_hash


@app.route("/")
def homepage():
    return render_template("base.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        user = session.query(User).filter_by(email=email).first()
        if not user or not check_password_hash(user.password, password):
            flash("incorrect username or password", "danger")
            return render_template("failure.html")
        login_user(user, remember=True)
        return render_template("success.html")
    else:
        return render_template("login.html")


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return render_template("login.html")


@app.route("/create-account", methods=["GET", "POST"])
def create_account():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        display_name = request.form["display_name"]
        password = request.form["password"]
        confirm_password = request.form["confirm_password"]

        if session.query(User).filter_by(email=email).first():
            flash ("There is already a registered user with that email",
                   "danger")
            return redirect(url_for("create_account"))

        while len(password) < 8:
            flash("Please make the password at least 8 charecters long",
                  "danger")
            return redirect(url_for("create_account"))

        while password != confirm_password:
            flash("Passwords do not match", "danger")
            return redirect(url_for("create_account"))

        user = User(name=name,email=email,display_name=display_name,
                    password=generate_password_hash(password))

        session.add(user)
        session.commit()
        login_user(user, remember=True)
        return render_template("success.html")

    else:
        return render_template("create_account.html")



