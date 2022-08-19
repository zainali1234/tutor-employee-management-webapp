from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

db = SQLAlchemy()
DB_NAME = "database.db"

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'hjshjhdjahkjshkjdhjs'
    
    # connects to database
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)
    
    # intializes login functionality
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)
    
    # imports blueprints to link to webpages 
    from .account import account
    from .auth import auth
    from .admin import admin
    
    # registers blueprints 
    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(account, url_prefix='/')
    app.register_blueprint(admin, url_prefix='/')
    
    # imports database schemas
    from .models import Employee, SessionForm, Student

    # allows reference of user object and attributes
    @login_manager.user_loader
    def load_user(id):
        return Employee.query.get(int(id))

    create_db(app)
    return app

# creates SQLAlchemy database
def create_db(app):
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
