"""
AI Tools routes for the AI Directory Platform.
"""

from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy import or_
from ..models import AITool, Category, Industry, ToolIndustry, User, ToolGuide
from ..database import db
from ..utils import (
    format_response, format_error, admin_required, 
    subscription_required, paginate, save_image, delete_image
)
import json

tools_bp = Blueprint('tools', __name__, url_prefix='/api/v1/tools')

@tools_bp.route('', methods=['GET'])
def get_tools():
    """Get a list of AI tools."""
    # Get query parameters
    search = request.args.get('search', '')
    category_id = request.args.get('category_id')
    industry_id = request.args.get('industry_id')
    access_level = request.args.get('access_level')
    sort_by = request.args.get('sort', 'name')
    sort_order = request.args.get('order', 'asc')
    
    # Start with base query
    query = AITool.query
    
    # Apply search filter
    if search:
        query = query.filter(
            or_(
                AITool.name.ilike(f'%{search}%'),
                AITool.description.ilike(f'%{search}%')
            )
        )
    
    # Apply category filter
    if category_id:
        query = query.filter(AITool.category_id == category_id)
    
    # Apply industry filter
    if industry_id:
        query = query.join(AITool.industries).filter(Industry.id == industry_id)
    
    # Apply access level filter
    if access_level:
        query = query.filter(AITool.access_level == access_level)
    
    # Apply sorting
    if sort_by == 'name':
        query = query.order_by(AITool.name.asc() if sort_order == 'asc' else AITool.name.desc())
    elif sort_by == 'rating':
        query = query.order_by(AITool.rating.desc() if sort_order == 'asc' else AITool.rating.asc())
    elif sort_by == 'created_at':
        query = query.order_by(AITool.created_at.desc() if sort_order == 'asc' else AITool.created_at.asc())
    
    # Paginate results
    result = paginate(query)
    
    # Format response
    tools = [tool.to_dict() for tool in result['items']]
    
    return format_response({
        'tools': tools,
        'pagination': result['pagination']
    })

@tools_bp.route('/<int:tool_id>', methods=['GET'])
def get_tool(tool_id):
    """Get a specific AI tool by ID."""
    tool = AITool.query.get(tool_id)
    
    if not tool:
        return format_error("Tool not found", "TOOL_NOT_FOUND", status_code=404)
    
    # Check if user is authenticated and has access to the tool
    current_user_id = None
    try:
        from flask_jwt_extended import get_jwt_identity
        current_user_id = get_jwt_identity()
    except:
        pass
    
    # If tool is not public, check if user has access
    if tool.access_level != 'Public' and current_user_id:
        user = User.query.get(current_user_id)
        if not user:
            return format_error("Tool access restricted", "ACCESS_RESTRICTED", status_code=403)
        
        # Check subscription tier
        if tool.access_level == 'Premium Only' and user.subscription_tier not in ['Premium', 'Business']:
            return format_error("Premium subscription required", "SUBSCRIPTION_REQUIRED", status_code=403)
        
        if tool.access_level == 'Business Only' and user.subscription_tier != 'Business':
            return format_error("Business subscription required", "SUBSCRIPTION_REQUIRED", status_code=403)
    elif tool.access_level != 'Public' and not current_user_id:
        return format_error("Authentication required", "AUTHENTICATION_REQUIRED", status_code=401)
    
    # Return tool details with reviews
    return format_response(tool.to_dict(include_reviews=True))

