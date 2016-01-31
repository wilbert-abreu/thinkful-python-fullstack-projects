from flask import render_template

from realtime_chat import app


@app.route("/")
def index():
    return app.send_static_file("index.html")

