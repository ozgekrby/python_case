from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    
    # Configure database
    app.config['SECRET_KEY'] = os.urandom(24)  # Session için güvenli bir key
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///quiz.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Initialize database
    db.init_app(app)
    
    # Import and register blueprints/routes
    from routes import main
    app.register_blueprint(main)
    
    # Create database tables
    with app.app_context():
        db.create_all()
    
    return app
