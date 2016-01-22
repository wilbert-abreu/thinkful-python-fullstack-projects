import os.path
import json

from flask import request, Response, url_for, send_from_directory
from werkzeug.utils import secure_filename
from jsonschema import validate, ValidationError

from . import models
from . import decorators
from tuneful import app
from .database import session
from .utils import upload_path

song_schema = {
    "properties": {
        "file": {
            "properties": {
                "id": {"type": "integer"}
            },

        },
    },
    "required": ["file"]
}


@app.route("/api/songs", methods=["GET"])
@decorators.accept("application/json")
def songs_get():
    """ Get a list of songs """
    songs = session.query(models.Song)
    songs = songs.order_by(models.Song.id)
    data = json.dumps([song.as_dictionary() for song in songs])
    return Response(data, 200, mimetype="application/json")


@app.route("/api/songs", methods=["POST"])
@decorators.accept("application/json")
@decorators.require("application/json")
def posts_song():
    """ Add a new song """
    data = request.json
    try:
        validate(data, song_schema)
    except ValidationError as error:
        data = {"message": error.message}
        return Response(json.dumps(data), 422, mimetype="application/json")
    song = models.Song(file_id=data["file"]["id"])
    session.add(song)
    session.commit()
    data = json.dumps(song.as_dictionary())
    headers = {"Location": url_for("songs_get", id=song.id)}
    return Response(data, 201, headers=headers,
                    mimetype="application/json")


@app.route("/api/files", methods=["POST"])
@decorators.require("multipart/form-data")
@decorators.accept("application/json")
def file_post():
    file = request.files.get("file")
    if not file:
        data = {"message": "Could not find file data"}
        return Response(json.dumps(data), 422, mimetype="application/json")

    filename = secure_filename(file.filename)
    db_file = models.File(filename=filename)
    session.add(db_file)
    session.commit()
    file.save(upload_path(filename))

    data = db_file.as_dictionary()
    return Response(json.dumps(data), 201, mimetype="application/json")


@app.route("/api/files/<int:id>", methods=["PUT"])
@decorators.require("multipart/form-data")
@decorators.accept("application/json")
def file_edit(id):
    file = session.query(models.File).get(id)
    if not file:
        message = "Could not find file with id {}".format(id)
        data = json.dumps({"message": message})
        return Response(data, 404, mimetype="application/json")
    data = request.json
    try:
        validate(data, song_schema)
    except ValidationError as error:
        data = {"message": error.message}
        return Response(json.dumps(data), 422, mimetype="application/json")
    file.filename = data["name"]
    session.commit()
    data = json.dumps(file.as_dictionary())
    return Response(data, 200, mimetype="application/json")






