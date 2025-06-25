from pydantic import BaseModel, EmailStr
from typing import List, Optional
from uuid import UUID
from datetime import datetime

# ------------------ User Schemas ------------------

class UserBase(BaseModel):
    email: EmailStr
    user_name: str

    class Config:
        from_attributes = True

class UserCreate(UserBase):
    email:EmailStr
    password:str

class UserRead(UserBase):
    user_id: UUID
    created_at: datetime
    updated_at: datetime

class UserOut(BaseModel):
    id: int
    email: EmailStr
    class Config:
        orm_mode = True
# ------------------ Auth Token ------------------

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

# ------------------ Recipe Schemas ------------------

class RecipeBase(BaseModel):
    title: str
    description: Optional[str] = None
    status: Optional[bool] = False

class RecipeCreate(RecipeBase):
    pass

class RecipeRead(RecipeBase):
    recipe_id: UUID
    created_at: datetime
    updated_at: datetime
    owner_id: UUID

# ------------------ Ingredient Schemas ------------------

class RecipeIngredientBase(BaseModel):
    name: str
    quantity: str
    description: Optional[str] = None

class RecipeIngredientCreate(RecipeIngredientBase):
    pass

class RecipeIngredientRead(RecipeIngredientBase):
    ingredient_id: UUID
    recipe_id: UUID
    created_at: datetime
    updated_at: datetime

# ------------------ Step Schemas ------------------

class RecipeStepBase(BaseModel):
    description: str
    order: int

class RecipeStepCreate(RecipeStepBase):
    pass

class RecipeStepRead(RecipeStepBase):
    step_id: UUID
    recipe_id: UUID
    created_at: datetime
    updated_at: datetime
