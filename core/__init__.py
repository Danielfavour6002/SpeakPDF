import getpass
from flask.cli import FlaskGroup
from flask import Flask, render_template
from flask_migrate import Migrate
from flask_login  import LoginManager, current_user
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from celery import Celery
import datetime



load_dotenv()
import os

db = SQLAlchemy()

DB_NAME = 'database.db'

def make_celery(app):
    celery = Celery(app.import_name, broker=app.config['CELERY_BROKER_URL'])
    celery.conf.update(app.config)
    return celery

def create_app():
    app = Flask(__name__)
    
    # Configuration
    app.config['UPLOAD_FOLDER'] = os.getenv('UPLOAD_FOLDER') 
    app.config['OUTPUT_FOLDER'] = os.getenv('OUTPUT_FOLDER')
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
    app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'

    celery = make_celery(app)

    db.init_app(app)
    migrate = Migrate(app, db)

    # Register Blueprints
    from .auth import auth as auth_blueprint
    from .main import main as main_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/')
    app.register_blueprint(main_blueprint)

    login_manager = LoginManager()
    login_manager.init_app(app)
    from .models import User
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(id)
    @login_manager.unauthorized_handler
    def unauthorized_callback():
        return render_template('login.html')
    # cli = FlaskGroup(app)
    # @cli.command("create_admin")
    # def create_admin():
    #     """Creates the admin user."""
    #     user_name = input("Enter username")
    #     email = input("Enter email address: ")
    #     password = getpass.getpass("Enter password: ")
    #     confirm_password = getpass.getpass("Enter password again: ")
    #     if password != confirm_password:
    #         print("Passwords don't match")
    #     else:
    #         try:
    #             user = User(
    #                 user_name=user_name,
    #                 email=email,
    #                 password=password,
    #                 is_admin=True,
    #                 is_confirmed=True,
    #                 confirmed_on=datetime.now(),
    #             )
    #             db.session.add(user)
    #             db.session.commit()
    #             print(f"Admin with email {email} created successfully!")
    #         except Exception:
    #             print("Couldn't create admin user.")
    

    # Create directories if they don't exist
    with app.app_context():
        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
        os.makedirs(app.config['OUTPUT_FOLDER'], exist_ok=True)
        db.create_all()

    return app, celery