@tools_bp.route('', methods=['POST'])
@jwt_required()
@admin_required
def create_tool():
    """Create a new AI tool."""
    # Check if request has the multipart/form-data content type
    if 'multipart/form-data' not in request.content_type:
        return format_error("Content-Type must be multipart/form-data", "INVALID_CONTENT_TYPE")
    
    # Validate required fields
    required_fields = ['name', 'description', 'category_id', 'access_level']
    for field in required_fields:
        if field not in request.form:
            return format_error(f"Missing required field: {field}", "VALIDATION_ERROR")
    
    # Check if category exists
    category_id = request.form.get('category_id')
    category = Category.query.get(category_id)
    if not category:
        return format_error("Category not found", "CATEGORY_NOT_FOUND", status_code=404)
    
    # Process image upload
    image_path = None
    if 'image' in request.files and request.files['image'].filename:
        try:
            image_path = save_image(request.files['image'], 'tool_images')
        except ValueError as e:
            return format_error(str(e), "INVALID_FILE")
    
    # Parse price point details if provided
    price_point_details = {}
    if 'price_point_details' in request.form:
        try:
            price_point_details = json.loads(request.form.get('price_point_details'))
        except json.JSONDecodeError:
            return format_error("Invalid price point details format", "VALIDATION_ERROR")
    
    # Create new tool
    tool = AITool(
        name=request.form.get('name'),
        description=request.form.get('description'),
        category_id=category_id,
        website_url=request.form.get('website_url'),
        image_path=image_path,
        access_level=request.form.get('access_level'),
        # New fields
        business_utility=request.form.get('business_utility', ''),
        price_point_type=request.form.get('price_point_type', ''),
        price_point_details=price_point_details
    )
    
    # Save tool to database
    db.session.add(tool)
    db.session.commit()
    
    # Process industry associations
    industry_ids = request.form.getlist('industry_ids')
    if industry_ids:
        for industry_id in industry_ids:
            industry = Industry.query.get(industry_id)
            if industry:
                tool_industry = ToolIndustry(
                    tool_id=tool.id,
                    industry_id=industry.id
                )
                db.session.add(tool_industry)
        
        db.session.commit()
    
    # Process guides if provided
    guides_json = request.form.get('guides', '[]')
    try:
        guides_data = json.loads(guides_json)
        if isinstance(guides_data, list):
            current_user_id = get_jwt_identity()
            for guide_data in guides_data:
                guide = ToolGuide(
                    tool_id=tool.id,
                    title=guide_data.get('title', ''),
                    content=guide_data.get('content', ''),
                    author_id=current_user_id,
                    guide_type=guide_data.get('guide_type', 'Tutorial'),
                    order_index=guide_data.get('order_index', 0)
                )
                db.session.add(guide)
            
            db.session.commit()
    except json.JSONDecodeError:
        # Just log the error but don't fail the request
        current_app.logger.error("Failed to parse guides JSON")
    
    # Return tool data
    return format_response(tool.to_dict(), "Tool created successfully", status_code=201)

@tools_bp.route('/<int:tool_id>', methods=['PUT'])
@jwt_required()
@admin_required
def update_tool(tool_id):
    """Update an existing AI tool."""
    tool = AITool.query.get(tool_id)
    
    if not tool:
        return format_error("Tool not found", "TOOL_NOT_FOUND", status_code=404)
    
    # Check if request has the multipart/form-data content type
    if 'multipart/form-data' not in request.content_type:
        return format_error("Content-Type must be multipart/form-data", "INVALID_CONTENT_TYPE")
    
    # Update tool fields
    if 'name' in request.form:
        tool.name = request.form.get('name')
    
    if 'description' in request.form:
        tool.description = request.form.get('description')
    
    if 'category_id' in request.form:
        category_id = request.form.get('category_id')
        category = Category.query.get(category_id)
        if not category:
            return format_error("Category not found", "CATEGORY_NOT_FOUND", status_code=404)
        tool.category_id = category_id
    
    if 'website_url' in request.form:
        tool.website_url = request.form.get('website_url')
    
    if 'access_level' in request.form:
        tool.access_level = request.form.get('access_level')
    
    # Update new fields
    if 'business_utility' in request.form:
        tool.business_utility = request.form.get('business_utility')
    
    if 'price_point_type' in request.form:
        tool.price_point_type = request.form.get('price_point_type')
    
    if 'price_point_details' in request.form:
        try:
            tool.price_point_details = json.loads(request.form.get('price_point_details'))
        except json.JSONDecodeError:
            return format_error("Invalid price point details format", "VALIDATION_ERROR")
    
    # Process image upload
    if 'image' in request.files and request.files['image'].filename:
        try:
            # Delete old image if it exists
            if tool.image_path:
                delete_image(tool.image_path)
            
            # Save new image
            tool.image_path = save_image(request.files['image'], 'tool_images')
        except ValueError as e:
            return format_error(str(e), "INVALID_FILE")
    
    # Update industry associations
    industry_ids = request.form.getlist('industry_ids')
    if industry_ids:
        # Remove existing associations
        ToolIndustry.query.filter_by(tool_id=tool.id).delete()
        
        # Add new associations
        for industry_id in industry_ids:
            industry = Industry.query.get(industry_id)
            if industry:
                tool_industry = ToolIndustry(
                    tool_id=tool.id,
                    industry_id=industry.id
                )
                db.session.add(tool_industry)
    
    # Save changes to database
    db.session.commit()
    
    # Return updated tool data
    return format_response(tool.to_dict(), "Tool updated successfully")

