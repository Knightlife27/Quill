from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# Initialize the database and migration objects
db = SQLAlchemy()
migrate = Migrate()

def create_app():
    # Create a new Flask application
    app = Flask(__name__)

    # Configure your app here
    app.config['SQLALCHEMY_DATABASE_URI'] = 'your_database_uri_here'  # Update with your actual database URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize the database and migration with the app
    db.init_app(app)
    migrate.init_app(app, db)

    # Import and register blueprints here
    from .routes import api as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api')

    return app