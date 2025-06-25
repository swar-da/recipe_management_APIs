import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Text, Boolean, DateTime, ForeignKey, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.database import base
from sqlalchemy.ext.declarative import declarative_base
from alembic import op
import sqlalchemy as sa


Base = declarative_base()


class User(base):
    __tablename__ = "users"

    user_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    user_name = Column(String, nullable=False)
    hashed_password = Column(String, nullable=True)
    email = Column(String, unique=True, nullable=False)

    recipes = relationship("Recipe", back_populates="owner")

    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))


class Recipe(base):
    __tablename__ = "recipes"

    recipe_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    status = Column(Boolean, default=False)

    owner_id = Column(UUID(as_uuid=True), ForeignKey("users.user_id"), nullable=False)
    owner = relationship("User", back_populates="recipes")

    ingredients = relationship("RecipeIngredient", back_populates="recipe", cascade="all, delete-orphan")
    steps = relationship("RecipeStep", back_populates="recipe", cascade="all, delete-orphan")

    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))


class RecipeIngredient(base):
    __tablename__ = "recipe_ingredients"

    ingredient_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    name = Column(String, nullable=False)
    quantity = Column(String, nullable=False)
    description = Column(Text, nullable=True)

    recipe_id = Column(UUID(as_uuid=True), ForeignKey("recipes.recipe_id"))
    recipe = relationship("Recipe", back_populates="ingredients")

    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))


class RecipeStep(base):
    __tablename__ = "recipe_steps"

    step_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    description = Column(Text, nullable=False)
    order = Column(Integer, nullable=False)

    recipe_id = Column(UUID(as_uuid=True), ForeignKey("recipes.recipe_id"))
    recipe = relationship("Recipe", back_populates="steps")

    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))
