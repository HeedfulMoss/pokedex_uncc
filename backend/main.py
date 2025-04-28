from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from models import Base, Pokemon, Type
from init_db import init_database

import json
import requests
import os
import uvicorn

# Database connection
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:password@postgres:5432/pokemon_db")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

app = FastAPI(title="Pokemon API")

# Add CORS middleware to allow cross-origin requests from frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For development, will restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root():
    """Root endpoint to check if API is running"""
    return {"status": "Pokemon API is running"}

@app.get("/pokemon")
def get_pokemon_list():
    """Get a list of all Pokemon names"""
    pokemon_list = db.query(Pokemon.name).all()
    return {"pokemon": [pokemon[0] for pokemon in pokemon_list]}

@app.get("/pokemon/{name}")
def get_pokemon_info(name: str, db: Session = Depends(get_db)):
    """Get detailed information about a specific Pokemon"""
    pokemon = db.query(Pokemon).filter(Pokemon.name == name).first()
    
    if not pokemon:
        raise HTTPException(status_code=404, detail=f"Pokemon {name} not found")
    
    # Format the response to match the JSON structure expected by the frontend
    return {
        "name": pokemon.name,
        "types": [type.name for type in pokemon.types],
        "weak_against": [type.name for type in pokemon.weak_against],
        "strong_against": [type.name for type in pokemon.strong_against]
    }

@app.get("/pokemon/{name}/image")
def get_pokemon_image(name: str, db: Session = Depends(get_db)):
    """Get the image URL for a specific Pokemon"""
    # Check if the Pokemon exists
    pokemon = db.query(Pokemon).filter(Pokemon.name == name).first()
    
    if not pokemon:
        raise HTTPException(status_code=404, detail=f"Pokemon {name} not found")
    
    try:
        api_url = f"https://pokeapi.co/api/v2/pokemon/{name.lower()}"
        response = requests.get(api_url)
        if response.status_code == 200:
            data = response.json()
            pokemon_id = data['id']
            image_url = f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/{pokemon_id}.png"
            return {"image_url": image_url}
        else:
            raise HTTPException(status_code=404, detail=f"Pokemon image not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching Pokemon image: {str(e)}")

# Initialize database on startup
@app.on_event("startup")
async def startup_event():
    init_database()

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)