from flask import render_template, flash, request, Response, redirect, url_for
from slack_clone import app
from .models import session, User, File, Channel, Message
from flask_login import login_required, current_user, login_user, logout_user
from werkzeug.security import check_password_hash, generate_password_hash
from pusher import Pusher
from . import decorators
import datetime
import json


pusher = Pusher(
  app_id='173573',
  key='b568462b35424532aa89',
  secret='37566de4aecc1f1b312c'
)


@app.route("/")
def homepage():
    if current_user.is_authenticated:
        return render_template("chatroom.html")
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
        return render_template("chatroom.html")
    else:
        return render_template("login.html")


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('homepage'))


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
            flash("Please make the password at least 8 characters long",
                  "danger")
            return redirect(url_for("create_account"))

        while password != confirm_password:
            flash("Passwords do not match", "danger")
            return redirect(url_for("create_account"))

        user = User(name=name, email=email, display_name=display_name,
                    password=generate_password_hash(password))

        session.add(user)
        session.commit()
        login_user(user, remember=True)
        return render_template("chatroom.html")

    else:
        return render_template("create_account.html")


@app.route("/messages", methods=["GET", "POST"])
@decorators.accept("application/json")
@login_required
def chatroom():
    if request.method == "POST":
        message = request.form["message"]
        channel_name = request.form["current-channel"]
        username = current_user.display_name
        time_stamp = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
        if message.strip() == '':
            flash("Please fill in a message before sending", "danger")
            return "Failed"
        pusher.trigger('messages', 'new_message', {
            'message': message,
            'username': username,
            'time': time_stamp
        })
        current_channel = session.query(Channel).filter_by(
            name=channel_name).first()
        send_message = Message(content=message, sender_id=current_user.id,
                               channel_id=current_channel.id)
        session.add(send_message)
        session.commit()
        return Response(status=204)
    else:
        channel_name = request.args.get("channel_name")
        channel = session.query(Channel).filter_by(name=channel_name).first()
        messages = session.query(Message).filter_by(channel_id=channel.id)
        messages = messages.order_by(Message.time_stamp.asc())
        data = json.dumps([message.as_dictionary() for message in messages])
        return Response(data, 200, mimetype="application/json")


@app.route("/create-channel", methods=["GET", "POST"])
def create_channel():
    if request.method == "POST":
        channel_name = request.form["channel-name"]

        if session.query(Channel).filter_by(name=channel_name).first():
            flash ("There is already a channel with that name",
                   "danger")
            return redirect(url_for("create_channel"))

        while len(channel_name) < 4:
            flash("Please make the channel name at least 3 characters long",
                  "danger")
            return redirect(url_for("create_channel"))

        channel = Channel(name=channel_name, creator_id=current_user.id)

        session.add(channel)
        session.commit()
        return redirect(url_for('homepage'))
    else:
        return render_template("create_channel.html")


@app.route("/channel-list", methods=["GET"])
def channel_list():
    channels = session.query(Channel).order_by(Channel.created_date.asc()).all()
    data = json.dumps([channel.as_dictionary() for channel in channels])
    return Response(data, 200, mimetype="application/json")


@app.route("/delete-channel", methods=["POST"])
def delete_channel():
    if request.method == "POST":
        channel_name = request.form["current-channel"]
        channel = session.query(Channel).filter_by(name=channel_name).first()
        messages = session.query(Message).filter_by(channel_id=channel.id)
        session.delete(channel)
        session.delete(messages)
        session.commit()
        return Response(status=204)





