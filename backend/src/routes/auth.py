"""
Authentication routes for the AI Directory Platform.
"""

from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import (
    create_access_token, create_refresh_token, jwt_required,
    get_jwt_identity, get_jwt
)
from datetime import datetime, timezone, timedelta
from ..models import User
from ..database import db
from ..utils import format_response, format_error

auth_bp = Blueprint('auth', __name__, url_prefix='/api/v1/auth')

@auth_bp.route('/register', methods=['POST'])
def register():
    """Register a new user."""
    data = request.get_json()
    
    # Validate required fields
    required_fields = ['email', 'password', 'first_name', 'last_name']
    for field in required_fields:
        if field not in data:
            return format_error(f"Missing required field: {field}", "VALIDATION_ERROR")
    
    # Check if user already exists
    if User.query.filter_by(email=data['email']).first():
        return format_error("Email already registered", "EMAIL_EXISTS")
    
    # Create new user
    user = User(
        email=data['email'],
        first_name=data['first_name'],
        last_name=data['last_name'],
        company=data.get('company'),
        job_title=data.get('job_title'),
        industry_id=data.get('industry_id'),
        subscription_tier='Free'
    )
    
    # Set password
    user.password = data['password']
    
    # Save user to database
    db.session.add(user)
    db.session.commit()
    
    # Generate tokens
    access_token = create_access_token(identity=user.id)
    refresh_token = create_refresh_token(identity=user.id)
    
    # Return user data and tokens
    return format_response({
        'user_id': user.id,
        'email': user.email,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'subscription_tier': user.subscription_tier,
        'token': access_token,
        'refresh_token': refresh_token
    }, "User registered successfully")

@auth_bp.route('/login', methods=['POST'])
def login():
    """Log in an existing user."""
    data = request.get_json()
    
    # Validate required fields
    if not data.get('email') or not data.get('password'):
        return format_error("Email and password are required", "VALIDATION_ERROR")
    
    # Find user by email
    user = User.query.filter_by(email=data['email']).first()
    
    # Check if user exists and password is correct
    if not user or not user.verify_password(data['password']):
        return format_error("Invalid email or password", "INVALID_CREDENTIALS", status_code=401)
    
    # Generate tokens
    access_token = create_access_token(identity=user.id)
    refresh_token = create_refresh_token(identity=user.id)
    
    # Return user data and tokens
    return format_response({
        'user_id': user.id,
        'email': user.email,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'subscription_tier': user.subscription_tier,
        'is_admin': user.is_admin,
        'token': access_token,
        'refresh_token': refresh_token
    }, "Login successful")

@auth_bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    """Refresh an expired JWT token."""
    current_user_id = get_jwt_identity()
    
    # Generate new access token
    access_token = create_access_token(identity=current_user_id)
    
    return format_response({
        'token': access_token
    }, "Token refreshed")

@auth_bp.route('/verify', methods=['GET'])
@jwt_required()
def verify():
    """Verify a JWT token."""
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    
    if not user:
        return format_error("User not found", "USER_NOT_FOUND", status_code=404)
    
    return format_response({
        'user_id': user.id,
        'email': user.email,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'subscription_tier': user.subscription_tier,
        'is_admin': user.is_admin
    }, "Token verified")

@auth_bp.route('/change-password', methods=['POST'])
@jwt_required()
def change_password():
    """Change user password."""
    data = request.get_json()
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    
    if not user:
        return format_error("User not found", "USER_NOT_FOUND", status_code=404)
    
    # Validate required fields
    if not data.get('current_password') or not data.get('new_password'):
        return format_error("Current password and new password are required", "VALIDATION_ERROR")
    
    # Check if current password is correct
    if not user.verify_password(data['current_password']):
        return format_error("Current password is incorrect", "INVALID_PASSWORD", status_code=401)
    
    # Update password
    user.password = data['new_password']
    db.session.commit()
    
    return format_response(message="Password changed successfully")