@tools_bp.route('/<int:tool_id>', methods=['DELETE'])
@jwt_required()
@admin_required
def delete_tool(tool_id):
    """Delete an AI tool."""
    tool = AITool.query.get(tool_id)
    
    if not tool:
        return format_error("Tool not found", "TOOL_NOT_FOUND", status_code=404)
    
    # Delete image if it exists
    if tool.image_path:
        delete_image(tool.image_path)
    
    # Delete tool from database
    db.session.delete(tool)
    db.session.commit()
    
    return format_response(message="Tool deleted successfully")

@tools_bp.route('/<int:tool_id>/favorite', methods=['POST'])
@jwt_required()
@subscription_required(min_tier='Premium')
def add_favorite(tool_id):
    """Add an AI tool to the user's favorites."""
    from ..models import UserFavorite
    
    current_user_id = get_jwt_identity()
    tool = AITool.query.get(tool_id)
    
    if not tool:
        return format_error("Tool not found", "TOOL_NOT_FOUND", status_code=404)
    
    # Check if already favorited
    existing_favorite = UserFavorite.query.filter_by(
        user_id=current_user_id,
        tool_id=tool_id
    ).first()
    
    if existing_favorite:
        return format_error("Tool already in favorites", "ALREADY_FAVORITED")
    
    # Add to favorites
    favorite = UserFavorite(
        user_id=current_user_id,
        tool_id=tool_id
    )
    
    db.session.add(favorite)
    db.session.commit()
    
    return format_response({
        'id': favorite.id,
        'tool_id': tool_id,
        'created_at': favorite.created_at.isoformat()
    }, "Tool added to favorites")

@tools_bp.route('/<int:tool_id>/favorite', methods=['DELETE'])
@jwt_required()
def remove_favorite(tool_id):
    """Remove an AI tool from the user's favorites."""
    from ..models import UserFavorite
    
    current_user_id = get_jwt_identity()
    
    # Find the favorite
    favorite = UserFavorite.query.filter_by(
        user_id=current_user_id,
        tool_id=tool_id
    ).first()
    
    if not favorite:
        return format_error("Tool not in favorites", "NOT_FAVORITED", status_code=404)
    
    # Remove from favorites
    db.session.delete(favorite)
    db.session.commit()
    
    return format_response(message="Tool removed from favorites")

@tools_bp.route('/<int:tool_id>/guides', methods=['GET'])
def get_tool_guides(tool_id):
    """Get all guides for a specific tool."""
    tool = AITool.query.get(tool_id)
    
    if not tool:
        return format_error("Tool not found", "TOOL_NOT_FOUND", status_code=404)
    
    guides = ToolGuide.query.filter_by(tool_id=tool_id).order_by(ToolGuide.order_index).all()
    
    return format_response({
        'guides': [guide.to_dict() for guide in guides]
    })

@tools_bp.route('/<int:tool_id>/guides', methods=['POST'])
@jwt_required()
@admin_required
def create_tool_guide(tool_id):
    """Create a new guide for a tool."""
    tool = AITool.query.get(tool_id)
    
    if not tool:
        return format_error("Tool not found", "TOOL_NOT_FOUND", status_code=404)
    
    data = request.get_json()
    
    # Validate required fields
    required_fields = ['title', 'content', 'guide_type']
    for field in required_fields:
        if field not in data:
            return format_error(f"Missing required field: {field}", "VALIDATION_ERROR")
    
    # Create new guide
    guide = ToolGuide(
        tool_id=tool_id,
        title=data['title'],
        content=data['content'],
        author_id=get_jwt_identity(),
        guide_type=data['guide_type'],
        order_index=data.get('order_index', 0)
    )
    
    db.session.add(guide)
    db.session.commit()
    
    return format_response(guide.to_dict(), "Guide created successfully", status_code=201)

