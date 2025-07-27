"""
Subscription routes for the AI Directory Platform.
"""

from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime, timedelta
from ..models import User, Subscription, PaymentTransaction
from ..database import db
from ..utils import format_response, format_error, admin_required

subscriptions_bp = Blueprint('subscriptions', __name__, url_prefix='/api/v1/subscriptions')

@subscriptions_bp.route('/plans', methods=['GET'])
def get_subscription_plans():
    """Get available subscription plans."""
    plans = current_app.config['SUBSCRIPTION_PLANS']
    
    return format_response(list(plans.values()))

@subscriptions_bp.route('/subscribe', methods=['POST'])
@jwt_required()
def subscribe():
    """Subscribe to a plan."""
    data = request.get_json()
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    
    if not user:
        return format_error("User not found", "USER_NOT_FOUND", status_code=404)
    
    # Validate required fields
    if not data.get('plan_id'):
        return format_error("Plan ID is required", "VALIDATION_ERROR")
    
    # Check if plan exists
    plan_id = data['plan_id']
    plans = current_app.config['SUBSCRIPTION_PLANS']
    
    if plan_id not in plans:
        return format_error("Invalid plan ID", "INVALID_PLAN")
    
    plan = plans[plan_id]
    
    # If plan is free, just update the user's subscription tier
    if plan['price'] == 0:
        user.subscription_tier = plan['name']
        user.subscription_start_date = datetime.utcnow()
        user.subscription_end_date = None
        
        db.session.commit()
        
        return format_response({
            'subscription_id': None,
            'plan': {
                'id': plan_id,
                'name': plan['name']
            },
            'status': 'active',
            'current_period_start': user.subscription_start_date.isoformat(),
            'current_period_end': None
        }, "Subscription created successfully")
    
    # For paid plans, we would integrate with a payment processor like Stripe
    # For now, we'll simulate a successful payment
    
    # Create a subscription record
    current_date = datetime.utcnow()
    end_date = current_date + timedelta(days=30)
    
    subscription = Subscription(
        user_id=current_user_id,
        plan_id=plan_id,
        status='active',
        current_period_start=current_date,
        current_period_end=end_date,
        cancel_at_period_end=False,
        payment_method_id=data.get('payment_method_id')
    )
    
    # Create a payment transaction record
    transaction = PaymentTransaction(
        user_id=current_user_id,
        amount=plan['price'],
        currency=plan['currency'],
        status='completed',
        payment_method=data.get('payment_method_id'),
        subscription_tier=plan['name'],
        transaction_date=current_date
    )
    
    # Update user's subscription tier
    user.subscription_tier = plan['name']
    user.subscription_start_date = current_date
    user.subscription_end_date = end_date
    
    # Save changes to database
    db.session.add(subscription)
    db.session.add(transaction)
    db.session.commit()
    
    return format_response({
        'subscription_id': subscription.id,
        'plan': {
            'id': plan_id,
            'name': plan['name']
        },
        'status': 'active',
        'current_period_start': subscription.current_period_start.isoformat(),
        'current_period_end': subscription.current_period_end.isoformat()
    }, "Subscription created successfully")

@subscriptions_bp.route('/me', methods=['GET'])
@jwt_required()
def get_current_subscription():
    """Get the current user's subscription."""
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    
    if not user:
        return format_error("User not found", "USER_NOT_FOUND", status_code=404)
    
    # Get the user's subscription
    subscription = Subscription.query.filter_by(
        user_id=current_user_id,
        status='active'
    ).first()
    
    if not subscription:
        # If no active subscription, return the user's subscription tier
        return format_response({
            'subscription_id': None,
            'plan': {
                'id': 'free',
                'name': user.subscription_tier
            },
            'status': 'active',
            'current_period_start': user.subscription_start_date.isoformat() if user.subscription_start_date else None,
            'current_period_end': user.subscription_end_date.isoformat() if user.subscription_end_date else None,
            'cancel_at_period_end': False
        })
    
    # Get the payment method
    payment_transaction = PaymentTransaction.query.filter_by(
        user_id=current_user_id
    ).order_by(PaymentTransaction.transaction_date.desc()).first()
    
    payment_method = None
    if payment_transaction and payment_transaction.payment_method:
        # In a real implementation, we would get the payment method details from the payment processor
        payment_method = {
            'brand': 'visa',
            'last4': '4242',
            'exp_month': 12,
            'exp_year': 2025
        }
    
    return format_response({
        'subscription_id': subscription.id,
        'plan': {
            'id': subscription.plan_id,
            'name': user.subscription_tier
        },
        'status': subscription.status,
        'current_period_start': subscription.current_period_start.isoformat(),
        'current_period_end': subscription.current_period_end.isoformat(),
        'cancel_at_period_end': subscription.cancel_at_period_end,
        'payment_method': payment_method
    })

@subscriptions_bp.route('/cancel', methods=['POST'])
@jwt_required()
def cancel_subscription():
    """Cancel the current user's subscription."""
    data = request.get_json()
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    
    if not user:
        return format_error("User not found", "USER_NOT_FOUND", status_code=404)
    
    # Get the user's subscription
    subscription = Subscription.query.filter_by(
        user_id=current_user_id,
        status='active'
    ).first()
    
    if not subscription:
        return format_error("No active subscription found", "NO_SUBSCRIPTION", status_code=404)
    
    # Check if immediate cancellation is requested
    cancel_immediately = data.get('cancel_immediately', False)
    
    if cancel_immediately:
        # Update subscription status
        subscription.status = 'canceled'
        
        # Update user's subscription tier
        user.subscription_tier = 'Free'
        user.subscription_end_date = datetime.utcnow()
        
        db.session.commit()
        
        return format_response({
            'subscription_id': subscription.id,
            'status': 'canceled',
            'cancel_at_period_end': False
        }, "Subscription canceled immediately")
    else:
        # Set subscription to cancel at the end of the period
        subscription.cancel_at_period_end = True
        
        db.session.commit()
        
        return format_response({
            'subscription_id': subscription.id,
            'status': 'active',
            'cancel_at_period_end': True,
            'current_period_end': subscription.current_period_end.isoformat()
        }, "Subscription will be canceled at the end of the billing period")

@subscriptions_bp.route('/admin/subscriptions', methods=['GET'])
@jwt_required()
@admin_required
def get_all_subscriptions():
    """Get all subscriptions (admin only)."""
    # Get query parameters
    status = request.args.get('status')
    plan_id = request.args.get('plan_id')
    
    # Start with base query
    query = Subscription.query
    
    # Apply filters
    if status:
        query = query.filter(Subscription.status == status)
    
    if plan_id:
        query = query.filter(Subscription.plan_id == plan_id)
    
    # Get all subscriptions
    subscriptions = query.all()
    
    # Format response
    subscription_list = [subscription.to_dict() for subscription in subscriptions]
    
    return format_response(subscription_list)

