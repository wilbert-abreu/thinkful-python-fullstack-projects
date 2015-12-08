from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from datetime import datetime

from sqlalchemy import Column, Integer,Float, String, DateTime

# this will talk directly to your database using the raw SQL commands
engine = create_engine('postgresql://wilbertabreu@localhost:5432/tbay')
# equivalent to the psycopg2 cursor, queue up and execute databse transactions, multiple sessions can take place simultaneously
Session = sessionmaker(bind=engine)
session = Session()
# repository for the models, will isse the create table statements
Base = declarative_base()

class Item(Base):
    __tablename__ = "items"
    # set primary key
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String)
    start_time = Column(DateTime, default=datetime.utcnow)

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False)
    password = Column(String, nullable=False)

class bid(Base):
    __tablename__ = "bids"
    id = Column(Integer, primary_k/ey=True)
    price = Column(Float)

#creates a new table for each subclass of Base, ignoring any tables which already existi
Base.metadata.create_all(engine)

# creating rows
wilbert = User(username="wabreu", password="123456")
session.add(wilbert)
session.commit()

abby = User(username="acg361", password="123123")
session.add(abby)
session.commit()

item1 = Item(name="Item1", description="Item1")
session.add(item1)
session.commit()
item2 = Item(name="Item2", description="Item2")
session.add(item2)
session.commit()

# Querying for rows

# Returns a list of all of the user objects
# Note that user objects won't display very prettily by default -
# you'll see their type (User) and their internal identifiers.
session.query(User).all() # Returns a list of all of the user objects

# Returns the first user
session.query(User).first()

# Finds the user with the primary key equal to 1
session.query(User).get(1)

# Returns a list of all of the usernames in ascending order
session.query(User.username).order_by(User.username).all()

# Returns the description of all of the basesballs
session.query(Item.description).filter(Item.name == "baseball").all()

# Return the item id and description for all baseballs which were created in the past.  Remember to import the datetime object: from datetime import datetime
session.query(Item.id, Item.description).filter(Item.name == "baseball", Item.start_time < datetime.utcnow()).all()


# Updating Rows
user = session.query(User).first()
user.username = "solange"
session.commit()

# Deleting rows
user = session.query(User).first()
session.delete(user)
session.commit()
