from flask import Flask, jsonify, request
from flask_cors import CORS
import os
from src.config import Config
from src.database import db
from src.routes.auth import auth_bp
from src.routes.tools import tools_bp
from src.routes.users import users_bp
from src.routes.categories import categories_bp
from src.routes.industries import industries_bp
from src.routes.reviews import reviews_bp
from src.routes.subscriptions import subscriptions_bp
from src.routes.admin import admin_bp
from src.routes.guides import guides_bp

app = Flask(__name__)

# Configure the Flask application
database_url = os.environ.get("DATABASE_URL", "sqlite:///instance/ai_directory.db")
# PostgreSQL URLs from Railway start with postgres://, but SQLAlchemy expects postgresql://
if database_url.startswith("postgres://"):
    database_url = database_url.replace("postgres://", "postgresql://", 1)

app.config["SQLALCHEMY_DATABASE_URI"] = database_url
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["JWT_SECRET_KEY"] = os.environ.get("JWT_SECRET_KEY", "dev-secret-key")
app.config["UPLOAD_FOLDER"] = os.path.join(os.path.dirname(os.path.abspath(__file__)), "uploads")

# Ensure upload directory exists
os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

# Initialize extensions
db.init_app(app)

# Configure CORS
CORS(app, resources={r"/api/*": {"origins": "*"}})

# Register blueprints
app.register_blueprint(auth_bp, url_prefix="/api/auth")
app.register_blueprint(tools_bp, url_prefix="/api/tools")
app.register_blueprint(users_bp, url_prefix="/api/users")
app.register_blueprint(categories_bp, url_prefix="/api/categories")
app.register_blueprint(industries_bp, url_prefix="/api/industries")
app.register_blueprint(reviews_bp, url_prefix="/api/reviews")
app.register_blueprint(subscriptions_bp, url_prefix="/api/subscriptions")
app.register_blueprint(admin_bp, url_prefix="/api/admin")
app.register_blueprint(guides_bp, url_prefix="/api/guides")

@app.route("/")
def root():
    return jsonify({
        "message": "Welcome to AI Directory API",
        "name": "AI Directory API",
        "status": "running",
        "version": "1.0.0"
    })

@app.route("/api/health")
def health_check():
    return jsonify({
        "message": "AI Directory API is running",
        "status": "healthy",
        "version": "1.0.0"
    })

# Create database tables
with app.app_context():
    db.create_all()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

