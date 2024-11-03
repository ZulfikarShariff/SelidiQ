import os
from dotenv import load_dotenv
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# Load environment variables from .env file
load_dotenv()

# Initialize SQLAlchemy and Flask-Migrate (but do not bind to an app yet)
db = SQLAlchemy()
migrate = Migrate()

def create_app():
    # Create a Flask application instance
    app = Flask(__name__)

    # Set up the database configuration from environment variables
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'postgresql://default')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize SQLAlchemy and Flask-Migrate with the app instance
    db.init_app(app)
    migrate.init_app(app, db)

    # Import models to ensure they are registered with the app
    from selidiq.models import Student, Subject, Teacher, Class, StudentProgress, Lesson

    # Any additional configuration can go here, like registering blueprints or routes

    return app

# Import models to ensure they are registered
from selidiq.models import Student, Subject, Teacher, Class, StudentProgress

