from flask import Flask, jsonify
from flask_cors import CORS
from app.routes.recommend_routes import recommend_bp
from app.database import init_db

from werkzeug.exceptions import InternalServerError
from sqlalchemy.exc import SQLAlchemyError

def register_error_handlers(app):
    @app.errorhandler(SQLAlchemyError)
    def handle_database_error(error):
        app.logger.error(f"Database error: {str(error)}")
        return jsonify({
            "error": "Database connection error",
            "message": str(error)
        }), 500

def create_app():
    app = Flask(__name__)
    CORS(app)

    # Initialize database
    # init_db()

    # Register error handlers
    register_error_handlers(app)

    # Register blueprints
    app.register_blueprint(recommend_bp, url_prefix='/api')

    return app