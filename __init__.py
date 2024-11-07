# selidiq/__init__.py

import os
from dotenv import load_dotenv
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# Load environment variables
load_dotenv()

# Initialize extensions
db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)

    # Configure the app using environment variables
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)

    # Import and register the Blueprint
    from .routes import main
    app.register_blueprint(main)

    # Ensure models are imported for Alembic migrations
    from .models import Student, Subject, Teacher, Class, StudentProgress, Lesson

    return app

