from datetime import datetime
from src.database import db

class ToolGuide(db.Model):
    __tablename__ = 'tool_guides'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    tool_id = db.Column(db.Integer, db.ForeignKey('ai_tools.id', ondelete='CASCADE'), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    guide_type = db.Column(db.String(50), nullable=False)  # Tutorial, Case Study, Quick Start, etc.
    order_index = db.Column(db.Integer, default=0)  # For ordering multiple guides
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    author = db.relationship('User', backref='guides')

    def __repr__(self):
        return f'<ToolGuide {self.title}>'

    def to_dict(self):
        return {
            'id': self.id,
            'tool_id': self.tool_id,
            'title': self.title,
            'content': self.content,
            'author': self.author.to_dict() if self.author else None,
            'guide_type': self.guide_type,
            'order_index': self.order_index,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

