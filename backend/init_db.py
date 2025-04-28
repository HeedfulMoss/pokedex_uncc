import json
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Pokemon, Type
import os

# Database connection string
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:password@postgres:5432/pokemon_db")

def init_database():
    print("Initializing database...")
    
    # Create the database engine
    engine = create_engine(DATABASE_URL)
    
    # Create all tables
    Base.metadata.create_all(engine)
    
    # Create a session
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    
    try:
        # Check if data already exists
        if db.query(Pokemon).count() > 0:
            print("Database already has data, skipping initialization")
            return
        
        # Load the Pokemon data from the JSON file
        with open('pokemon_data.json', 'r') as file:
            pokemon_data = json.load(file)
        
        # First, create all type entries
        all_types = set()
        for pokemon_info in pokemon_data.values():
            all_types.update(pokemon_info["types"])
            all_types.update(pokemon_info["weak_against"])
            all_types.update(pokemon_info["strong_against"])
        
        type_objects = {}
        for type_name in all_types:
            type_obj = Type(name=type_name)
            db.add(type_obj)
            type_objects[type_name] = type_obj
        
        # Commit the types
        db.commit()
        
        # Now create the Pokemon entries with their relationships
        for pokemon_name, pokemon_info in pokemon_data.items():
            # Create the Pokemon
            pokemon = Pokemon(name=pokemon_name)
            
            # Add types
            for type_name in pokemon_info["types"]:
                pokemon.types.append(type_objects[type_name])
            
            # Add weak against
            for type_name in pokemon_info["weak_against"]:
                pokemon.weak_against.append(type_objects[type_name])
            
            # Add strong against
            for type_name in pokemon_info["strong_against"]:
                pokemon.strong_against.append(type_objects[type_name])
            
            db.add(pokemon)
        
        # Commit all changes
        db.commit()
        print("Database initialized successfully!")
    
    except Exception as e:
        print(f"Error initializing database: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    init_database()