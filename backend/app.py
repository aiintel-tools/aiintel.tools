from flask import Flask, jsonify, request
from flask_cors import CORS
import os
import json
from datetime import datetime
import uuid

app = Flask(__name__)
CORS(app)

# In-memory data storage (for demo purposes)
users = []
tools = []
reviews = []

# Data file paths
DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
USERS_FILE = os.path.join(DATA_DIR, "users.json")
TOOLS_FILE = os.path.join(DATA_DIR, "tools.json")
REVIEWS_FILE = os.path.join(DATA_DIR, "reviews.json")

# Ensure data directory exists
os.makedirs(DATA_DIR, exist_ok=True)

# Load data from files if they exist
def load_data():
    global users, tools, reviews
    
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, 'r') as f:
            users = json.load(f)
    
    if os.path.exists(TOOLS_FILE):
        with open(TOOLS_FILE, 'r') as f:
            tools = json.load(f)
    
    if os.path.exists(REVIEWS_FILE):
        with open(REVIEWS_FILE, 'r') as f:
            reviews = json.load(f)

# Save data to files
def save_data():
    with open(USERS_FILE, 'w') as f:
        json.dump(users, f)
    
    with open(TOOLS_FILE, 'w') as f:
        json.dump(tools, f)
    
    with open(REVIEWS_FILE, 'w') as f:
        json.dump(reviews, f)

# Load data on startup
load_data()

@app.route('/')
def root():
    return jsonify({
        "message": "Welcome to A.I Intel API",
        "name": "A.I Intel API",
        "status": "running",
        "version": "1.0.0"
    })

@app.route('/api/health')
def health_check():
    return jsonify({
        "message": "A.I Intel API is running",
        "status": "healthy",
        "version": "1.0.0"
    })

# User endpoints
@app.route('/api/users', methods=['GET'])
def get_users():
    return jsonify({
        "success": True,
        "data": {
            "users": users
        }
    })

@app.route('/api/users', methods=['POST'])
def create_user():
    data = request.json
    
    new_user = {
        "id": str(uuid.uuid4()),
        "email": data.get("email"),
        "first_name": data.get("first_name"),
        "last_name": data.get("last_name"),
        "subscription_tier": data.get("subscription_tier", "Free"),
        "is_admin": data.get("is_admin", False),
        "created_at": datetime.now().isoformat()
    }
    
    users.append(new_user)
    save_data()
    
    return jsonify({
        "success": True,
        "message": "User created successfully",
        "data": {
            "user": new_user
        }
    }), 201

# Tool endpoints
@app.route('/api/tools', methods=['GET'])
def get_tools():
    return jsonify({
        "success": True,
        "data": {
            "tools": tools
        }
    })

@app.route('/api/tools', methods=['POST'])
def create_tool():
    data = request.json
    
    new_tool = {
        "id": str(uuid.uuid4()),
        "name": data.get("name"),
        "description": data.get("description"),
        "category": data.get("category"),
        "access_level": data.get("access_level", "Public"),
        "rating": data.get("rating", 0),
        "website_url": data.get("website_url"),
        "business_utility": data.get("business_utility"),
        "price_point": data.get("price_point"),
        "created_at": datetime.now().isoformat()
    }
    
    tools.append(new_tool)
    save_data()
    
    return jsonify({
        "success": True,
        "message": "Tool created successfully",
        "data": {
            "tool": new_tool
        }
    }), 201

# Admin dashboard data
@app.route('/api/admin/dashboard', methods=['GET'])
def get_dashboard_data():
    return jsonify({
        "success": True,
        "data": {
            "counts": {
                "users": len(users),
                "tools": len(tools),
                "reviews": len(reviews),
                "revenue": 12850.00
            },
            "recent_users": users[-5:] if users else [],
            "recent_tools": tools[-5:] if tools else []
        }
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

