from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from blog import app

engine = create_engine("postgresql://ubuntu:wilbertabreu@locahost:5432/blogful")
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()
