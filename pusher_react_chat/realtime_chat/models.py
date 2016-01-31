import os.path

from flask import url_for
from sqlalchemy import Column, Integer, String, Sequence, ForeignKey
from sqlalchemy.orm import relationship
from realtime_chat import app
from .database import Base, engine, session




Base.metadata.create_all(engine)