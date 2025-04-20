# pokedex_frontend.py
import requests
import json
from bs4 import BeautifulSoup
import streamlit as st
import os
from PIL import Image


with open('pokemon_data.json', 'r') as p:
    pokemon_data = json.load(p)

# Function to get Pokémon info from the database
def get_pokemon_info(name):
    return pokemon_data.get(name)

# Function to get Pokémon image URL using PokeAPI and GitHub CDN
def get_pokemon_image_url(pokemon_name):
    try:
        api_url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_name.lower()}"
        response = requests.get(api_url)
        if response.status_code == 200:
            data = response.json()
            pokemon_id = data['id']
            image_url = f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/{pokemon_id}.png"
            return image_url
    except Exception as e:
        st.warning(f"Image not found for {pokemon_name}: {e}")
    return None

def render_type_images(types_list, scale=1.5):
    cols = st.columns(3)
    for i, t in enumerate(types_list):
        type_image_path = f"types/{t.lower()}.png"
        if os.path.exists(type_image_path):
            with Image.open(type_image_path) as img:
                width, _ = img.size
                scaled_width = int(width * scale)
            with cols[i % 3]:
                st.image(type_image_path, width=scaled_width)
        else:
            st.warning(f"Image for type '{t}' not found.")

# Main app function
def main():
    st.title("Pokedex - Matchups")

    # Dropdown menus for selecting two Pokémon
    pokemon_names = list(pokemon_data.keys())  # Extract Pokémon names from the data
    
    # User selects Pokémon
    pokemon1_name = st.selectbox("Choose your Pokemon", pokemon_names)
    pokemon2_name = st.selectbox("Choose the opposing Pokemon", pokemon_names)

    # Button to compare Pokémon
    if st.button("Compare Pokemon"):
        pokemon1 = get_pokemon_info(pokemon1_name)
        pokemon2 = get_pokemon_info(pokemon2_name)

        if pokemon1 and pokemon2:
            # Displaying information side by side
            col1, col2 = st.columns(2)

            # Left side (your Pokémon)
            with col1:
                st.subheader(pokemon1['name'])

                image_url1 = get_pokemon_image_url(pokemon1['name'])
                if image_url1:
                    st.image(image_url1, use_container_width=True)

                st.write("**Types**:")
                render_type_images(pokemon1['types'])

                st.markdown('<span style="color:red">**Weak Against**:</span>', unsafe_allow_html=True)
                render_type_images(pokemon1['weak_against'])

                st.markdown('<span style="color:lightgreen">**Strong Against**:</span>', unsafe_allow_html=True)
                render_type_images(pokemon1['strong_against'])

            # Right side (opposing Pokemon)
            with col2:
                st.subheader(pokemon2['name'])

                image_url2 = get_pokemon_image_url(pokemon2['name'])
                if image_url2:
                    st.image(image_url2, use_container_width=True)
                st.write("**Types**:")
                render_type_images(pokemon2['types'])

                st.markdown('<span style="color:red">**Weak Against**:</span>', unsafe_allow_html=True)
                render_type_images(pokemon2['weak_against'])

                st.markdown('<span style="color:lightgreen">**Strong Against**:</span>', unsafe_allow_html=True)
                render_type_images(pokemon2['strong_against'])
        else:
            st.error("Could not retrieve Pokémon data.")

if __name__ == "__main__":
    main()
