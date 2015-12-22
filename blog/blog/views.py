from flask import render_template, flash, request, redirect, url_for
from blog import app
from .database import session, Entry, User
from flask_login import login_required, current_user, login_user, logout_user
from werkzeug.security import check_password_hash, generate_password_hash


@app.route("/")
@app.route("/page/<int:page>")
def entries(page=1, limit=10):

    paginate_by = int(request.args.get('limit', limit))
    page_index = page - 1
    count = session.query(Entry).count()
    start = page_index * paginate_by
    end = start + paginate_by
    total_pages = (count - 1) / paginate_by + 1
    has_next = page_index < total_pages - 1
    has_prev = page_index > 0
    posts = session.query(Entry)
    posts = posts.order_by(Entry.datetime.desc())
    posts = posts[start:end]

    return render_template("entries.html", paginate_by=paginate_by,
                           entries=posts, has_next=has_next,
                           has_prev=has_prev, page=page,
                           total_pages=total_pages)


@app.route("/add", methods=["GET"])
@app.route("/entry/add", methods=["GET"])
@login_required
def add_entry_get():
    return render_template("add_entry.html")


@app.route("/add", methods=["POST"])
@app.route("/entry/add", methods=["POST"])
@login_required
def add_entry_post():
    entry = Entry(title=request.form["title"], content=request.form["content"],
                  author=current_user)
    session.add(entry)
    session.commit()
    return redirect(url_for("entries"))


@app.route("/entry/<int:id>")
def view_post(id):
    entry = session.query(Entry).filter_by(id=id).first()
    return render_template("single_entry.html", entry=entry)


@app.route("/entry/<int:id>/edit", methods=["GET"])
@login_required
def edit_entry_get(id):
    entry = session.query(Entry).filter_by(id=id).first()
    return render_template("edit_entry.html", entry=entry)


@app.route("/entry/<int:id>/edit", methods=["POST"])
@login_required
def edit_entry_post(id):
    entry = session.query(Entry).filter_by(id=id).first()
    entry.title = request.form["title"]
    entry.content = request.form["content"]
    session.commit()
    return redirect(url_for("entries"))


@app.route("/entry/<int:id>/delete", methods=["GET"])
@login_required
def delete_entry_get(id):
    entry = session.query(Entry).filter_by(id=id).first()
    return render_template("delete_entry.html", entry=entry)


@app.route("/entry/<int:id>/delete", methods=["POST"])
@login_required
def delete_entry_post(id):
    entry = session.query(Entry).filter_by(id=id).first()
    session.delete(entry)
    session.commit()
    return redirect(url_for("entries"))


@app.route("/login", methods=["GET"])
def login_get():
    return render_template("login.html")


@app.route("/login", methods=["POST"])
def login_post():
    email = request.form["email"]
    password = request.form["password"]
    user = session.query(User).filter_by(email=email).first()
    if not user or not check_password_hash(user.password, password):
        flash("Incorrect username or password", "danger")
        return redirect(url_for("login_get"))
    login_user(user, remember=True)
    return redirect(request.args.get('next') or url_for("entries"))


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("entries"))


@app.route("/create-account", methods=["GET"])
def create_account_get():
    return render_template("create_account.html")


@app.route("/create-account", methods=["POST"])
def create_account_post():
    name = request.form["name"]
    email = request.form["email"]
    password = request.form["password"]
    confirm_password = request.form["confirm_password"]

    if session.query(User).filter_by(email=email).first():
        flash("The is already a registered user with that email", "danger")
        return redirect(url_for("create_account_get"))

    while len(password) < 8:
        flash("Please make the password at least 8 characters long", "danger")
        return redirect(url_for("create_account_get"))

    while password != confirm_password:
        flash("Passwords do not match", "danger")
        return redirect(url_for("create_account_get"))

    user = User(name=name, email=email,
                password=generate_password_hash(password))
    session.add(user)
    session.commit()
    login_user(user, remember=True)
    return redirect(url_for("entries"))

