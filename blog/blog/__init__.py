import os
# from config import DevelopmentConfig
from flask import Flask



app = Flask(__name__)
config_path = "blog.config.DevelopmentConfig"
app.config.from_object(config_path)

# add new files here to new code to app
from . import views
from . import filters
from . import login
