from flask_login import LoginManager
from slack_clone import app
from .models import session, User

login_manager = LoginManager()

login_manager.init_app(app)

login_manager.login_view = "login"

login_manager.login_message_category = "danger"

@login_manager.user_loader
def load_user(user_id):
    return session.query(User).get(int(user_id))

# how does this work exactly?