from flask import Flask, jsonify, request, render_template_string
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

# Initialize with frontend data if empty
if not users:
    users.extend([
        {
            "id": "1",
            "email": "john.doe@example.com",
            "first_name": "John",
            "last_name": "Doe",
            "subscription_tier": "Premium",
            "is_admin": False,
            "created_at": "2025-01-15T10:30:00"
        },
        {
            "id": "2", 
            "email": "sarah.smith@company.com",
            "first_name": "Sarah",
            "last_name": "Smith",
            "subscription_tier": "Business",
            "is_admin": False,
            "created_at": "2025-01-20T14:22:00"
        },
        {
            "id": "3",
            "email": "mike.johnson@startup.io",
            "first_name": "Mike", 
            "last_name": "Johnson",
            "subscription_tier": "Free",
            "is_admin": False,
            "created_at": "2025-01-25T09:15:00"
        }
    ])

if not tools:
    tools.extend([
        {
            "id": "1",
            "name": "ChatGPT",
            "description": "Advanced language model that can generate human-like text, answer questions, and assist with various tasks.",
            "category": "Conversational AI",
            "access_level": "Public",
            "rating": 4.8,
            "website_url": "https://chat.openai.com",
            "business_utility": "Automate customer support, content creation, and research tasks. Helps businesses save time on writing, brainstorming, and problem-solving.",
            "price_point": "Free tier available, Plus at $20/month",
            "created_at": "2025-01-01T00:00:00"
        },
        {
            "id": "2", 
            "name": "Midjourney",
            "description": "AI art generator that creates stunning images from text descriptions using advanced machine learning.",
            "category": "Image Generation",
            "access_level": "Premium",
            "rating": 4.7,
            "website_url": "https://midjourney.com",
            "business_utility": "Create marketing visuals, product mockups, and brand assets without hiring designers. Perfect for social media content and advertising.",
            "price_point": "Basic plan $10/month, Standard $30/month",
            "created_at": "2025-01-01T00:00:00"
        },
        {
            "id": "3",
            "name": "GitHub Copilot", 
            "description": "AI pair programmer that helps you write code faster with suggestions based on comments and context.",
            "category": "Code Assistant",
            "access_level": "Business",
            "rating": 4.6,
            "website_url": "https://github.com/features/copilot",
            "business_utility": "Accelerate software development, reduce coding errors, and help developers learn new programming languages faster.",
            "price_point": "$10/month per user, Free for students",
            "created_at": "2025-01-01T00:00:00"
        }
    ])

if not reviews:
    reviews.extend([
        {
            "id": "1",
            "user_name": "John Doe",
            "tool_name": "ChatGPT", 
            "rating": 5,
            "status": "Approved",
            "comment": "Incredible tool for content creation and customer support automation.",
            "created_at": "2025-01-20T10:00:00"
        },
        {
            "id": "2",
            "user_name": "Sarah Smith",
            "tool_name": "Midjourney",
            "rating": 5,
            "status": "Approved", 
            "comment": "Amazing for creating marketing visuals. Saves us thousands on design costs.",
            "created_at": "2025-01-22T15:30:00"
        },
        {
            "id": "3",
            "user_name": "Mike Johnson",
            "tool_name": "GitHub Copilot",
            "rating": 4,
            "status": "Pending",
            "comment": "Great coding assistant, though sometimes suggestions need refinement.",
            "created_at": "2025-01-25T11:45:00"
        }
    ])
    
# Save the initialized data
save_data()

