from flask import render_template

from tuneful import app


@app.route("/")
def index():
    return app.send_static_file("index.html")


@app.route("/uploads/<filename>", methods=["GET"])
def uploaded_file(filename):
    return send_from_directory(upload_path(), filename)
