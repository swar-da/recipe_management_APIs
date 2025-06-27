from pydantic import BaseModel, EmailStr
from typing import List, Optional
from uuid import UUID
from datetime import datetime

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
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


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
    
class RecipeUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None



class RecipeIngredientBase(BaseModel):
    ingredient_id: UUID
    name: str
    quantity: str
    recipe_id: UUID
    created_at: datetime
    updated_at: datetime
class Config:
    from_attributes = True


class RecipeIngredientCreate(BaseModel):
    name: str
    quantity: str
    
class RecipeIngredientRead(RecipeIngredientBase):
    ingredient_id: UUID
    recipe_id: UUID
    created_at: datetime
    updated_at: datetime


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
