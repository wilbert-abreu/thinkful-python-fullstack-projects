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

if __name__ == "__main__":
    manager.run()



