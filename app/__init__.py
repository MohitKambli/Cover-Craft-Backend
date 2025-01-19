from flask import Flask
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config')  # Load app configuration
    CORS(app, resources={r"/*": {"origins": ["http://localhost:3000", "cover-craft-frontend.vercel.app"], "methods": ["GET", "POST", "PUT", "DELETE"]}})

    # Import and register blueprints (routes)
    from app.routes import api
    app.register_blueprint(api)

    return app
