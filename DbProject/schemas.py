"""This module contains all the schemas used in the application."""
from pydantic import BaseModel


class PostBase(BaseModel):
    """
    Base schema for Post model.
    Contains the basic fields that are shared across Post creation and retrieval.
    """
    title: str
    content: str
    user_id: int


class PostCreate(PostBase):
    """
    Schema for creating a new Post.
    Inherits from PostBase, and does not add additional fields.
    """
    pass


class Post(PostBase):
    """
    Full schema for Post model, including additional fields such as 'id' and 'user_id'.
    Used for returning a Post object after it's been created or retrieved.
    """
    id: int
    user_id: int

    class Config:
        """Pydantic configuration to enable working with SQLAlchemy ORM models."""
        orm_mode = True


class UserBase(BaseModel):
    """
    Base schema for User model.
    Contains fields shared across User creation and retrieval.
    """
    username: str
    email: str
    password: str


class UserCreate(UserBase):
    """
    Schema for creating a new User.
    Inherits from UserBase, and does not add additional fields.
    """
    pass


class User(UserBase):
    """
    Full schema for User model, including the additional 'id' field.
    Used for returning a User object after it's been created or retrieved.
    """
    id: int

    class Config:
        """Pydantic configuration to enable working with SQLAlchemy ORM models."""
        orm_mode = True
