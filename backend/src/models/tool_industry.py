"""
Tool Industry junction model for the AI Directory Platform.
"""

from ..database import db, BaseModel

class ToolIndustry(db.Model, BaseModel):
    """Junction table for the many-to-many relationship between AI tools and industries."""
    
    __tablename__ = 'tool_industries'
    __table_args__ = {'extend_existing': True}
    
    id = db.Column(db.Integer, primary_key=True)
    tool_id = db.Column(db.Integer, db.ForeignKey('ai_tools.id'), nullable=False)
    industry_id = db.Column(db.Integer, db.ForeignKey('industries.id'), nullable=False)
    
    def __repr__(self):
        return f'<ToolIndustry {self.tool_id}:{self.industry_id}>'

