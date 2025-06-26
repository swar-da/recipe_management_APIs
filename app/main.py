from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import connect_to_db, AsyncSession
from app.routes import router as api_router
import app


app = FastAPI( title= "Recipe Management",
    description="Manage's recipes, ingredients",
    version="1.0.0"
    )

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"], 
    )

app.include_router(api_router)
