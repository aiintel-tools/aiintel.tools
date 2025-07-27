import os
from flask import Flask, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from database import db, init_db

def create_app():
    app = Flask(__name__, static_folder=os.path.join(os.path.dirname(__file__), 'static'))
    
    # Configuration
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'ai-directory-secret-key-change-in-production')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///instance/ai_directory.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'jwt-secret-key-change-in-production')
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = False
    
    # Initialize extensions
    CORS(app, origins="*")
    jwt = JWTManager(app)
    
    # Initialize rate limiting
    limiter = Limiter(
        app=app,
        key_func=get_remote_address,
        default_limits=["1000 per hour"]
    )
    
    # JWT error handlers
    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return jsonify({'error': 'Token has expired'}), 401
    
    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return jsonify({'error': 'Invalid token'}), 401
    
    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return jsonify({'error': 'Authorization token is required'}), 401
    
    # Initialize database
    init_db(app)
    
    # Health check endpoint
    @app.route('/api/health')
    def health_check():
        return jsonify({
            'status': 'healthy',
            'message': 'AI Directory API is running',
            'version': '1.0.0'
        }), 200
    
    # Basic API info endpoint
    @app.route('/api/info')
    def api_info():
        return jsonify({
            'name': 'AI Directory API',
            'version': '1.0.0',
            'description': 'AI Tools Directory Platform API',
            'endpoints': {
                'health': '/api/health',
                'auth': '/api/auth/*',
                'tools': '/api/tools/*',
                'users': '/api/users/*',
                'categories': '/api/categories/*',
                'admin': '/api/admin/*',
                'subscriptions': '/api/subscriptions/*'
            }
        }), 200
    
    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'error': 'Endpoint not found'}), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({'error': 'Internal server error'}), 500
    
    return app

if __name__ == '__main__':
    app = create_app()
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)

