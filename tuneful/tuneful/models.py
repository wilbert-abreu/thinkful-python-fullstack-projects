import os.path

from flask import url_for
from sqlalchemy import Column, Integer, String, Sequence, ForeignKey
from sqlalchemy.orm import relationship
from tuneful import app
from .database import Base, engine, session


class Song(Base):
    __tablename__ = "songs"

    id = Column(Integer, primary_key=True)
    file_id = Column(Integer, ForeignKey('files.id'))

    def as_dictionary(self):
        file_info = session.query(File).filter_by(id=self.file_id).first()
        song = {
            "id": self.id,
            "file": {
                "id": file_info.id,
                "name": file_info.filename
            }
        }
        return song


class File(Base):
    __tablename__ = "files"

    id = Column(Integer, primary_key=True)
    filename = Column(String(1024))
    song = relationship("Song", uselist=False, backref="song")

    def as_dictionary(self):
        file = {
            "id": self.id,
            "name": self.filename,
            "path": url_for("uploaded_file", filename=self.filename)
        }
        return file

Base.metadata.create_all(engine)