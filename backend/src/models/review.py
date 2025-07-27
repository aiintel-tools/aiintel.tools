"""
Review model for the AI Directory Platform.
"""

from ..database import db, BaseModel

class Review(db.Model, BaseModel):
    """Review model for user reviews of AI tools."""
    
    __tablename__ = 'reviews'
    __table_args__ = {'extend_existing': True}
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    tool_id = db.Column(db.Integer, db.ForeignKey('ai_tools.id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.Text)
    is_verified = db.Column(db.Boolean, nullable=False, default=False)
    
    def to_dict(self):
        """Convert the model instance to a dictionary."""
        data = {
            'id': self.id,
            'rating': self.rating,
            'comment': self.comment,
            'is_verified': self.is_verified,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
        
        if self.user:
            data['user'] = {
                'id': self.user.id,
                'first_name': self.user.first_name,
                'last_name': self.user.last_name
            }
        
        return data
    
    def __repr__(self):
        return f'<Review {self.id}>'

