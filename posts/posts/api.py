import json
from flask import request, Response, url_for
from jsonschema import validate, ValidationError
from . import models
from . import decorators
from posts import app
from .database import session
from sqlalchemy import or_


@app.route("/api/posts", methods=["GET"])
@decorators.accept("application/json")
def posts_get():
    """ Get a list of posts """
    title_like = request.args.get("title_like")
    body_like = request.args.get("body_like")

    posts = session.query(models.Post)
    if title_like:
        posts = posts.filter(models.Post.title.contains(title_like))
    if body_like:
        posts = posts.filter(models.Post.body.contains(body_like))
    if title_like and body_like:
        posts = posts.filter(or_(models.Post.title.contains(title_like),
                                 models.Post.body.contains(body_like)))

    posts = posts.order_by(models.Post.id)
    data = json.dumps([post.as_dictionary() for post in posts])
    return Response(data, 200, mimetype="application/json")


@app.route("/api/posts/<int:id>", methods=["GET"])
def post_get(id):
    """ Single post endpoint """
    post = session.query(models.Post).get(id)
    if not post:
        message = "Could not find post with id {}".format(id)
        data = json.dumps({"message": message})
        return Response(data, 404, mimetype="application/json")
    data = json.dumps(post.as_dictionary())
    return Response(data, 200, mimetype="application/json")
