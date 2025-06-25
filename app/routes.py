from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from typing import List
from app.database import get_db
from app import crud, schemas
from app.schemas import UserCreate, UserOut, Token
from app.models import User
from app.auth.token import hash_password, verify_password, create_access_token
from app.auth.dependencies import get_current_user

router = APIRouter()

# ---------------------- User Routes ----------------------
@router.post("/register", response_model=schemas.UserRead)
async def register_user(user: schemas.UserCreate, db: AsyncSession = Depends(get_db)):
    db_user = await crud.get_user_by_email(db, user.email)
    print("Incoming user payload:", user)
    print("user_name:", user.user_name)  
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return await crud.create_user(db, user)

@router.post("/login", response_model=schemas.Token)
async def login(user: schemas.UserCreate, db: AsyncSession = Depends(get_db)):
    db_user = await crud.get_user_by_email(db, user.email)
    if not db_user or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    token = create_access_token({"sub": db_user.email})
    return {"access_token": token}

@router.get("/me", response_model=schemas.UserRead)
async def get_profile(current_user: User = Depends(get_current_user)):
    return current_user

# ---------------------- Recipe Routes ----------------------
@router.post("/recipes/", response_model=schemas.RecipeRead)
async def create_recipe(
    recipe: schemas.RecipeCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return await crud.create_recipe(db, recipe, current_user.id)

@router.get("/recipes/", response_model=List[schemas.RecipeRead])
async def read_all_recipes(db: AsyncSession = Depends(get_db)):
    return await crud.get_all_recipes(db)

@router.get("/recipes/{recipe_id}", response_model=schemas.RecipeRead)
async def read_recipe(recipe_id: UUID, db: AsyncSession = Depends(get_db)):
    recipe = await crud.get_recipe_by_id(db, recipe_id)
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
    return recipe

@router.put("/recipes/{recipe_id}", response_model=schemas.RecipeRead)
async def update_recipe(
    recipe_id: UUID,
    recipe: schemas.RecipeCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    updated = await crud.update_recipe(db, recipe_id, recipe, current_user.id)
    if not updated:
        raise HTTPException(status_code=404, detail="Recipe not found or unauthorized")
    return updated

@router.delete("/recipes/{recipe_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_recipe(
    recipe_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    deleted = await crud.delete_recipe(db, recipe_id, current_user.id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Recipe not found or unauthorized")
    return None

# ---------------------- Ingredient Routes ----------------------
@router.post("/recipes/{recipe_id}/ingredients/", response_model=schemas.RecipeIngredientRead)
async def add_ingredient(
    recipe_id: UUID,
    ingredient: schemas.RecipeIngredientCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return await crud.add_ingredient(db, ingredient, recipe_id, current_user.id)

@router.get("/recipes/{recipe_id}/ingredients/", response_model=List[schemas.RecipeIngredientRead])
async def get_ingredients(recipe_id: UUID, db: AsyncSession = Depends(get_db)):
    return await crud.get_ingredients_for_recipe(db, recipe_id)

# ---------------------- Step Routes ----------------------
@router.post("/recipes/{recipe_id}/steps/", response_model=schemas.RecipeStepRead)
async def add_step(
    recipe_id: UUID,
    step: schemas.RecipeStepCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return await crud.add_step(db, step, recipe_id, current_user.id)

@router.get("/recipes/{recipe_id}/steps/", response_model=List[schemas.RecipeStepRead])
async def get_steps(recipe_id: UUID, db: AsyncSession = Depends(get_db)):
    return await crud.get_steps_for_recipe(db, recipe_id)
