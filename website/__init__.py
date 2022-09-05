from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
from . import config
from .models import db


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    # connect sqlalchemy to mysql db
    app.config['SQLALCHEMY_DATABASE_URI'] = config.DATABASE_CONNECTION_URI
    app.config['SECRET_KEY'] = 'hjshjhdjah kjshkjdhjs'

    from .models import User, Note
    import time
    try:
        db.init_app(app)
    except:
        time.sleep(1000000) #for debugging

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    db.create_all(app=app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app