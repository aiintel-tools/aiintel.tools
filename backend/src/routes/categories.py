"""
Category routes for the AI Directory Platform.
"""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from ..models import Category
from ..database import db
from ..utils import format_response, format_error, admin_required

categories_bp = Blueprint('categories', __name__, url_prefix='/api/v1/categories')

@categories_bp.route('', methods=['GET'])
def get_categories():
    """Get a list of all categories."""
    categories = Category.query.all()
    
    # Format response
    category_list = [category.to_dict() for category in categories]
    
    return format_response(category_list)

@categories_bp.route('/<int:category_id>', methods=['GET'])
def get_category(category_id):
    """Get a specific category by ID."""
    category = Category.query.get(category_id)
    
    if not category:
        return format_error("Category not found", "CATEGORY_NOT_FOUND", status_code=404)
    
    return format_response(category.to_dict())

@categories_bp.route('', methods=['POST'])
@jwt_required()
@admin_required
def create_category():
    """Create a new category."""
    data = request.get_json()
    
    # Validate required fields
    if not data.get('name'):
        return format_error("Name is required", "VALIDATION_ERROR")
    
    # Check if category already exists
    if Category.query.filter_by(name=data['name']).first():
        return format_error("Category already exists", "CATEGORY_EXISTS")
    
    # Create new category
    category = Category(
        name=data['name'],
        description=data.get('description'),
        icon=data.get('icon')
    )
    
    # Save category to database
    db.session.add(category)
    db.session.commit()
    
    return format_response(category.to_dict(), "Category created successfully", status_code=201)

@categories_bp.route('/<int:category_id>', methods=['PUT'])
@jwt_required()
@admin_required
def update_category(category_id):
    """Update a category."""
    category = Category.query.get(category_id)
    
    if not category:
        return format_error("Category not found", "CATEGORY_NOT_FOUND", status_code=404)
    
    data = request.get_json()
    
    # Update category fields
    if 'name' in data:
        # Check if name already exists
        existing_category = Category.query.filter_by(name=data['name']).first()
        if existing_category and existing_category.id != category_id:
            return format_error("Category name already exists", "CATEGORY_EXISTS")
        
        category.name = data['name']
    
    if 'description' in data:
        category.description = data['description']
    
    if 'icon' in data:
        category.icon = data['icon']
    
    # Save changes to database
    db.session.commit()
    
    return format_response(category.to_dict(), "Category updated successfully")

@categories_bp.route('/<int:category_id>', methods=['DELETE'])
@jwt_required()
@admin_required
def delete_category(category_id):
    """Delete a category."""
    category = Category.query.get(category_id)
    
    if not category:
        return format_error("Category not found", "CATEGORY_NOT_FOUND", status_code=404)
    
    # Check if category has tools
    if category.tools:
        return format_error(
            "Cannot delete category with associated tools",
            "CATEGORY_HAS_TOOLS"
        )
    
    # Delete category from database
    db.session.delete(category)
    db.session.commit()
    
    return format_response(message="Category deleted successfully")

