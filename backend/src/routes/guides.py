from flask import Blueprint, request, jsonify
from src.models import ToolGuide, AITool
from src.database import db
from src.utils import token_required, admin_required

guides_bp = Blueprint('guides', __name__)

@guides_bp.route('/guides', methods=['GET'])
def get_guides():
    """Get all guides."""
    guides = ToolGuide.query.all()
    return jsonify([guide.to_dict() for guide in guides]), 200

@guides_bp.route('/guides/<int:guide_id>', methods=['GET'])
def get_guide(guide_id):
    """Get a specific guide."""
    guide = ToolGuide.query.get_or_404(guide_id)
    return jsonify(guide.to_dict()), 200

@guides_bp.route('/tools/<int:tool_id>/guides', methods=['GET'])
def get_tool_guides(tool_id):
    """Get all guides for a specific tool."""
    AITool.query.get_or_404(tool_id)  # Check if tool exists
    guides = ToolGuide.query.filter_by(tool_id=tool_id).order_by(ToolGuide.order_index).all()
    return jsonify([guide.to_dict() for guide in guides]), 200

@guides_bp.route('/guides', methods=['POST'])
@token_required
def create_guide(current_user):
    """Create a new guide."""
    data = request.get_json()
    
    # Validate required fields
    required_fields = ['tool_id', 'title', 'content', 'guide_type']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Missing required field: {field}'}), 400
    
    # Check if tool exists
    tool = AITool.query.get(data['tool_id'])
    if not tool:
        return jsonify({'error': 'Tool not found'}), 404
    
    # Create new guide
    guide = ToolGuide(
        tool_id=data['tool_id'],
        title=data['title'],
        content=data['content'],
        author_id=current_user.id,
        guide_type=data['guide_type'],
        order_index=data.get('order_index', 0)
    )
    
    db.session.add(guide)
    db.session.commit()
    
    return jsonify(guide.to_dict()), 201

@guides_bp.route('/guides/<int:guide_id>', methods=['PUT'])
@token_required
def update_guide(current_user, guide_id):
    """Update a guide."""
    guide = ToolGuide.query.get_or_404(guide_id)
    data = request.get_json()
    
    # Check if user is author or admin
    if guide.author_id != current_user.id and current_user.role != 'admin':
        return jsonify({'error': 'Unauthorized'}), 403
    
    # Update fields
    if 'title' in data:
        guide.title = data['title']
    if 'content' in data:
        guide.content = data['content']
    if 'guide_type' in data:
        guide.guide_type = data['guide_type']
    if 'order_index' in data:
        guide.order_index = data['order_index']
    
    db.session.commit()
    
    return jsonify(guide.to_dict()), 200

@guides_bp.route('/guides/<int:guide_id>', methods=['DELETE'])
@token_required
def delete_guide(current_user, guide_id):
    """Delete a guide."""
    guide = ToolGuide.query.get_or_404(guide_id)
    
    # Check if user is author or admin
    if guide.author_id != current_user.id and current_user.role != 'admin':
        return jsonify({'error': 'Unauthorized'}), 403
    
    db.session.delete(guide)
    db.session.commit()
    
    return jsonify({'message': 'Guide deleted successfully'}), 200

