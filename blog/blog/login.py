from flask.ext.login import LoginManager

from blog import app
from .database import session, User

# creates inatnce of login manager and ints it
login_manager = LoginManager()
login_manager.init_app(app)

#login_view = login screen view
login_manager.login_view = "login_get"

#classifies error messages from Flask-Login
login_manager.login_message_category = "danger"

# tells flask-login how to access a user id
@login_manager.user_loader
def load_user(id):
    return session.query(User).get(int(id))
