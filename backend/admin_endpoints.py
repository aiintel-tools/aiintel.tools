from flask import Blueprint, jsonify, request

admin_bp = Blueprint('admin', __name__, url_prefix='/api/admin')

# Mock admin user for demonstration
ADMIN_USER = {
    "email": "admin@aidirectory.com",
    "password": "admin123",
    "name": "Admin User",
    "role": "admin"
}

@admin_bp.route('/login', methods=['POST'])
def admin_login():
    """Admin login endpoint"""
    data = request.get_json()
    
    if not data:
        return jsonify({
            "success": False,
            "message": "Missing request data"
        }), 400
    
    email = data.get('email')
    password = data.get('password')
    
    if not email or not password:
        return jsonify({
            "success": False,
            "message": "Email and password are required"
        }), 400
    
    # Check against mock admin user
    if email == ADMIN_USER['email'] and password == ADMIN_USER['password']:
        return jsonify({
            "success": True,
            "message": "Admin login successful",
            "token": "mock-admin-jwt-token",
            "user": {
                "name": ADMIN_USER['name'],
                "email": ADMIN_USER['email'],
                "role": ADMIN_USER['role']
            }
        }), 200
    else:
        return jsonify({
            "success": False,
            "message": "Invalid email or password"
        }), 401

@admin_bp.route('/dashboard', methods=['GET'])
def admin_dashboard():
    """Admin dashboard data endpoint"""
    # Check for authorization header
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        return jsonify({
            "success": False,
            "message": "Unauthorized access"
        }), 401
    
    # In a real app, we would validate the JWT token here
    # For demo purposes, we'll just check if it's our mock token
    token = auth_header.split(' ')[1]
    if token != "mock-admin-jwt-token":
        return jsonify({
            "success": False,
            "message": "Invalid token"
        }), 401
    
    # Return mock dashboard data
    return jsonify({
        "success": True,
        "stats": {
            "users": {
                "total": 15482,
                "active": 12345,
                "new_today": 127,
                "growth": 12.5
            },
            "tools": {
                "total": 253,
                "pending": 14,
                "featured": 12,
                "new_today": 5
            },
            "subscriptions": {
                "free": 13245,
                "premium": 1850,
                "business": 387,
                "revenue_monthly": 28743
            },
            "reviews": {
                "total": 8543,
                "pending": 87,
                "average_rating": 4.2,
                "new_today": 34
            }
        },
        "recent_activity": [
            {
                "type": "user_registration",
                "user": "john.doe@example.com",
                "timestamp": "2025-07-23T08:12:34Z"
            },
            {
                "type": "tool_submission",
                "tool": "AI Code Helper",
                "user": "developer@techco.com",
                "timestamp": "2025-07-23T07:45:12Z"
            },
            {
                "type": "subscription_upgrade",
                "user": "marketing@company.com",
                "plan": "business",
                "timestamp": "2025-07-23T06:30:45Z"
            },
            {
                "type": "review_submission",
                "tool": "ChatGPT",
                "user": "writer@content.com",
                "rating": 5,
                "timestamp": "2025-07-23T05:22:18Z"
            },
            {
                "type": "user_registration",
                "user": "designer@studio.com",
                "timestamp": "2025-07-23T04:55:39Z"
            }
        ],
        "system_status": {
            "api": "healthy",
            "database": "healthy",
            "payments": "healthy",
            "email": "healthy"
        }
    }), 200

