import os
from flask.ext.script import Manager

from blog import app

#import manager object and create an instance of it
manager = Manager(app)

#add a command to the manager
@manager.command
def run():
    app.run(host="0.0.0.0", port="8080")

if __name__ == "__main__":
    manager.run()
