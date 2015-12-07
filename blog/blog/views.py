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
