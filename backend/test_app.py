import os
from flask import Flask, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from src.database import db, init_db

def create_test_app():
    app = Flask(__name__)
    
    # Configuration
    app.config['SECRET_KEY'] = 'test-secret-key-change-in-production'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///instance/test_ai_directory.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = 'test-jwt-secret-key'
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = False
    
    # Initialize extensions
    CORS(app, origins="*")
    jwt = JWTManager(app)
    
    # Initialize database
    init_db(app)
    
    # Test route
    @app.route('/api/health')
    def health_check():
        return jsonify({
            'status': 'healthy',
            'message': 'AI Directory API is running'
        }), 200
    
    return app

if __name__ == '__main__':
    app = create_test_app()
    print("Starting test Flask application...")
    app.run(host='0.0.0.0', port=5000, debug=True)

