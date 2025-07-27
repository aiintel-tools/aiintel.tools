"""
Industry routes for the AI Directory Platform.
"""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from ..models import Industry
from ..database import db
from ..utils import format_response, format_error, admin_required

industries_bp = Blueprint('industries', __name__, url_prefix='/api/v1/industries')

@industries_bp.route('', methods=['GET'])
def get_industries():
    """Get a list of all industries."""
    industries = Industry.query.all()
    
    # Format response
    industry_list = [industry.to_dict() for industry in industries]
    
    return format_response(industry_list)

@industries_bp.route('/<int:industry_id>', methods=['GET'])
def get_industry(industry_id):
    """Get a specific industry by ID."""
    industry = Industry.query.get(industry_id)
    
    if not industry:
        return format_error("Industry not found", "INDUSTRY_NOT_FOUND", status_code=404)
    
    return format_response(industry.to_dict())

@industries_bp.route('', methods=['POST'])
@jwt_required()
@admin_required
def create_industry():
    """Create a new industry."""
    data = request.get_json()
    
    # Validate required fields
    if not data.get('name'):
        return format_error("Name is required", "VALIDATION_ERROR")
    
    # Check if industry already exists
    if Industry.query.filter_by(name=data['name']).first():
        return format_error("Industry already exists", "INDUSTRY_EXISTS")
    
    # Create new industry
    industry = Industry(
        name=data['name'],
        description=data.get('description')
    )
    
    # Save industry to database
    db.session.add(industry)
    db.session.commit()
    
    return format_response(industry.to_dict(), "Industry created successfully", status_code=201)

@industries_bp.route('/<int:industry_id>', methods=['PUT'])
@jwt_required()
@admin_required
def update_industry(industry_id):
    """Update an industry."""
    industry = Industry.query.get(industry_id)
    
    if not industry:
        return format_error("Industry not found", "INDUSTRY_NOT_FOUND", status_code=404)
    
    data = request.get_json()
    
    # Update industry fields
    if 'name' in data:
        # Check if name already exists
        existing_industry = Industry.query.filter_by(name=data['name']).first()
        if existing_industry and existing_industry.id != industry_id:
            return format_error("Industry name already exists", "INDUSTRY_EXISTS")
        
        industry.name = data['name']
    
    if 'description' in data:
        industry.description = data['description']
    
    # Save changes to database
    db.session.commit()
    
    return format_response(industry.to_dict(), "Industry updated successfully")

@industries_bp.route('/<int:industry_id>', methods=['DELETE'])
@jwt_required()
@admin_required
def delete_industry(industry_id):
    """Delete an industry."""
    industry = Industry.query.get(industry_id)
    
    if not industry:
        return format_error("Industry not found", "INDUSTRY_NOT_FOUND", status_code=404)
    
    # Check if industry has associated users or tools
    if industry.users or industry.tools:
        return format_error(
            "Cannot delete industry with associated users or tools",
            "INDUSTRY_HAS_ASSOCIATIONS"
        )
    
    # Delete industry from database
    db.session.delete(industry)
    db.session.commit()
    
    return format_response(message="Industry deleted successfully")

