"""
Database configuration for the AI Directory Platform.
This module provides a central SQLite database connection for all models.
"""

import os
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData

# Create a metadata object with naming conventions for constraints
convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

metadata = MetaData(naming_convention=convention)

# Create a SQLAlchemy instance
db = SQLAlchemy(metadata=metadata)

# Base model class with common fields and methods
class BaseModel:
    """Base model class with common fields and methods."""
    
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def save(self):
        """Save the model instance to the database."""
        db.session.add(self)
        db.session.commit()
        return self
    
    def delete(self):
        """Delete the model instance from the database."""
        db.session.delete(self)
        db.session.commit()
        return self
    
    @classmethod
    def get_by_id(cls, id):
        """Get a model instance by ID."""
        return cls.query.get(id)
    
    @classmethod
    def get_all(cls):
        """Get all model instances."""
        return cls.query.all()
    
    def to_dict(self):
        """Convert the model instance to a dictionary."""
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

def init_app(app):
    """Initialize the database with the Flask app."""
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
        'DATABASE_URL', 'sqlite:///ai_directory.db'
    )
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Initialize the SQLAlchemy app
    db.init_app(app)
    
    # Create tables
    with app.app_context():
        db.create_all()

