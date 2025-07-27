"""
Review routes for the AI Directory Platform.
"""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..models import Review, AITool, User
from ..database import db
from ..utils import format_response, format_error, admin_required, paginate, subscription_required

reviews_bp = Blueprint('reviews', __name__, url_prefix='/api/v1')

@reviews_bp.route('/tools/<int:tool_id>/reviews', methods=['GET'])
def get_tool_reviews(tool_id):
    """Get reviews for a specific AI tool."""
    # Check if tool exists
    tool = AITool.query.get(tool_id)
    if not tool:
        return format_error("Tool not found", "TOOL_NOT_FOUND", status_code=404)
    
    # Get query parameters
    sort_by = request.args.get('sort', 'created_at')
    sort_order = request.args.get('order', 'desc')
    
    # Start with base query
    query = Review.query.filter_by(tool_id=tool_id)
    
    # Apply sorting
    if sort_by == 'rating':
        query = query.order_by(Review.rating.desc() if sort_order == 'desc' else Review.rating.asc())
    elif sort_by == 'created_at':
        query = query.order_by(Review.created_at.desc() if sort_order == 'desc' else Review.created_at.asc())
    
    # Paginate results
    result = paginate(query)
    
    # Format response
    reviews = [review.to_dict() for review in result['items']]
    
    return format_response({
        'reviews': reviews,
        'pagination': result['pagination']
    })

@reviews_bp.route('/tools/<int:tool_id>/reviews', methods=['POST'])
@jwt_required()
@subscription_required(min_tier='Premium')
def create_review(tool_id):
    """Create a review for an AI tool."""
    # Check if tool exists
    tool = AITool.query.get(tool_id)
    if not tool:
        return format_error("Tool not found", "TOOL_NOT_FOUND", status_code=404)
    
    data = request.get_json()
    current_user_id = get_jwt_identity()
    
    # Validate required fields
    if 'rating' not in data:
        return format_error("Rating is required", "VALIDATION_ERROR")
    
    # Validate rating range
    rating = data['rating']
    if not isinstance(rating, int) or rating < 1 or rating > 5:
        return format_error("Rating must be an integer between 1 and 5", "VALIDATION_ERROR")
    
    # Check if user already reviewed this tool
    existing_review = Review.query.filter_by(
        user_id=current_user_id,
        tool_id=tool_id
    ).first()
    
    if existing_review:
        return format_error("You have already reviewed this tool", "REVIEW_EXISTS")
    
    # Create new review
    review = Review(
        user_id=current_user_id,
        tool_id=tool_id,
        rating=rating,
        comment=data.get('comment'),
        is_verified=False
    )
    
    # Save review to database
    db.session.add(review)
    db.session.commit()
    
    # Update tool rating
    tool.update_rating()
    
    return format_response(review.to_dict(), "Review submitted successfully", status_code=201)

@reviews_bp.route('/reviews/<int:review_id>', methods=['PUT'])
@jwt_required()
def update_review(review_id):
    """Update a review."""
    review = Review.query.get(review_id)
    
    if not review:
        return format_error("Review not found", "REVIEW_NOT_FOUND", status_code=404)
    
    current_user_id = get_jwt_identity()
    
    # Check if user is the author of the review or an admin
    user = User.query.get(current_user_id)
    if review.user_id != current_user_id and not user.is_admin:
        return format_error("You are not authorized to update this review", "UNAUTHORIZED", status_code=403)
    
    data = request.get_json()
    
    # Update review fields
    if 'rating' in data:
        rating = data['rating']
        if not isinstance(rating, int) or rating < 1 or rating > 5:
            return format_error("Rating must be an integer between 1 and 5", "VALIDATION_ERROR")
        review.rating = rating
    
    if 'comment' in data:
        review.comment = data['comment']
    
    # If an admin is updating, they can update verification status
    if user.is_admin and 'is_verified' in data:
        review.is_verified = data['is_verified']
    
    # Save changes to database
    db.session.commit()
    
    # Update tool rating
    tool = AITool.query.get(review.tool_id)
    tool.update_rating()
    
    return format_response(review.to_dict(), "Review updated successfully")

@reviews_bp.route('/reviews/<int:review_id>', methods=['DELETE'])
@jwt_required()
def delete_review(review_id):
    """Delete a review."""
    review = Review.query.get(review_id)
    
    if not review:
        return format_error("Review not found", "REVIEW_NOT_FOUND", status_code=404)
    
    current_user_id = get_jwt_identity()
    
    # Check if user is the author of the review or an admin
    user = User.query.get(current_user_id)
    if review.user_id != current_user_id and not user.is_admin:
        return format_error("You are not authorized to delete this review", "UNAUTHORIZED", status_code=403)
    
    # Get tool ID before deleting the review
    tool_id = review.tool_id
    
    # Delete review from database
    db.session.delete(review)
    db.session.commit()
    
    # Update tool rating
    tool = AITool.query.get(tool_id)
    tool.update_rating()
    
    return format_response(message="Review deleted successfully")

@reviews_bp.route('/reviews/<int:review_id>/verify', methods=['PUT'])
@jwt_required()
@admin_required
def verify_review(review_id):
    """Verify a review (admin only)."""
    review = Review.query.get(review_id)
    
    if not review:
        return format_error("Review not found", "REVIEW_NOT_FOUND", status_code=404)
    
    # Update verification status
    review.is_verified = True
    db.session.commit()
    
    return format_response({
        'id': review.id,
        'is_verified': review.is_verified,
        'updated_at': review.updated_at.isoformat()
    }, "Review verified successfully")

