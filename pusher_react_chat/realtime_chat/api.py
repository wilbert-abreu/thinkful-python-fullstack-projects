import os.path
import json
import cgi

from flask import request, Response, url_for, send_from_directory
from werkzeug.utils import secure_filename
from jsonschema import validate, ValidationError

from . import models
from . import decorators
from realtime_chat import app
from .database import session
from pusher import Pusher # get this package via `pip install pusher`

pusher = Pusher(
  app_id='173573',
  key='b568462b35424532aa89',
  secret='37566de4aecc1f1b312c'
)


@app.route('/messages', methods=['POST'])
def new_message():
  username = request.form['username']
  text = cgi.escape(request.form['text']) # let's escape it for security's sake
  time = request.form['time']

  # ENTER MAGIC HERE
  pusher.trigger('messages', 'new_message', {
    'text': text,
    'username': username,
    'time': time
  })

  return "great success!"










