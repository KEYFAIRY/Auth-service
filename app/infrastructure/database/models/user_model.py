from sqlalchemy import Column, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class UserModel(Base):
    """ORM model for the users table"""
    
    __tablename__ = "Student"

    uid = Column(String(128), primary_key=True)  # Firebase UID
    email = Column(String(255), nullable=False, unique=True)
    name = Column(String(255), nullable=False)
    piano_level = Column(String(50), nullable=False)