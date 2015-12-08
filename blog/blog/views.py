from flask import render_template

from blog import app
from .database import session, Entry
"""
@app.route("/")
def entries():
    entries = session.query(Entry)
    entries = entries.order_by(Entry.title.desc())
    entries = entries.all()
    return render_template("entries.html", entries=entries)
"""
PAGINATE_BY = 10

@app.route("/")
@app.route("/page/<int:page>")
def entries(page=1):
    # Zero-indexed page
    # 4
    page_index = page - 1
    #3

    count = session.query(Entry).count()
    #26
    start = page_index * PAGINATE_BY

    end = start + PAGINATE_BY

    total_pages = (count - 1) / PAGINATE_BY + 1
    #25/11 2.27
    has_next = page_index < total_pages - 1

    has_prev = page_index > 0

    entries = session.query(Entry)
    entries = entries.order_by(Entry.datetime.desc())
    entries = entries[start:end]

    return render_template("entries.html",
        entries=entries,
        has_next=has_next,
        has_prev=has_prev,
        page=page,
        total_pages=total_pages
    )

# This specifies that the route will only be used for GET requests to the page
# I will have to add a new view for the POST request which takes place when you submit the form
@app.route("/entry/add", methods=["GET"])
def add_entry_get():
    return render_template("add_entry.html")

#takes the form data and creates a new blog entry
from flask import request, redirect, url_for

#similar to add_entry_get but only accepts posts
@app.route("/entry/add", methods=["POST"])
def add_entry_post():
    entry = Entry(
                  # request.form dictionary allows you to use the data submitted in the from
            title=request.form["title"],
            content=request.form["content"],
        )
    session.add(entry)
    session.commit()
    return redirect(url_for("entries"))

# view single post
@app.route("/entry/<int:id>")
def view_post(id):
    entry = session.query(Entry).filter_by(id=id).first()
    return render_template("single_entry.html",
        entry=entry
    )

@app.route("/entry/<int:id>/edit", methods=["GET"])
def edit_entry_get(id):
    entry = session.query(Entry).filter_by(id=id).first()
    return render_template("edit_entry.html", entry=entry)

@app.route("/entry/<int:id>/edit", methods=["POST"])
def edit_entry_post(id):
    entry = session.query(Entry).filter_by(id=id).first()
    entry.title = request.form["title"]
    entry.content = request.form["content"]
    session.commit()
    return redirect(url_for("entries"))
