"""
Payment Transaction model for the AI Directory Platform.
"""

from ..database import db, BaseModel

class PaymentTransaction(db.Model, BaseModel):
    """Payment Transaction model for tracking subscription payments."""
    
    __tablename__ = 'payment_transactions'
    __table_args__ = {'extend_existing': True}
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    currency = db.Column(db.String(10), nullable=False, default='USD')
    status = db.Column(db.String(50), nullable=False)
    payment_method = db.Column(db.String(100))
    subscription_tier = db.Column(db.String(50), nullable=False)
    transaction_date = db.Column(db.DateTime, nullable=False)
    transaction_metadata = db.Column(db.Text)
    
    def to_dict(self):
        """Convert the model instance to a dictionary."""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'amount': self.amount,
            'currency': self.currency,
            'status': self.status,
            'payment_method': self.payment_method,
            'subscription_tier': self.subscription_tier,
            'transaction_date': self.transaction_date.isoformat() if self.transaction_date else None,
            'transaction_metadata': self.transaction_metadata,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
    
    def __repr__(self):
        return f'<PaymentTransaction {self.id}>'

