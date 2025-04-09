# pokedex_frontend.py
import streamlit as st
from Pokemon_database import pokemon_data  # Import the pokemon data

# Function to get Pokémon info from the database
def get_pokemon_info(name):
    return pokemon_data.get(name)

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
                st.write(f"**Types**: {', '.join(pokemon1['types'])}")
                st.write(f"**Weak Against**: {', '.join(pokemon1['weak_against'])}")
                st.write(f"**Strong Against**: {', '.join(pokemon1['strong_against'])}")
            



            # Right side (opposing Pokemon)
            with col2:
                st.subheader(pokemon2['name'])
                st.write(f"**Types**: {', '.join(pokemon2['types'])}")
                st.write(f"**Weak Against**: {', '.join(pokemon2['weak_against'])}")
                st.write(f"**Strong Against**: {', '.join(pokemon2['strong_against'])}")
        else:
            st.error("Error for collum portion")

if __name__ == "__main__":
    main()
