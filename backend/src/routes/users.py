"""
User routes for the AI Directory Platform.
"""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..models import User, UserActivityLog
from ..database import db
from ..utils import format_response, format_error, admin_required, paginate

users_bp = Blueprint('users', __name__, url_prefix='/api/v1/users')

@users_bp.route('/me', methods=['GET'])
@jwt_required()
def get_current_user():
    """Get the current user's profile."""
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    
    if not user:
        return format_error("User not found", "USER_NOT_FOUND", status_code=404)
    
    # Log activity
    UserActivityLog.log_activity(
        user_id=current_user_id,
        activity_type='view_profile'
    )
    
    return format_response(user.to_dict())

@users_bp.route('/me', methods=['PUT'])
@jwt_required()
def update_current_user():
    """Update the current user's profile."""
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    
    if not user:
        return format_error("User not found", "USER_NOT_FOUND", status_code=404)
    
    data = request.get_json()
    
    # Update user fields
    if 'first_name' in data:
        user.first_name = data['first_name']
    
    if 'last_name' in data:
        user.last_name = data['last_name']
    
    if 'company' in data:
        user.company = data['company']
    
    if 'job_title' in data:
        user.job_title = data['job_title']
    
    if 'industry_id' in data:
        user.industry_id = data['industry_id']
    
    # Save changes to database
    db.session.commit()
    
    # Log activity
    UserActivityLog.log_activity(
        user_id=current_user_id,
        activity_type='update_profile'
    )
    
    return format_response(user.to_dict(), "Profile updated successfully")

@users_bp.route('', methods=['GET'])
@jwt_required()
@admin_required
def get_users():
    """Get a list of all users (admin only)."""
    # Get query parameters
    search = request.args.get('search', '')
    subscription_tier = request.args.get('subscription_tier')
    
    # Start with base query
    query = User.query
    
    # Apply search filter
    if search:
        query = query.filter(
            (User.email.ilike(f'%{search}%')) |
            (User.first_name.ilike(f'%{search}%')) |
            (User.last_name.ilike(f'%{search}%'))
        )
    
    # Apply subscription tier filter
    if subscription_tier:
        query = query.filter(User.subscription_tier == subscription_tier)
    
    # Paginate results
    result = paginate(query)
    
    # Format response
    users = [user.to_dict() for user in result['items']]
    
    return format_response({
        'users': users,
        'pagination': result['pagination']
    })

@users_bp.route('/<int:user_id>', methods=['GET'])
@jwt_required()
@admin_required
def get_user(user_id):
    """Get a specific user by ID (admin only)."""
    user = User.query.get(user_id)
    
    if not user:
        return format_error("User not found", "USER_NOT_FOUND", status_code=404)
    
    return format_response(user.to_dict())

@users_bp.route('/<int:user_id>', methods=['PUT'])
@jwt_required()
@admin_required
def update_user(user_id):
    """Update a specific user (admin only)."""
    user = User.query.get(user_id)
    
    if not user:
        return format_error("User not found", "USER_NOT_FOUND", status_code=404)
    
    data = request.get_json()
    
    # Update user fields
    if 'first_name' in data:
        user.first_name = data['first_name']
    
    if 'last_name' in data:
        user.last_name = data['last_name']
    
    if 'company' in data:
        user.company = data['company']
    
    if 'job_title' in data:
        user.job_title = data['job_title']
    
    if 'industry_id' in data:
        user.industry_id = data['industry_id']
    
    if 'subscription_tier' in data:
        user.subscription_tier = data['subscription_tier']
    
    if 'is_admin' in data:
        user.is_admin = data['is_admin']
    
    # Save changes to database
    db.session.commit()
    
    # Log activity
    current_user_id = get_jwt_identity()
    UserActivityLog.log_activity(
        user_id=current_user_id,
        activity_type='admin_update_user',
        details=f"Updated user {user.id}"
    )
    
    return format_response(user.to_dict(), "User updated successfully")

@users_bp.route('/<int:user_id>', methods=['DELETE'])
@jwt_required()
@admin_required
def delete_user(user_id):
    """Delete a specific user (admin only)."""
    user = User.query.get(user_id)
    
    if not user:
        return format_error("User not found", "USER_NOT_FOUND", status_code=404)
    
    # Log activity before deleting the user
    current_user_id = get_jwt_identity()
    UserActivityLog.log_activity(
        user_id=current_user_id,
        activity_type='admin_delete_user',
        details=f"Deleted user {user.id} ({user.email})"
    )
    
    # Delete user from database
    db.session.delete(user)
    db.session.commit()
    
    return format_response(message="User deleted successfully")

@users_bp.route('/me/favorites', methods=['GET'])
@jwt_required()
def get_favorites():
    """Get the current user's favorite AI tools."""
    from ..models import UserFavorite
    
    current_user_id = get_jwt_identity()
    
    # Start with base query
    query = UserFavorite.query.filter_by(user_id=current_user_id)
    
    # Paginate results
    result = paginate(query)
    
    # Format response
    favorites = [favorite.to_dict() for favorite in result['items']]
    
    return format_response({
        'favorites': favorites,
        'pagination': result['pagination']
    })

