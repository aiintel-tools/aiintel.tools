"""
Main application module for the AI Directory Platform.
"""

import os
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from werkzeug.middleware.proxy_fix import ProxyFix

from .config import config
from .database import init_app as init_db
from .routes.auth import auth_bp
from .routes.tools import tools_bp
from .routes.users import users_bp
from .routes.categories import categories_bp
from .routes.industries import industries_bp
from .routes.reviews import reviews_bp
from .routes.subscriptions import subscriptions_bp
from .routes.admin import admin_bp

def create_app(config_name='default'):
    """Create and configure the Flask application."""
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object(config[config_name])
    
    # Configure middleware
    app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1)
    
    # Initialize extensions
    CORS(app, resources={r"/*": {"origins": app.config['CORS_ORIGINS']}})
    jwt = JWTManager(app)
    limiter = Limiter(
        get_remote_address,
        app=app,
        default_limits=[app.config['RATELIMIT_DEFAULT']],
        storage_uri=app.config['RATELIMIT_STORAGE_URL']
    )
    
    # Initialize database
    init_db(app)
    
    # Create upload directory if it doesn't exist
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    
    # Register blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(tools_bp)
    app.register_blueprint(users_bp)
    app.register_blueprint(categories_bp)
    app.register_blueprint(industries_bp)
    app.register_blueprint(reviews_bp)
    app.register_blueprint(subscriptions_bp)
    app.register_blueprint(admin_bp)
    
    # Root route
    @app.route('/')
    def index():
        return jsonify({
            'name': app.config['API_TITLE'],
            'version': app.config['API_VERSION'],
            'status': 'running',
            'message': 'Welcome to AI Directory API'
        })
    
    # Health check route
    @app.route('/api/health')
    def health():
        return jsonify({
            'status': 'healthy',
            'version': app.config['API_VERSION'],
            'message': 'AI Directory API is running'
        })
    
    # Serve uploaded files
    @app.route('/uploads/<path:filename>')
    def uploaded_file(filename):
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
    
    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'error': {
                'code': 'NOT_FOUND',
                'message': 'The requested resource was not found'
            }
        }), 404
    
    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({
            'success': False,
            'error': {
                'code': 'METHOD_NOT_ALLOWED',
                'message': 'The method is not allowed for the requested URL'
            }
        }), 405
    
    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({
            'success': False,
            'error': {
                'code': 'INTERNAL_SERVER_ERROR',
                'message': 'An internal server error occurred'
            }
        }), 500
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=True)

