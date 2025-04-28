import streamlit as st
import requests
import os
from PIL import Image

# Backend API URL (this will be the service name in docker-compose)
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

# Function to get all Pokémon names from the API
def get_pokemon_names():
    try:
        response = requests.get(f"{BACKEND_URL}/pokemon")
        if response.status_code == 200:
            return response.json()["pokemon"]
        else:
            st.error(f"Failed to fetch Pokémon list: {response.status_code}")
            return []
    except Exception as e:
        st.error(f"Error connecting to backend: {e}")
        return []

# Function to get Pokémon info from the API
def get_pokemon_info(name):
    try:
        response = requests.get(f"{BACKEND_URL}/pokemon/{name}")
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Failed to fetch data for {name}: {response.status_code}")
            return None
    except Exception as e:
        st.error(f"Error connecting to backend: {e}")
        return None

# Function to get Pokémon image URL from the API
def get_pokemon_image_url(name):
    try:
        response = requests.get(f"{BACKEND_URL}/pokemon/{name}/image")
        if response.status_code == 200:
            return response.json()["image_url"]
        else:
            st.warning(f"Image not found for {name}")
            return None
    except Exception as e:
        st.warning(f"Error fetching image for {name}: {e}")
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

    # Get Pokémon names from the API
    pokemon_names = get_pokemon_names()
    
    if not pokemon_names:
        st.error("Could not load Pokémon data. Please make sure the backend is running.")
        return
    
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