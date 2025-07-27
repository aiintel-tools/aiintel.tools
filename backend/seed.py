"""
Database seeder script for the AI Directory Platform.
"""

import os
import sys
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash
from src.main import create_app
from src.models import (
    User, Category, Industry, AITool, Review, 
    UserFavorite, UserActivityLog, PaymentTransaction, 
    Subscription, ToolIndustry
)
from src.database import db

def seed_database():
    """Seed the database with initial data."""
    print("Seeding database...")
    
    # Create admin user
    admin = User(
        email='admin@aidirectory.com',
        first_name='Admin',
        last_name='User',
        password_hash=generate_password_hash('admin123'),
        subscription_tier='Business',
        is_admin=True
    )
    db.session.add(admin)
    
    # Create test user
    test_user = User(
        email='user@example.com',
        first_name='Test',
        last_name='User',
        password_hash=generate_password_hash('password123'),
        subscription_tier='Free'
    )
    db.session.add(test_user)
    
    # Create premium user
    premium_user = User(
        email='premium@example.com',
        first_name='Premium',
        last_name='User',
        password_hash=generate_password_hash('password123'),
        subscription_tier='Premium',
        subscription_start_date=datetime.utcnow() - timedelta(days=15),
        subscription_end_date=datetime.utcnow() + timedelta(days=15)
    )
    db.session.add(premium_user)
    
    # Create business user
    business_user = User(
        email='business@example.com',
        first_name='Business',
        last_name='User',
        password_hash=generate_password_hash('password123'),
        subscription_tier='Business',
        subscription_start_date=datetime.utcnow() - timedelta(days=5),
        subscription_end_date=datetime.utcnow() + timedelta(days=25)
    )
    db.session.add(business_user)
    
    # Create categories
    categories = [
        Category(name='Conversational AI', description='AI tools for natural language conversations', icon='message-circle'),
        Category(name='Image Generation', description='AI tools for generating images from text prompts', icon='image'),
        Category(name='Code Assistant', description='AI tools for helping with coding tasks', icon='code'),
        Category(name='Text Analysis', description='AI tools for analyzing and understanding text', icon='file-text'),
        Category(name='Data Analysis', description='AI tools for analyzing and visualizing data', icon='bar-chart'),
        Category(name='Audio Generation', description='AI tools for generating audio and music', icon='music'),
        Category(name='Video Generation', description='AI tools for generating and editing videos', icon='video')
    ]
    
    for category in categories:
        db.session.add(category)
    
    # Create industries
    industries = [
        Industry(name='Technology', description='Software, hardware, and IT services'),
        Industry(name='Healthcare', description='Medical services, pharmaceuticals, and healthcare technology'),
        Industry(name='Finance', description='Banking, insurance, and financial services'),
        Industry(name='Education', description='Schools, universities, and educational technology'),
        Industry(name='Marketing', description='Advertising, PR, and marketing services')
    ]
    
    for industry in industries:
        db.session.add(industry)
    
    # Commit to get IDs
    db.session.commit()
    
    # Create AI tools
    tools = [
        {
            'name': 'ChatGPT',
            'description': 'ChatGPT is an AI chatbot developed by OpenAI that can engage in human-like conversations and assist with various tasks.',
            'category_id': categories[0].id,
            'website_url': 'https://chat.openai.com',
            'image_path': 'tool_images/chatgpt.png',
            'access_level': 'Public',
            'industries': [industries[0].id, industries[1].id, industries[2].id, industries[3].id, industries[4].id]
        },
        {
            'name': 'Midjourney',
            'description': 'Midjourney is an AI art generator that creates images from textual descriptions.',
            'category_id': categories[1].id,
            'website_url': 'https://www.midjourney.com',
            'image_path': 'tool_images/midjourney.png',
            'access_level': 'Premium Only',
            'industries': [industries[0].id, industries[3].id, industries[4].id]
        },
        {
            'name': 'GitHub Copilot',
            'description': 'GitHub Copilot is an AI pair programmer that helps you write code faster with less work.',
            'category_id': categories[2].id,
            'website_url': 'https://github.com/features/copilot',
            'image_path': 'tool_images/github_copilot.png',
            'access_level': 'Business Only',
            'industries': [industries[0].id]
        },
        {
            'name': 'DALL-E',
            'description': 'DALL-E is an AI system by OpenAI that can create realistic images and art from a description in natural language.',
            'category_id': categories[1].id,
            'website_url': 'https://openai.com/dall-e-2',
            'image_path': 'tool_images/dalle.png',
            'access_level': 'Premium Only',
            'industries': [industries[0].id, industries[3].id, industries[4].id]
        },
        {
            'name': 'Claude',
            'description': 'Claude is an AI assistant created by Anthropic to be helpful, harmless, and honest.',
            'category_id': categories[0].id,
            'website_url': 'https://www.anthropic.com/claude',
            'image_path': 'tool_images/claude.png',
            'access_level': 'Public',
            'industries': [industries[0].id, industries[1].id, industries[2].id, industries[3].id, industries[4].id]
        },
        {
            'name': 'Jasper',
            'description': 'Jasper is an AI content platform that helps you create marketing copy, social media posts, and more.',
            'category_id': categories[3].id,
            'website_url': 'https://www.jasper.ai',
            'image_path': 'tool_images/jasper.png',
            'access_level': 'Business Only',
            'industries': [industries[4].id]
        },
        {
            'name': 'Stable Diffusion',
            'description': 'Stable Diffusion is an open-source AI art generator that creates images from textual descriptions.',
            'category_id': categories[1].id,
            'website_url': 'https://stability.ai',
            'image_path': 'tool_images/stable_diffusion.png',
            'access_level': 'Premium Only',
            'industries': [industries[0].id, industries[3].id, industries[4].id]
        },
        {
            'name': 'Notion AI',
            'description': 'Notion AI is an AI writing assistant that helps you draft, edit, and summarize content in Notion.',
            'category_id': categories[3].id,
            'website_url': 'https://www.notion.so/product/ai',
            'image_path': 'tool_images/notion_ai.png',
            'access_level': 'Premium Only',
            'industries': [industries[0].id, industries[3].id, industries[4].id]
        }
    ]
    
    for tool_data in tools:
        industries_ids = tool_data.pop('industries')
        tool = AITool(**tool_data)
        db.session.add(tool)
        db.session.flush()  # Get the tool ID
        
        # Add industry associations
        for industry_id in industries_ids:
            tool_industry = ToolIndustry(
                tool_id=tool.id,
                industry_id=industry_id
            )
            db.session.add(tool_industry)
    
    # Commit to get IDs
    db.session.commit()
    
    # Add ratings and reviews
    ai_tools = AITool.query.all()
    users = [test_user, premium_user, business_user]
    
    for tool in ai_tools:
        # Add reviews from different users
        for i, user in enumerate(users):
            rating = 4 + (i % 2)  # Ratings between 4 and 5
            review = Review(
                user_id=user.id,
                tool_id=tool.id,
                rating=rating,
                comment=f"This is a great tool! I've been using it for {i+1} months and it has really improved my workflow.",
                is_verified=(i == 0)  # Verify some reviews
            )
            db.session.add(review)
        
        # Add favorites
        for i, user in enumerate(users):
            if i % 2 == 0:  # Add favorites for some users
                favorite = UserFavorite(
                    user_id=user.id,
                    tool_id=tool.id
                )
                db.session.add(favorite)
    
    # Update tool ratings
    for tool in ai_tools:
        tool.update_rating()
    
    # Add user activity logs
    for user in users:
        activities = [
            ('login', 'User logged in'),
            ('view_profile', None),
            ('search_tools', 'Searched for "AI assistant"'),
            ('view_tool', f'Viewed tool {ai_tools[0].id}')
        ]
        
        for activity_type, details in activities:
            log = UserActivityLog(
                user_id=user.id,
                activity_type=activity_type,
                details=details
            )
            db.session.add(log)
    
    # Add payment transactions for premium and business users
    transactions = [
        {
            'user_id': premium_user.id,
            'amount': 9.99,
            'currency': 'USD',
            'status': 'completed',
            'payment_method': 'card_1234',
            'subscription_tier': 'Premium',
            'transaction_date': datetime.utcnow() - timedelta(days=15)
        },
        {
            'user_id': business_user.id,
            'amount': 29.99,
            'currency': 'USD',
            'status': 'completed',
            'payment_method': 'card_5678',
            'subscription_tier': 'Business',
            'transaction_date': datetime.utcnow() - timedelta(days=5)
        }
    ]
    
    for transaction_data in transactions:
        transaction = PaymentTransaction(**transaction_data)
        db.session.add(transaction)
    
    # Add subscriptions
    subscriptions = [
        {
            'user_id': premium_user.id,
            'plan_id': 'premium',
            'status': 'active',
            'current_period_start': datetime.utcnow() - timedelta(days=15),
            'current_period_end': datetime.utcnow() + timedelta(days=15),
            'cancel_at_period_end': False,
            'payment_method_id': 'card_1234'
        },
        {
            'user_id': business_user.id,
            'plan_id': 'business',
            'status': 'active',
            'current_period_start': datetime.utcnow() - timedelta(days=5),
            'current_period_end': datetime.utcnow() + timedelta(days=25),
            'cancel_at_period_end': False,
            'payment_method_id': 'card_5678'
        }
    ]
    
    for subscription_data in subscriptions:
        subscription = Subscription(**subscription_data)
        db.session.add(subscription)
    
    # Commit all changes
    db.session.commit()
    
    print("Database seeded successfully!")

if __name__ == '__main__':
    app = create_app()
    
    with app.app_context():
        # Check if database should be reset
        if len(sys.argv) > 1 and sys.argv[1] == '--reset':
            print("Resetting database...")
            db.drop_all()
            db.create_all()
        
        # Seed database
        seed_database()

