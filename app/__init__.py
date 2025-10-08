from flask import Flask
from flask_mongoengine import MongoEngine
from flask_login import LoginManager


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'spiritomb'
    app.config['MONGODB SETTINGS'] = {
        'db' : 'ICT239_SU2_LAB',
        'host' : 'localhost',
        'port' : 27017
    }
    login_manager = LoginManager(app)
    #login view
    login_manager.login_view = 'login'
    db = MongoEngine(app)

    return app, db, login_manager

app, db, login_manager = create_app()