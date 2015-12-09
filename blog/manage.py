import os
from flask.ext.script import Manager

from blog import app

#add a task to your manager which generates a series of entries in the database
from blog.database import session, Entry

#import manager object and create an instance of it
manager = Manager(app)

#add a command to the manager
@manager.command
def run():
    app.run(host="0.0.0.0", port=8080)

@manager.command
def seed():
    content = """Lorem ipsum dolor sit amet, consectetur adipisicing elit"""

    for i in range(25):
        entry = Entry(
             title = "Test Entry #{}".format(i),
             content = content
        )
        session.add(entry)
    session.commit()



#add test user
from getpass import getpass

from werkzeug.security import generate_password_hash

from blog.database import User

@manager.command
def adduser():
    name = input("Name: ")
    email = input("Email: ")
    if session.query(User).filter_by(email=email).first():
        print("User with that email address already exists")
        return

    password = ""
    while len(password) < 8 or password != password_2:
        password = getpass("Password: ")
        password_2 = getpass("Re-enter password: ")
        #generate_password_hash hashes the password
    user = User(name=name, email=email,
                password=generate_password_hash(password))
    session.add(user)
    session.commit()


#add migration command
from flask.ext.migrate import Migrate, MigrateCommand
from blog.database import Base

#holds the metadata object
# Alembic(migration tool) uses the metadata to work out the changes to the database schema
class DB(object):
    def __init__(self, metadata):
        self.metadata = metadata
#create instance of Flask's migrate class
#pass in app and instance of Db class
migrate = Migrate(app, DB(Base.metadata))
#add migrate commands to the manager
manager.add_command('db', MigrateCommand)


if __name__ == "__main__":
    manager.run()





