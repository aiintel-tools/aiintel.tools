"""
Admin routes for the AI Directory Platform.
"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy import func
from datetime import datetime, timedelta
from src.models.user import User
from src.models.ai_tool import AITool
from src.models.category import Category
from src.models.industry import Industry
from src.models.review import Review
from src.models.user_favorite import UserFavorite
from src.models.user_activity_log import UserActivityLog
from src.models.payment_transaction import PaymentTransaction
from src.models.subscription import Subscription
from src.database import db
from src.utils import format_response, format_error, admin_required

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/dashboard', methods=['GET'])
@jwt_required()
@admin_required
def get_dashboard_stats():
    """Get dashboard statistics."""
    # Get counts
    user_count = User.query.count()
    tool_count = AITool.query.count()
    review_count = Review.query.count()
    
    # Get revenue
    revenue = db.session.query(func.sum(PaymentTransaction.amount)).filter(
        PaymentTransaction.status == 'completed'
    ).scalar() or 0
    
    # Get recent users
    recent_users = User.query.order_by(User.created_at.desc()).limit(5).all()
    recent_users_data = [
        {
            'id': user.id,
            'email': user.email,
            'name': f"{user.first_name} {user.last_name}",
            'subscription_tier': user.subscription_tier,
            'created_at': user.created_at.isoformat() if user.created_at else None
        }
        for user in recent_users
    ]
    
    # Get recent tools
    recent_tools = AITool.query.order_by(AITool.created_at.desc()).limit(5).all()
    recent_tools_data = [
        {
            'id': tool.id,
            'name': tool.name,
            'category': tool.category.name if tool.category else None,
            'access_level': tool.access_level,
            'created_at': tool.created_at.isoformat() if tool.created_at else None
        }
        for tool in recent_tools
    ]
    
    return format_response({
        'counts': {
            'users': user_count,
            'tools': tool_count,
            'reviews': review_count,
            'revenue': round(revenue, 2)
        },
        'recent_users': recent_users_data,
        'recent_tools': recent_tools_data
    })

@admin_bp.route('/users/stats', methods=['GET'])
@jwt_required()
@admin_required
def get_user_stats():
    """Get user statistics."""
    # Get query parameters
    days = int(request.args.get('days', 30))
    
    # Calculate date range
    end_date = datetime.utcnow()
    start_date = end_date - timedelta(days=days)
    
    # Get daily signups
    daily_signups = []
    current_date = start_date
    
    while current_date <= end_date:
        next_date = current_date + timedelta(days=1)
        
        count = User.query.filter(
            User.created_at >= current_date,
            User.created_at < next_date
        ).count()
        
        daily_signups.append({
            'date': current_date.strftime('%Y-%m-%d'),
            'count': count
        })
        
        current_date = next_date
    
    # Get subscription distribution
    subscription_distribution = [
        {
            'name': 'Free',
            'count': User.query.filter_by(subscription_tier='Free').count()
        },
        {
            'name': 'Premium',
            'count': User.query.filter_by(subscription_tier='Premium').count()
        },
        {
            'name': 'Business',
            'count': User.query.filter_by(subscription_tier='Business').count()
        }
    ]
    
    return format_response({
        'daily_signups': daily_signups,
        'subscription_distribution': subscription_distribution
    })

@admin_bp.route('/tools/stats', methods=['GET'])
@jwt_required()
@admin_required
def get_tool_stats():
    """Get tool statistics."""
    # Get category distribution
    categories = Category.query.all()
    category_distribution = []
    
    for category in categories:
        count = AITool.query.filter_by(category_id=category.id).count()
        category_distribution.append({
            'name': category.name,
            'count': count
        })
    
    # Get access level distribution
    access_level_distribution = [
        {
            'name': 'Public',
            'count': AITool.query.filter_by(access_level='Public').count()
        },
        {
            'name': 'Premium Only',
            'count': AITool.query.filter_by(access_level='Premium Only').count()
        },
        {
            'name': 'Business Only',
            'count': AITool.query.filter_by(access_level='Business Only').count()
        }
    ]
    
    # Get top rated tools
    top_rated_tools = AITool.query.order_by(AITool.rating.desc()).limit(5).all()
    top_rated = [
        {
            'id': tool.id,
            'name': tool.name,
            'rating': tool.rating,
            'category': tool.category.name if tool.category else None
        }
        for tool in top_rated_tools
    ]
    
    # Get most favorited tools
    most_favorited_subquery = db.session.query(
        UserFavorite.tool_id,
        func.count(UserFavorite.id).label('favorite_count')
    ).group_by(UserFavorite.tool_id).subquery()
    
    most_favorited_tools = db.session.query(
        AITool, most_favorited_subquery.c.favorite_count
    ).join(
        most_favorited_subquery,
        AITool.id == most_favorited_subquery.c.tool_id
    ).order_by(
        most_favorited_subquery.c.favorite_count.desc()
    ).limit(5).all()
    
    most_favorited = [
        {
            'id': tool.id,
            'name': tool.name,
            'favorite_count': favorite_count,
            'category': tool.category.name if tool.category else None
        }
        for tool, favorite_count in most_favorited_tools
    ]
    
    return format_response({
        'category_distribution': category_distribution,
        'access_level_distribution': access_level_distribution,
        'top_rated': top_rated,
        'most_favorited': most_favorited
    })

@admin_bp.route('/revenue/stats', methods=['GET'])
@jwt_required()
@admin_required
def get_revenue_stats():
    """Get revenue statistics."""
    # Get query parameters
    days = int(request.args.get('days', 30))
    
    # Calculate date range
    end_date = datetime.utcnow()
    start_date = end_date - timedelta(days=days)
    
    # Get daily revenue
    daily_revenue = []
    current_date = start_date
    
    while current_date <= end_date:
        next_date = current_date + timedelta(days=1)
        
        amount = db.session.query(func.sum(PaymentTransaction.amount)).filter(
            PaymentTransaction.transaction_date >= current_date,
            PaymentTransaction.transaction_date < next_date,
            PaymentTransaction.status == 'completed'
        ).scalar() or 0
        
        daily_revenue.append({
            'date': current_date.strftime('%Y-%m-%d'),
            'amount': round(amount, 2)
        })
        
        current_date = next_date
    
    # Get revenue by subscription tier
    revenue_by_tier = []
    
    for tier in ['Premium', 'Business']:
        amount = db.session.query(func.sum(PaymentTransaction.amount)).filter(
            PaymentTransaction.subscription_tier == tier,
            PaymentTransaction.transaction_date >= start_date,
            PaymentTransaction.status == 'completed'
        ).scalar() or 0
        
        revenue_by_tier.append({
            'name': tier,
            'amount': round(amount, 2)
        })
    
    return format_response({
        'daily_revenue': daily_revenue,
        'revenue_by_tier': revenue_by_tier
    })

