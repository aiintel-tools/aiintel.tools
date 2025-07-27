from datetime import datetime
from src.database import db

class AITool(db.Model):
    __tablename__ = 'ai_tools'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    description = db.Column(db.Text, nullable=False)
    website_url = db.Column(db.String(255), nullable=False)
    image_path = db.Column(db.String(255))
    access_level = db.Column(db.String(50), nullable=False, default='public')
    rating = db.Column(db.Float, default=0)
    
    # New fields
    business_utility = db.Column(db.Text)
    price_point_type = db.Column(db.String(50))  # Free, Freemium, Paid, Enterprise, etc.
    price_point_details = db.Column(db.JSON)  # Structured pricing information
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    category = db.relationship('Category', backref='tools')
    reviews = db.relationship('Review', backref='tool', cascade='all, delete-orphan')
    favorites = db.relationship('UserFavorite', backref='tool', cascade='all, delete-orphan')
    industries = db.relationship('Industry', secondary='tool_industries', backref='tools')
    guides = db.relationship('ToolGuide', backref='tool', cascade='all, delete-orphan')

    def __repr__(self):
        return f'<AITool {self.name}>'

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'category': self.category.to_dict() if self.category else None,
            'description': self.description,
            'website_url': self.website_url,
            'image_path': self.image_path,
            'access_level': self.access_level,
            'rating': self.rating,
            'business_utility': self.business_utility,
            'price_point_type': self.price_point_type,
            'price_point_details': self.price_point_details,
            'industries': [industry.to_dict() for industry in self.industries],
            'guides': [guide.to_dict() for guide in self.guides],
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

