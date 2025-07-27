"""
Admin routes for the AI Directory Platform.
"""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy import func
from datetime import datetime, timedelta
from ..models import (
    User, AITool, Category, Industry, Review, 
    UserFavorite, UserActivityLog, PaymentTransaction, Subscription
)
from ..database import db
from ..utils import format_response, format_error, admin_required

admin_bp = Blueprint('admin', __name__, url_prefix='/api/v1/admin')

@admin_bp.route('/dashboard', methods=['GET'])
@jwt_required()
@admin_required
def get_dashboard():
    """Get admin dashboard statistics."""
    # Get user statistics
    total_users = User.query.count()
    new_users_today = User.query.filter(
        User.created_at >= datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
    ).count()
    new_users_week = User.query.filter(
        User.created_at >= datetime.utcnow() - timedelta(days=7)
    ).count()
    new_users_month = User.query.filter(
        User.created_at >= datetime.utcnow() - timedelta(days=30)
    ).count()
    
    # Get subscription statistics
    free_users = User.query.filter_by(subscription_tier='Free').count()
    premium_users = User.query.filter_by(subscription_tier='Premium').count()
    business_users = User.query.filter_by(subscription_tier='Business').count()
    
    # Get tool statistics
    total_tools = AITool.query.count()
    public_tools = AITool.query.filter_by(access_level='Public').count()
    premium_tools = AITool.query.filter_by(access_level='Premium Only').count()
    business_tools = AITool.query.filter_by(access_level='Business Only').count()
    
    # Get review statistics
    total_reviews = Review.query.count()
    verified_reviews = Review.query.filter_by(is_verified=True).count()
    
    # Get revenue statistics
    month_start = datetime.utcnow().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    last_month_start = (month_start - timedelta(days=1)).replace(day=1)
    
    monthly_revenue = db.session.query(func.sum(PaymentTransaction.amount)).filter(
        PaymentTransaction.transaction_date >= month_start,
        PaymentTransaction.status == 'completed'
    ).scalar() or 0
    
    last_month_revenue = db.session.query(func.sum(PaymentTransaction.amount)).filter(
        PaymentTransaction.transaction_date >= last_month_start,
        PaymentTransaction.transaction_date < month_start,
        PaymentTransaction.status == 'completed'
    ).scalar() or 0
    
    # Calculate growth rates
    user_growth = ((new_users_month / total_users) * 100) if total_users > 0 else 0
    revenue_growth = ((monthly_revenue / last_month_revenue) * 100 - 100) if last_month_revenue > 0 else 0
    
    return format_response({
        'users': {
            'total': total_users,
            'new_today': new_users_today,
            'new_week': new_users_week,
            'new_month': new_users_month,
            'growth_rate': round(user_growth, 2)
        },
        'subscriptions': {
            'free': free_users,
            'premium': premium_users,
            'business': business_users
        },
        'tools': {
            'total': total_tools,
            'public': public_tools,
            'premium': premium_tools,
            'business': business_tools
        },
        'reviews': {
            'total': total_reviews,
            'verified': verified_reviews
        },
        'revenue': {
            'monthly': round(monthly_revenue, 2),
            'last_month': round(last_month_revenue, 2),
            'growth_rate': round(revenue_growth, 2)
        }
    })

@admin_bp.route('/activity', methods=['GET'])
@jwt_required()
@admin_required
def get_activity():
    """Get recent user activity."""
    # Get query parameters
    days = int(request.args.get('days', 7))
    limit = int(request.args.get('limit', 20))
    
    # Get recent activity
    activity = UserActivityLog.query.order_by(
        UserActivityLog.created_at.desc()
    ).limit(limit).all()
    
    # Format response
    activity_list = []
    for log in activity:
        user = User.query.get(log.user_id)
        if user:
            activity_list.append({
                'id': log.id,
                'user': {
                    'id': user.id,
                    'email': user.email,
                    'first_name': user.first_name,
                    'last_name': user.last_name
                },
                'activity_type': log.activity_type,
                'details': log.details,
                'created_at': log.created_at.isoformat()
            })
    
    return format_response(activity_list)

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
    
    # Get daily user signups
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