@admin_bp.route('/users', methods=['GET'])
def admin_users():
    """Admin users management endpoint"""
    # Check for authorization header
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        return jsonify({
            "success": False,
            "message": "Unauthorized access"
        }), 401
    
    # Mock user data
    return jsonify({
        "success": True,
        "users": [
            {
                "id": 1,
                "name": "John Doe",
                "email": "john.doe@example.com",
                "subscription": "premium",
                "joined": "2025-06-15T10:30:00Z",
                "last_login": "2025-07-22T14:25:12Z",
                "status": "active"
            },
            {
                "id": 2,
                "name": "Jane Smith",
                "email": "jane.smith@company.com",
                "subscription": "business",
                "joined": "2025-05-22T08:45:00Z",
                "last_login": "2025-07-23T09:10:05Z",
                "status": "active"
            },
            {
                "id": 3,
                "name": "Robert Johnson",
                "email": "robert@techfirm.com",
                "subscription": "free",
                "joined": "2025-07-10T16:20:00Z",
                "last_login": "2025-07-20T11:30:45Z",
                "status": "active"
            },
            {
                "id": 4,
                "name": "Emily Davis",
                "email": "emily@design.co",
                "subscription": "premium",
                "joined": "2025-04-05T09:15:00Z",
                "last_login": "2025-07-21T15:40:22Z",
                "status": "active"
            },
            {
                "id": 5,
                "name": "Michael Wilson",
                "email": "michael@agency.net",
                "subscription": "business",
                "joined": "2025-06-30T11:50:00Z",
                "last_login": "2025-07-23T08:05:18Z",
                "status": "active"
            }
        ],
        "total": 15482,
        "page": 1,
        "per_page": 5,
        "total_pages": 3097
    }), 200

@admin_bp.route('/tools', methods=['GET'])
def admin_tools():
    """Admin tools management endpoint"""
    # Check for authorization header
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        return jsonify({
            "success": False,
            "message": "Unauthorized access"
        }), 401
    
    # Mock tools data
    return jsonify({
        "success": True,
        "tools": [
            {
                "id": 1,
                "name": "ChatGPT",
                "slug": "chatgpt",
                "category": "Conversational AI",
                "rating_average": 4.8,
                "reviews_count": 1245,
                "pricing_model": "freemium",
                "status": "approved",
                "is_featured": True,
                "submitted_by": "openai@example.com",
                "submitted_date": "2025-01-15T10:30:00Z"
            },
            {
                "id": 2,
                "name": "Midjourney",
                "slug": "midjourney",
                "category": "Image Generation",
                "rating_average": 4.7,
                "reviews_count": 987,
                "pricing_model": "subscription",
                "status": "approved",
                "is_featured": True,
                "submitted_by": "midjourney@example.com",
                "submitted_date": "2025-01-20T14:45:00Z"
            },
            {
                "id": 3,
                "name": "GitHub Copilot",
                "slug": "github-copilot",
                "category": "Code Assistant",
                "rating_average": 4.6,
                "reviews_count": 856,
                "pricing_model": "subscription",
                "status": "approved",
                "is_featured": True,
                "submitted_by": "github@example.com",
                "submitted_date": "2025-02-05T09:15:00Z"
            },
            {
                "id": 4,
                "name": "AI Code Helper",
                "slug": "ai-code-helper",
                "category": "Code Assistant",
                "rating_average": 0,
                "reviews_count": 0,
                "pricing_model": "freemium",
                "status": "pending",
                "is_featured": False,
                "submitted_by": "developer@techco.com",
                "submitted_date": "2025-07-23T07:45:12Z"
            },
            {
                "id": 5,
                "name": "Content Wizard",
                "slug": "content-wizard",
                "category": "Writing Assistant",
                "rating_average": 4.2,
                "reviews_count": 345,
                "pricing_model": "subscription",
                "status": "approved",
                "is_featured": False,
                "submitted_by": "wizard@content.com",
                "submitted_date": "2025-03-10T11:20:00Z"
            }
        ],
        "total": 253,
        "page": 1,
        "per_page": 5,
        "total_pages": 51
    }), 200

