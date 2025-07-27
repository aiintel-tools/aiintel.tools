import os
from flask import Flask, jsonify
from flask_cors import CORS
from admin_endpoints import admin_bp

def create_app():
    app = Flask(__name__)
    
    # Configuration
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'ai-directory-secret-key')
    CORS(app, origins="*", supports_credentials=True)
    
    # Register blueprints
    app.register_blueprint(admin_bp)
    
    # Root endpoint
    @app.route('/')
    def root():
        return jsonify({
            'name': 'AI Directory API',
            'version': '1.0.0',
            'status': 'running',
            'message': 'Welcome to AI Directory API'
        }), 200
    
    # Health check endpoint
    @app.route('/api/health')
    def health_check():
        return jsonify({
            'status': 'healthy',
            'message': 'AI Directory API is running',
            'version': '1.0.0'
        }), 200
    
    # API info endpoint
    @app.route('/api/info')
    def api_info():
        return jsonify({
            'name': 'AI Directory API',
            'version': '1.0.0',
            'description': 'AI Tools Directory Platform API',
            'endpoints': {
                'health': '/api/health',
                'info': '/api/info',
                'tools': '/api/tools',
                'categories': '/api/categories',
                'admin': '/api/admin/*'
            }
        }), 200
    
    # Mock endpoints for frontend compatibility
    @app.route('/api/tools')
    def get_tools():
        return jsonify({
            'success': True,
            'tools': [
                {
                    'id': 1,
                    'name': 'ChatGPT',
                    'slug': 'chatgpt',
                    'short_description': 'Advanced AI chatbot for conversations and content creation',
                    'rating_average': 4.8,
                    'category': {'name': 'Conversational AI'},
                    'pricing_model': 'freemium',
                    'is_featured': True
                },
                {
                    'id': 2,
                    'name': 'Midjourney',
                    'slug': 'midjourney',
                    'short_description': 'AI-powered image generation from text prompts',
                    'rating_average': 4.7,
                    'category': {'name': 'Image Generation'},
                    'pricing_model': 'subscription',
                    'is_featured': True
                },
                {
                    'id': 3,
                    'name': 'GitHub Copilot',
                    'slug': 'github-copilot',
                    'short_description': 'AI pair programmer that helps you write code faster',
                    'rating_average': 4.6,
                    'category': {'name': 'Code Assistant'},
                    'pricing_model': 'subscription',
                    'is_featured': True
                }
            ],
            'total': 3,
            'page': 1,
            'per_page': 10
        }), 200
    
    @app.route('/api/categories')
    def get_categories():
        return jsonify({
            'success': True,
            'categories': [
                {'id': 1, 'name': 'Conversational AI', 'tool_count': 45},
                {'id': 2, 'name': 'Image Generation', 'tool_count': 32},
                {'id': 3, 'name': 'Code Assistant', 'tool_count': 28},
                {'id': 4, 'name': 'Writing Assistant', 'tool_count': 38},
                {'id': 5, 'name': 'Data Analysis', 'tool_count': 22},
                {'id': 6, 'name': 'Video Generation', 'tool_count': 15}
            ]
        }), 200
    
    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'error': 'Endpoint not found'}), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({'error': 'Internal server error'}), 500
    
    return app

app = create_app()

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)

