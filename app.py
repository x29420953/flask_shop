from flask import Flask, session
from flask_login import LoginManager

from model import db, User
from accounts.views import accounts
from shop.views import shop

app = Flask(__name__)
app.config.from_object("config.Config")
db.init_app(app)
login_manager = LoginManager()
login_manager.login_view = "accounts.login"
login_manager.init_app(app)

app.register_blueprint(accounts, url_prefix='/accounts')
app.register_blueprint(shop, url_prefix='/shop')


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


if __name__ == "__main__":
    app.run(debug=True)
