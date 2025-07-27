"""
User Favorite model for the AI Directory Platform.
"""

from ..database import db, BaseModel

class UserFavorite(db.Model, BaseModel):
    """User Favorite model for tracking user's favorite AI tools."""
    
    __tablename__ = 'user_favorites'
    __table_args__ = {'extend_existing': True}
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    tool_id = db.Column(db.Integer, db.ForeignKey('ai_tools.id'), nullable=False)
    
    def to_dict(self):
        """Convert the model instance to a dictionary."""
        data = {
            'id': self.id,
            'user_id': self.user_id,
            'tool_id': self.tool_id,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
        
        if hasattr(self, 'tool') and self.tool:
            data['tool'] = self.tool.to_dict()
        
        return data
    
    def __repr__(self):
        return f'<UserFavorite {self.user_id}:{self.tool_id}>'

