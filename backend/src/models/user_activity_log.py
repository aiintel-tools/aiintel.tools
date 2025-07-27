"""
User Activity Log model for the AI Directory Platform.
"""

from ..database import db, BaseModel

class UserActivityLog(db.Model, BaseModel):
    """User Activity Log model for tracking user activity."""
    
    __tablename__ = 'user_activity_logs'
    __table_args__ = {'extend_existing': True}
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    activity_type = db.Column(db.String(100), nullable=False)
    details = db.Column(db.Text)
    
    @classmethod
    def log_activity(cls, user_id, activity_type, details=None):
        """Log a user activity."""
        log = cls(
            user_id=user_id,
            activity_type=activity_type,
            details=details
        )
        db.session.add(log)
        db.session.commit()
        return log
    
    def to_dict(self):
        """Convert the model instance to a dictionary."""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'activity_type': self.activity_type,
            'details': self.details,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
    
    def __repr__(self):
        return f'<UserActivityLog {self.id}>'

