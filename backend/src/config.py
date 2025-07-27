"""
Configuration settings for the AI Directory Platform.
"""

import os
from datetime import timedelta

class Config:
    """Base configuration."""
    
    # Flask settings
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-key-please-change-in-production')
    DEBUG = False
    TESTING = False
    
    # SQLAlchemy settings
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///ai_directory.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # JWT settings
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'jwt-dev-key-please-change-in-production')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
    
    # File upload settings
    UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB
    
    # API settings
    API_TITLE = 'AI Directory API'
    API_VERSION = '1.0.0'
    
    # CORS settings
    CORS_ORIGINS = ['*']
    
    # Rate limiting
    RATELIMIT_DEFAULT = "100/minute"
    RATELIMIT_STORAGE_URL = "memory://"
    
    # Subscription plans
    SUBSCRIPTION_PLANS = {
        'free': {
            'name': 'Free',
            'description': 'Basic access to the AI Directory',
            'price': 0,
            'currency': 'USD',
            'interval': 'month',
            'features': [
                'Browse all AI tools',
                'Basic search and filters',
                'Tool ratings and reviews',
                'Community support'
            ]
        },
        'premium': {
            'name': 'Premium',
            'description': 'Enhanced access with additional features',
            'price': 9.99,
            'currency': 'USD',
            'interval': 'month',
            'features': [
                'Everything in Free',
                'Advanced search filters',
                'Save favorite tools',
                'Write reviews',
                'Priority support',
                'Export tool lists'
            ]
        },
        'business': {
            'name': 'Business',
            'description': 'Complete access for professional use',
            'price': 29.99,
            'currency': 'USD',
            'interval': 'month',
            'features': [
                'Everything in Premium',
                'Team collaboration',
                'Custom categories',
                'API access',
                'Analytics dashboard',
                'Dedicated support'
            ]
        }
    }

class DevelopmentConfig(Config):
    """Development configuration."""
    
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///ai_directory_dev.db'

class TestingConfig(Config):
    """Testing configuration."""
    
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///ai_directory_test.db'
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(seconds=5)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(seconds=10)

class ProductionConfig(Config):
    """Production configuration."""
    
    # Use environment variables for sensitive settings
    SECRET_KEY = os.environ.get('SECRET_KEY')
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    
    # Stricter CORS settings
    CORS_ORIGINS = os.environ.get('CORS_ORIGINS', '').split(',')

# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}