@admin_bp.route('/subscriptions', methods=['GET'])
def admin_subscriptions():
    """Admin subscriptions management endpoint"""
    # Check for authorization header
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        return jsonify({
            "success": False,
            "message": "Unauthorized access"
        }), 401
    
    # Mock subscription data
    return jsonify({
        "success": True,
        "subscriptions": [
            {
                "id": 1,
                "user": {
                    "id": 2,
                    "name": "Jane Smith",
                    "email": "jane.smith@company.com"
                },
                "plan": "business",
                "status": "active",
                "start_date": "2025-05-22T08:45:00Z",
                "renewal_date": "2025-08-22T08:45:00Z",
                "amount": 29.00,
                "payment_method": "credit_card"
            },
            {
                "id": 2,
                "user": {
                    "id": 1,
                    "name": "John Doe",
                    "email": "john.doe@example.com"
                },
                "plan": "premium",
                "status": "active",
                "start_date": "2025-06-15T10:30:00Z",
                "renewal_date": "2025-07-15T10:30:00Z",
                "amount": 9.00,
                "payment_method": "paypal"
            },
            {
                "id": 3,
                "user": {
                    "id": 5,
                    "name": "Michael Wilson",
                    "email": "michael@agency.net"
                },
                "plan": "business",
                "status": "active",
                "start_date": "2025-06-30T11:50:00Z",
                "renewal_date": "2025-07-30T11:50:00Z",
                "amount": 29.00,
                "payment_method": "credit_card"
            },
            {
                "id": 4,
                "user": {
                    "id": 4,
                    "name": "Emily Davis",
                    "email": "emily@design.co"
                },
                "plan": "premium",
                "status": "active",
                "start_date": "2025-04-05T09:15:00Z",
                "renewal_date": "2025-08-05T09:15:00Z",
                "amount": 9.00,
                "payment_method": "credit_card"
            },
            {
                "id": 5,
                "user": {
                    "id": 10,
                    "name": "David Brown",
                    "email": "david@marketing.com"
                },
                "plan": "premium",
                "status": "canceled",
                "start_date": "2025-05-10T14:20:00Z",
                "renewal_date": "2025-06-10T14:20:00Z",
                "amount": 9.00,
                "payment_method": "paypal"
            }
        ],
        "total": 2237,
        "page": 1,
        "per_page": 5,
        "total_pages": 448
    }), 200

@admin_bp.route('/reviews', methods=['GET'])
def admin_reviews():
    """Admin reviews management endpoint"""
    # Check for authorization header
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        return jsonify({
            "success": False,
            "message": "Unauthorized access"
        }), 401
    
    # Mock reviews data
    return jsonify({
        "success": True,
        "reviews": [
            {
                "id": 1,
                "tool": "ChatGPT",
                "user": "writer@content.com",
                "rating": 5,
                "content": "Absolutely amazing tool! Has transformed my content creation workflow completely.",
                "status": "approved",
                "submitted_date": "2025-07-23T05:22:18Z"
            },
            {
                "id": 2,
                "tool": "Midjourney",
                "user": "designer@studio.com",
                "rating": 4,
                "content": "Great for generating creative concepts, though sometimes needs multiple attempts to get exactly what I want.",
                "status": "approved",
                "submitted_date": "2025-07-22T15:40:12Z"
            },
            {
                "id": 3,
                "tool": "GitHub Copilot",
                "user": "developer@techfirm.com",
                "rating": 5,
                "content": "A game-changer for coding productivity. Saves me hours every day with smart suggestions.",
                "status": "approved",
                "submitted_date": "2025-07-21T09:15:45Z"
            },
            {
                "id": 4,
                "tool": "Content Wizard",
                "user": "marketing@company.com",
                "rating": 3,
                "content": "Decent tool but needs improvement in understanding brand voice and style consistency.",
                "status": "pending",
                "submitted_date": "2025-07-23T07:30:22Z"
            },
            {
                "id": 5,
                "tool": "ChatGPT",
                "user": "student@university.edu",
                "rating": 4,
                "content": "Very helpful for research and learning complex topics. Great explanations!",
                "status": "pending",
                "submitted_date": "2025-07-23T06:55:10Z"
            }
        ],
        "total": 8543,
        "page": 1,
        "per_page": 5,
        "total_pages": 1709
    }), 200

