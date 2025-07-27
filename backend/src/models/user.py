"""
User model for the AI Directory Platform.
"""

from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from ..database import db, BaseModel

class User(db.Model, BaseModel):
    """User model for authentication and profile information."""
    
    __tablename__ = 'users'
    __table_args__ = {'extend_existing': True}
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    company = db.Column(db.String(255))
    job_title = db.Column(db.String(255))
    industry_id = db.Column(db.Integer, db.ForeignKey('industries.id'))
    subscription_tier = db.Column(db.String(50), nullable=False, default='Free')
    subscription_start_date = db.Column(db.DateTime)
    subscription_end_date = db.Column(db.DateTime)
    is_admin = db.Column(db.Boolean, nullable=False, default=False)
    
    # Relationships
    industry = db.relationship('Industry', backref='users')
    favorites = db.relationship('UserFavorite', backref='user', cascade='all, delete-orphan')
    reviews = db.relationship('Review', backref='user', cascade='all, delete-orphan')
    activity_logs = db.relationship('UserActivityLog', backref='user', cascade='all, delete-orphan')
    payment_transactions = db.relationship('PaymentTransaction', backref='user', cascade='all, delete-orphan')
    
    @property
    def password(self):
        """Prevent password from being accessed."""
        raise AttributeError('password is not a readable attribute')
    
    @password.setter
    def password(self, password):
        """Set password."""
        self.password_hash = generate_password_hash(password)
    
    def verify_password(self, password):
        """Check password."""
        return check_password_hash(self.password_hash, password)
    
    def to_dict(self):
        """Convert the model instance to a dictionary."""
        data = {
            'id': self.id,
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'company': self.company,
            'job_title': self.job_title,
            'subscription_tier': self.subscription_tier,
            'is_admin': self.is_admin,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
        
        if self.industry:
            data['industry'] = {
                'id': self.industry.id,
                'name': self.industry.name
            }
        
        if self.subscription_start_date:
            data['subscription_start_date'] = self.subscription_start_date.isoformat()
        
        if self.subscription_end_date:
            data['subscription_end_date'] = self.subscription_end_date.isoformat()
        
        return data
    
    def __repr__(self):
        return f'<User {self.email}>'

