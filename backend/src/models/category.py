"""
Category model for the AI Directory Platform.
"""

from ..database import db, BaseModel

class Category(db.Model, BaseModel):
    """Category model for organizing AI tools."""
    
    __tablename__ = 'categories'
    __table_args__ = {'extend_existing': True}
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.Text)
    icon = db.Column(db.String(100))
    
    def tool_count(self):
        """Get the number of tools in this category."""
        return len(self.tools)
    
    def to_dict(self):
        """Convert the model instance to a dictionary."""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'icon': self.icon,
            'tool_count': self.tool_count(),
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def __repr__(self):
        return f'<Category {self.name}>'

