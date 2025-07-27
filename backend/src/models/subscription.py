"""
Subscription model for the AI Directory Platform.
"""

from ..database import db, BaseModel

class Subscription(db.Model, BaseModel):
    """Subscription model for managing subscription plans."""
    
    __tablename__ = 'subscriptions'
    __table_args__ = {'extend_existing': True}
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    plan_id = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(50), nullable=False)
    current_period_start = db.Column(db.DateTime, nullable=False)
    current_period_end = db.Column(db.DateTime, nullable=False)
    cancel_at_period_end = db.Column(db.Boolean, nullable=False, default=False)
    payment_method_id = db.Column(db.String(100))
    subscription_metadata = db.Column(db.Text)
    
    def to_dict(self):
        """Convert the model instance to a dictionary."""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'plan_id': self.plan_id,
            'status': self.status,
            'current_period_start': self.current_period_start.isoformat() if self.current_period_start else None,
            'current_period_end': self.current_period_end.isoformat() if self.current_period_end else None,
            'cancel_at_period_end': self.cancel_at_period_end,
            'payment_method_id': self.payment_method_id,
            'subscription_metadata': self.subscription_metadata,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def __repr__(self):
        return f'<Subscription {self.id}>'