# Admin portal HTML template
ADMIN_PORTAL_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>A.I Intel Admin Portal</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: #f5f5f5; }
        .container { max-width: 1200px; margin: 0 auto; padding: 20px; }
        .header { background: white; padding: 20px; border-radius: 8px; margin-bottom: 20px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
        .header h1 { color: #2c3e50; }
        .stats { display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px; margin-bottom: 30px; }
        .stat-card { background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
        .stat-number { font-size: 2em; font-weight: bold; color: #3498db; }
        .stat-label { color: #7f8c8d; margin-top: 5px; }
        .section { background: white; padding: 20px; border-radius: 8px; margin-bottom: 20px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
        .section h2 { color: #2c3e50; margin-bottom: 15px; }
        table { width: 100%; border-collapse: collapse; }
        th, td { padding: 12px; text-align: left; border-bottom: 1px solid #ecf0f1; }
        th { background: #f8f9fa; font-weight: 600; }
        .btn { background: #3498db; color: white; padding: 8px 16px; border: none; border-radius: 4px; cursor: pointer; text-decoration: none; display: inline-block; }
        .btn:hover { background: #2980b9; }
        .form-group { margin-bottom: 15px; }
        .form-group label { display: block; margin-bottom: 5px; font-weight: 600; }
        .form-group input, .form-group textarea, .form-group select { width: 100%; padding: 8px; border: 1px solid #ddd; border-radius: 4px; }
        .modal { display: none; position: fixed; z-index: 1000; left: 0; top: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.5); }
        .modal-content { background: white; margin: 5% auto; padding: 20px; width: 80%; max-width: 600px; border-radius: 8px; }
        .close { color: #aaa; float: right; font-size: 28px; font-weight: bold; cursor: pointer; }
        .close:hover { color: black; }
        .tabs { display: flex; margin-bottom: 20px; }
        .tab { padding: 10px 20px; background: #ecf0f1; border: none; cursor: pointer; margin-right: 5px; }
        .tab.active { background: #3498db; color: white; }
        .tab-content { display: none; }
        .tab-content.active { display: block; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>A.I Intel Admin Portal</h1>
            <p>Manage your AI directory platform</p>
        </div>

        <div class="stats">
            <div class="stat-card">
                <div class="stat-number" id="userCount">{{ user_count }}</div>
                <div class="stat-label">Total Users</div>
            </div>
            <div class="stat-card">
                <div class="stat-number" id="toolCount">{{ tool_count }}</div>
                <div class="stat-label">AI Tools</div>
            </div>
            <div class="stat-card">
                <div class="stat-number" id="reviewCount">{{ review_count }}</div>
                <div class="stat-label">Reviews</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">$12,850</div>
                <div class="stat-label">Monthly Revenue</div>
            </div>
        </div>

        <div class="tabs">
            <button class="tab active" onclick="showTab('users')">Users</button>
            <button class="tab" onclick="showTab('tools')">AI Tools</button>
            <button class="tab" onclick="showTab('reviews')">Reviews</button>
        </div>

        <div id="users" class="tab-content active">
            <div class="section">
                <h2>User Management</h2>
                <button class="btn" onclick="showAddUserModal()">Add New User</button>
                <table>
                    <thead>
                        <tr>
                            <th>Name</th>
                            <th>Email</th>
                            <th>Subscription</th>
                            <th>Created</th>
                            <th>Actions</th>
                        </tr>
                    </thead>
                    <tbody id="usersTable">
                        {% for user in users %}
                        <tr>
                            <td>{{ user.first_name }} {{ user.last_name }}</td>
                            <td>{{ user.email }}</td>
                            <td>{{ user.subscription_tier }}</td>
                            <td>{{ user.created_at[:10] }}</td>
                            <td><button class="btn">Edit</button></td>
                        </tr>
                        {% endfor %}
                    </tbody>
                </table>
            </div>
        </div>

        <div id="tools" class="tab-content">
            <div class="section">
                <h2>AI Tools Management</h2>
                <button class="btn" onclick="showAddToolModal()">Add New Tool</button>
                <table>
                    <thead>
                        <tr>
                            <th>Name</th>
                            <th>Category</th>
                            <th>Access Level</th>
                            <th>Rating</th>
                            <th>Actions</th>
                        </tr>
                    </thead>
                    <tbody id="toolsTable">
                        {% for tool in tools %}
                        <tr>
                            <td>{{ tool.name }}</td>
                            <td>{{ tool.category }}</td>
                            <td>{{ tool.access_level }}</td>
                            <td>{{ tool.rating }}/5</td>
                            <td><button class="btn">Edit</button></td>
                        </tr>
                        {% endfor %}
                    </tbody>
                </table>
            </div>
        </div>

        <div id="reviews" class="tab-content">
            <div class="section">
                <h2>Reviews Management</h2>
                <table>
                    <thead>
                        <tr>
                            <th>User</th>
                            <th>Tool</th>
                            <th>Rating</th>
                            <th>Status</th>
                            <th>Actions</th>
                        </tr>
                    </thead>
                    <tbody id="reviewsTable">
                        {% for review in reviews %}
                        <tr>
                            <td>{{ review.user_name }}</td>
                            <td>{{ review.tool_name }}</td>
                            <td>{{ review.rating }}/5</td>
                            <td>{{ review.status }}</td>
                            <td><button class="btn">Approve</button></td>
                        </tr>
                        {% endfor %}
                    </tbody>
                </table>
            </div>
        </div>
    </div>

    <!-- Add User Modal -->
    <div id="addUserModal" class="modal">
        <div class="modal-content">
            <span class="close" onclick="closeModal('addUserModal')">&times;</span>
            <h2>Add New User</h2>
            <form id="addUserForm">
                <div class="form-group">
                    <label>First Name:</label>
                    <input type="text" id="firstName" required>
                </div>
                <div class="form-group">
                    <label>Last Name:</label>
                    <input type="text" id="lastName" required>
                </div>
                <div class="form-group">
                    <label>Email:</label>
                    <input type="email" id="email" required>
                </div>
                <div class="form-group">
                    <label>Subscription Tier:</label>
                    <select id="subscriptionTier">
                        <option value="Free">Free</option>
                        <option value="Premium">Premium</option>
                        <option value="Business">Business</option>
                    </select>
                </div>
                <button type="submit" class="btn">Add User</button>
            </form>
        </div>
    </div>

    <!-- Add Tool Modal -->
    <div id="addToolModal" class="modal">
        <div class="modal-content">
            <span class="close" onclick="closeModal('addToolModal')">&times;</span>
            <h2>Add New AI Tool</h2>
            <form id="addToolForm">
                <div class="form-group">
                    <label>Tool Name:</label>
                    <input type="text" id="toolName" required>
                </div>
                <div class="form-group">
                    <label>Description:</label>
                    <textarea id="toolDescription" rows="3" required></textarea>
                </div>
                <div class="form-group">
                    <label>Category:</label>
                    <select id="toolCategory">
                        <option value="Conversational AI">Conversational AI</option>
                        <option value="Image Generation">Image Generation</option>
                        <option value="Code Assistant">Code Assistant</option>
                        <option value="Data Analysis">Data Analysis</option>
                        <option value="Content Creation">Content Creation</option>
                    </select>
                </div>
                <div class="form-group">
                    <label>Website URL:</label>
                    <input type="url" id="toolWebsite">
                </div>
                <div class="form-group">
                    <label>Business Utility:</label>
                    <textarea id="businessUtility" rows="3"></textarea>
                </div>
                <div class="form-group">
                    <label>Price Point:</label>
                    <input type="text" id="pricePoint" placeholder="e.g., Free, $20/month">
                </div>
                <div class="form-group">
                    <label>Access Level:</label>
                    <select id="accessLevel">
                        <option value="Public">Public</option>
                        <option value="Premium">Premium</option>
                        <option value="Business">Business</option>
                    </select>
                </div>
                <button type="submit" class="btn">Add Tool</button>
            </form>
        </div>
    </div>

    <script>
        function showTab(tabName) {
            // Hide all tab contents
            const contents = document.querySelectorAll('.tab-content');
            contents.forEach(content => content.classList.remove('active'));
            
            // Remove active class from all tabs
            const tabs = document.querySelectorAll('.tab');
            tabs.forEach(tab => tab.classList.remove('active'));
            
            // Show selected tab content
            document.getElementById(tabName).classList.add('active');
            
            // Add active class to clicked tab
            event.target.classList.add('active');
        }

        function showAddUserModal() {
            document.getElementById('addUserModal').style.display = 'block';
        }

        function showAddToolModal() {
            document.getElementById('addToolModal').style.display = 'block';
        }

        function closeModal(modalId) {
            document.getElementById(modalId).style.display = 'none';
        }

        // Add User Form Submit
        document.getElementById('addUserForm').addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const userData = {
                first_name: document.getElementById('firstName').value,
                last_name: document.getElementById('lastName').value,
                email: document.getElementById('email').value,
                subscription_tier: document.getElementById('subscriptionTier').value
            };

            try {
                const response = await fetch('/api/users', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(userData)
                });

                if (response.ok) {
                    alert('User added successfully!');
                    closeModal('addUserModal');
                    location.reload();
                } else {
                    alert('Error adding user');
                }
            } catch (error) {
                alert('Error: ' + error.message);
            }
        });

        // Add Tool Form Submit
        document.getElementById('addToolForm').addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const toolData = {
                name: document.getElementById('toolName').value,
                description: document.getElementById('toolDescription').value,
                category: document.getElementById('toolCategory').value,
                website_url: document.getElementById('toolWebsite').value,
                business_utility: document.getElementById('businessUtility').value,
                price_point: document.getElementById('pricePoint').value,
                access_level: document.getElementById('accessLevel').value,
                rating: 0
            };

            try {
                const response = await fetch('/api/tools', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(toolData)
                });

                if (response.ok) {
                    alert('Tool added successfully!');
                    closeModal('addToolModal');
                    location.reload();
                } else {
                    alert('Error adding tool');
                }
            } catch (error) {
                alert('Error: ' + error.message);
            }
        });

        // Close modal when clicking outside
        window.onclick = function(event) {
            const modals = document.querySelectorAll('.modal');
            modals.forEach(modal => {
                if (event.target === modal) {
                    modal.style.display = 'none';
                }
            });
        }
    </script>
</body>
</html>
"""

@app.route('/')
def root():
    return jsonify({
        "message": "Welcome to A.I Intel API",
        "name": "A.I Intel API",
        "status": "running",
        "version": "1.0.0"
    })

@app.route('/admin')
def admin_portal():
    return render_template_string(ADMIN_PORTAL_HTML, 
                                users=users, 
                                tools=tools, 
                                reviews=reviews,
                                user_count=len(users),
                                tool_count=len(tools),
                                review_count=len(reviews))

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

