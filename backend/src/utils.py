"""
Utility functions for the AI Directory Platform.
"""
import os
import uuid
from datetime import datetime
from werkzeug.utils import secure_filename
from flask import current_app, request, jsonify
from functools import wraps
from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request, jwt_required

def allowed_file(filename):
    """Check if the file extension is allowed."""
    allowed_extensions = {'png', 'jpg', 'jpeg', 'gif'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions

def save_image(file, folder='tool_images'):
    """Save an image file and return the path."""
    if not file:
        return None
    
    if not allowed_file(file.filename):
        raise ValueError('File type not allowed')
    
    # Create the upload folder if it doesn't exist
    upload_folder = os.path.join(current_app.config['UPLOAD_FOLDER'], folder)
    os.makedirs(upload_folder, exist_ok=True)
    
    # Generate a unique filename
    filename = secure_filename(file.filename)
    unique_filename = f"{uuid.uuid4().hex}_{filename}"
    
    # Save the file
    file_path = os.path.join(upload_folder, unique_filename)
    file.save(file_path)
    
    # Return the relative path
    return os.path.join(folder, unique_filename)

def delete_image(image_path):
    """Delete an image file."""
    if not image_path:
        return
    
    file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], image_path)
    
    if os.path.exists(file_path):
        os.remove(file_path)

def admin_required(fn):
    """Decorator to require admin privileges."""
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        from src.models.user import User
        
        current_user_id = get_jwt_identity()
        current_user = User.query.get(current_user_id)
        
        if not current_user or not current_user.is_admin:
            return jsonify({
                'success': False,
                'error': {
                    'code': 'FORBIDDEN',
                    'message': 'Admin privileges required'
                }
            }), 403
        
        return fn(*args, **kwargs)
    
    return wrapper

def subscription_required(min_tier='Premium'):
    """Decorator to require a minimum subscription tier."""
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            verify_jwt_in_request()
            from src.models.user import User
            
            current_user_id = get_jwt_identity()
            current_user = User.query.get(current_user_id)
            
            if not current_user:
                return jsonify({
                    'success': False,
                    'error': {
                        'code': 'UNAUTHORIZED',
                        'message': 'Authentication required'
                    }
                }), 401
            
            # Define tier hierarchy
            tiers = {
                'Free': 0,
                'Premium': 1,
                'Business': 2
            }
            
            if tiers.get(current_user.subscription_tier, -1) < tiers.get(min_tier, 0):
                return jsonify({
                    'success': False,
                    'error': {
                        'code': 'SUBSCRIPTION_REQUIRED',
                        'message': f'{min_tier} subscription required'
                    }
                }), 403
            
            return fn(*args, **kwargs)
        
        return wrapper
    
    return decorator

def paginate(query, page=1, per_page=20):
    """Paginate a SQLAlchemy query."""
    page = int(request.args.get('page', page))
    per_page = int(request.args.get('limit', per_page))
    
    items = query.paginate(page=page, per_page=per_page, error_out=False)
    
    return {
        'items': items.items,
        'pagination': {
            'total': items.total,
            'page': items.page,
            'limit': per_page,
            'pages': items.pages
        }
    }

def format_response(data=None, message=None, success=True, status_code=200):
    """Format a consistent API response."""
    response = {
        'success': success
    }
    
    if message:
        response['message'] = message
    
    if data is not None:
        response['data'] = data
    
    return jsonify(response), status_code

def format_error(message, code, details=None, status_code=400):
    """Format a consistent API error response."""
    response = {
        'success': False,
        'error': {
            'code': code,
            'message': message
        }
    }
    
    if details:
        response['error']['details'] = details
    
    return jsonify(response), status_code

