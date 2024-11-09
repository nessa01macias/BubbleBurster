# Defines database models and schemas

from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base  # Assuming `Base` is initialized in database.py

class Issue(Base):
    __tablename__ = 'issues'
    id = Column(Integer, primary_key=True)
    content = Column(Text, nullable=False)
    department = Column(String(50))
    category_id = Column(Integer, ForeignKey('categories.id'))  # Link to Category table
    is_positive = Column(Boolean, default=False)
    ranking = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    category = relationship("Category", back_populates="issues")
    feedback = relationship("Feedback", back_populates="issue")
    progress = relationship("Progress", back_populates="issue")

class Category(Base):
    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True, nullable=False)
    is_positive = Column(Boolean, default=False)
    description = Column(Text)

    # Relationships
    issues = relationship("Issue", back_populates="category")

class Feedback(Base):
    __tablename__ = 'feedback'
    id = Column(Integer, primary_key=True)
    issue_id = Column(Integer, ForeignKey('issues.id'))
    content = Column(Text, nullable=False)
    anonymous = Column(Boolean, default=False)
    timestamp = Column(DateTime, default=datetime.utcnow)

    # Relationships
    issue = relationship("Issue", back_populates="feedback")

class Progress(Base):
    __tablename__ = 'progress'
    id = Column(Integer, primary_key=True)
    issue_id = Column(Integer, ForeignKey('issues.id'))
    status = Column(String(50), nullable=False)  # e.g., “In Progress,” “Resolved”
    action_taken = Column(Text)
    last_updated = Column(DateTime, default=datetime.utcnow)

    # Relationships
    issue = relationship("Issue", back_populates="progress")

class Settings(Base):
    __tablename__ = 'settings'
    id = Column(Integer, primary_key=True)
    visibility = Column(String(50), nullable=False)  # e.g., “Company-wide,” “HR-only”
    access_level = Column(String(200), nullable=True)
