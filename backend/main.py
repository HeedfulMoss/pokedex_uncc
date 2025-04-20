from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import json
import requests
import os

app = FastAPI(title="Pokemon API")

# Add CORS middleware to allow cross-origin requests from frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For development, will restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load the Pokemon data
with open('pokemon_data.json', 'r') as file:
    pokemon_data = json.load(file)

@app.get("/")
def read_root():
    """Root endpoint to check if API is running"""
    return {"status": "Pokemon API is running"}

@app.get("/pokemon")
def get_pokemon_list():
    """Get a list of all Pokemon names"""
    return {"pokemon": list(pokemon_data.keys())}

@app.get("/pokemon/{name}")
def get_pokemon_info(name: str):
    """Get detailed information about a specific Pokemon"""
    if name not in pokemon_data:
        raise HTTPException(status_code=404, detail=f"Pokemon {name} not found")
    return pokemon_data[name]

@app.get("/pokemon/{name}/image")
def get_pokemon_image(name: str):
    """Get the image URL for a specific Pokemon"""
    if name not in pokemon_data:
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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)