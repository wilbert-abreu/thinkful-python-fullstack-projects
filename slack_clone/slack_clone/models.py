import os.path
import datetime
from flask import url_for
from sqlalchemy import Column, Integer, String, Sequence, ForeignKey, \
    DateTime, Text
from sqlalchemy.orm import relationship
from slack_clone import app
from .database import Base, engine, session
from flask_login import UserMixin


class User(Base, UserMixin):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    email = Column(String(128), unique=True)
    name = Column(String(128))
    display_name = Column(String(128))
    password = Column(String(128))

    account_creation_date = Column(DateTime, default=datetime.datetime.utcnow)
    channels_subscribed = relationship("Channel", backref="channel")
    files_uploaded = relationship("File", backref="file")


class File(Base):
    __tablename__ = "file"

    id = Column(Integer, primary_key=True)
    filename = Column(String(128))
    upload_date = Column(DateTime, default=datetime.datetime.utcnow)
    user_id = Column(Integer, ForeignKey('user.id'))
    channel_id = Column(Integer, ForeignKey('channel.id'))
    caption = Column(Text(1024))


class Channel(Base):
    __tablename__ = "channel"

    id = Column(Integer, primary_key=True)
    name = Column(String(128), unique=True)
    creator_id = Column(Integer, ForeignKey('user.id'))
    created_date = Column(DateTime, default=datetime.datetime.utcnow)


class Message(Base):
    __tablename__ = "message"

    id = Column(Integer, primary_key=True)
    channel_id = Column(Integer, ForeignKey('channel.id'))
    sender_id = Column(Integer, ForeignKey('user.id'))
    time_stamp = Column(DateTime, default=datetime.datetime.utcnow)
    content = Column(Text())

    def as_dictionary(self):
        user = session.query(User).filter_by(id=self.sender_id).first()
        channel = session.query(Channel).filter_by(
                id=self.channel_id).first()
        messages = {
            "id": self.id,
            "channel_name": channel.name,
            "display_name": user.display_name,
            "time_stamp": str(self.time_stamp),
            "content": self.content
        }
        return messages

Base.metadata.create_all(engine)