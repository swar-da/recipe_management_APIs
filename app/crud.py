from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from uuid import UUID
from app.models import User, Recipe, RecipeIngredient, RecipeStep
from app.schemas import UserCreate, RecipeCreate, RecipeIngredientCreate, RecipeStepCreate
import uuid
from app import models
from passlib.context import CryptContext
from app.security import get_password_hash

# ---------------------- User CRUD ----------------------
async def create_user(db: AsyncSession, user: UserCreate):
    hashed_password = get_password_hash(user.password)  

    new_user = User(
        user_id=uuid.uuid4(),
        user_name=user.user_name,
        email=user.email,
        hashed_password=hashed_password 
    )
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user

async def get_user_by_email(db: AsyncSession, email: str):
    result = await db.execute(select(User).filter_by(email=email))
    return result.scalar_one_or_none()

# ---------------------- Recipe CRUD ----------------------
async def create_recipe(db: AsyncSession, recipe: RecipeCreate, user_id: UUID):
    new_recipe = Recipe(
        recipe_id=uuid.uuid4(),
        title=recipe.title,
        description=recipe.description,
        status=recipe.status,
        owner_id=user_id
    )
    db.add(new_recipe)
    await db.commit()
    await db.refresh(new_recipe)
    return new_recipe

async def get_all_recipes(db: AsyncSession):
    result = await db.execute(select(Recipe))
    return result.scalars().all()

async def get_recipe_by_id(db: AsyncSession, recipe_id: UUID):
    result = await db.execute(select(Recipe).filter_by(recipe_id=recipe_id))
    return result.scalar_one_or_none()

async def update_recipe(db: AsyncSession, recipe_id: UUID, updated_data: RecipeCreate):
    query = select(Recipe).where(Recipe.recipe_id == recipe_id)
    result = await db.execute(query)
    db_recipe = result.scalar_one_or_none()
    if not db_recipe:
        return None
    
    update_recipe = updated_data.dict(exclude_unset=True)
    for key, value in update_recipe.items():
        setattr(db_recipe, key, value)

    await db.commit()
    await db.refresh(db_recipe)
    return db_recipe


async def delete_recipe(db, recipe_id, user_id):
    recipe = db.query(models.Recipe).filter(
        models.Recipe.recipe_id == recipe_id,
        models.Recipe.owner_id == user_id
    ).first()

    if not recipe:
        return None

    db.delete(recipe)
    db.commit()
    return recipe


# ---------------------- Ingredient CRUD ----------------------
from sqlalchemy import select
from sqlalchemy.exc import NoResultFound

async def add_ingredient(db: AsyncSession, ingredient: RecipeIngredientCreate, recipe_id: UUID, user_id: int):
    stmt = select(models.Recipe).where(
        models.Recipe.recipe_id == recipe_id,
        models.Recipe.owner_id == user_id
    )

    result = (await db.execute(stmt)).scalars().first()
    if not result:
        raise HTTPException(status_code=404, detail="Recipe not found or unauthorized")

    new_ingredient = models.RecipeIngredient(
        name=ingredient.name,
        quantity=ingredient.quantity,
        recipe_id=recipe_id
    )
    db.add(new_ingredient)
    db.commit()
    db.refresh(new_ingredient)
    return new_ingredient

async def get_ingredients_for_recipe(db: AsyncSession, recipe_id: UUID):
    result = await db.execute(select(RecipeIngredient).filter_by(recipe_id=recipe_id))
    return result.scalars().all()

# ---------------------- Steps CRUD ----------------------
async def add_step(db: AsyncSession, step: RecipeStepCreate, recipe_id: UUID):
    new_step = RecipeStep(
        step_id=uuid.uuid4(),
        description=step.description,
        order=step.order,
        recipe_id=recipe_id
    )
    db.add(new_step)
    await db.commit()
    await db.refresh(new_step)
    return new_step

async def get_steps_for_recipe(db: AsyncSession, recipe_id: UUID):
    result = await db.execute(
        select(RecipeStep).filter_by(recipe_id=recipe_id).order_by(RecipeStep.order)
    )
    return result.scalars().all()
