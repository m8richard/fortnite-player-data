import streamlit as st
import pandas as pd
import random
import math
from pathlib import Path

# Set the title and logo for the page
st.set_page_config(
    page_title='M8 Fortnite Data Overview',
    page_icon="assets/M8Patch.png",  # Set the path to your logo in the "assets" folder
    layout='wide'  # Set the layout to 'wide' to use the full screen width
)

# ----------------------------------------------------------------------------- 
# Function to display data in squares (customized for light and dark modes)
def display_stat_square(label, value):
    # Check if the user is using light or dark mode based on the theme base
    theme_base = st.get_option("theme.base") or "light"  # Default to light if not found

    # Define colors based on theme mode
    if theme_base == "dark":
        square_background_color = "#333333"
        square_text_color = "#FFFFFF"
        square_border_color = "#555555"
    else:
        square_background_color = "#f9f9f9"
        square_text_color = "#000000"
        square_border_color = "#ddd"

    st.markdown(
        f"""
        <div style="background-color: {square_background_color}; color: {square_text_color}; padding: 20px; border-radius: 35px; border: 3px solid {square_border_color}; text-align: center; margin: 0px 0px 10px 0px;">
            <p style="font-size: 24px; margin: 0; font-weight: normal;">{label}</p>
            <p style="font-size: 24px; margin: 0; font-weight: semi-bold;">{value}</p>
        </div>
        """, unsafe_allow_html=True
    )

# ----------------------------------------------------------------------------- 
# Add the logo, title, and inputs on the left side, and player's stats on the right
main_cols = st.columns([2, 3])  # 2/5 for the rest, 3/5 for the player's data

# Left column with the logo, title, and inputs
with main_cols[0]:
    col1, col2 = st.columns([1, 3])  # Adjust the column proportions as needed

    with col1:
        st.image("assets/M8Patch.png", width=100)  # Display the logo on the left

    with col2:
        st.title("M8 Fortnite Data Overview")  # Display the updated title on the right

    # Placeholder for Fortnite tournament data.
    @st.cache_data
    def get_fortnite_data():
        """Placeholder Fortnite tournament data."""
        players = ['Snayzy', 'Podasai', 'Vanyak']
        tournaments = ['Major 1', 'Major 2', 'Major 3']

        # Generate placeholder data
        data = []
        for player in players:
            for tournament in tournaments:
                data.append({
                    'Player': player,
                    'Tournament': tournament,
                    'Rank': random.randint(1, 100),
                    'Points Earned': random.randint(100, 300),
                    'Damage Dealt': random.randint(1000, 5000),
                    'Damage Taken': random.randint(500, 3000),
                    'Builds': random.randint(50, 200),
                    'Farmed': random.randint(300, 1000),
                    'Duo': random.choice([p for p in players if p != player]),  # Duo can't be the player themselves
                    'Duo Damage Dealt': random.randint(1000, 5000),
                    'Duo Damage Taken': random.randint(500, 3000),
                    'Duo Builds': random.randint(50, 200),
                    'Duo Farmed': random.randint(300, 1000),
                })

        fortnite_df = pd.DataFrame(data)
        fortnite_df['Damage Ratio'] = fortnite_df['Damage Dealt'] / fortnite_df['Damage Taken']
        fortnite_df['Duo Damage Ratio'] = fortnite_df['Duo Damage Dealt'] / fortnite_df['Duo Damage Taken']
        return fortnite_df

    # Get the placeholder Fortnite data
    fortnite_df = get_fortnite_data()

    # Select a player
    players = fortnite_df['Player'].unique()
    selected_player = st.selectbox('Select a Player', players)

    # Filter the tournaments the player has participated in
    player_tournaments = fortnite_df[fortnite_df['Player'] == selected_player]['Tournament'].unique()
    selected_tournament = st.selectbox('Select a Tournament', player_tournaments)

    # Filter the data based on selected player and tournament
    filtered_df = fortnite_df[
        (fortnite_df['Player'] == selected_player) &
        (fortnite_df['Tournament'] == selected_tournament)
    ]

    # Display Player and Duo's Tournament Data
    if filtered_df.empty:
        st.warning(f"No data available for {selected_player} in {selected_tournament}")
    else:
        player_data = filtered_df.iloc[0]  # Get the first (and only) row for the player and tournament

        # Display the player's photo, Rank, and Points Earned
        cols = st.columns([1, 2])  # One column for the image and the rest for the stats

        with cols[0]:
            st.image(f"assets/{selected_player}.png", width=170)  # Display player's photo

        with cols[1]:
            display_stat_square('Rank', player_data['Rank'])
            display_stat_square('Points Earned', player_data['Points Earned'])

# Right column with player and duo stats
with main_cols[1]:
    cols = st.columns(2)

    # Center the subheader for the player
    with cols[0]:
        st.markdown(f"<h4 style='text-align: center;'>{selected_player}:</h4>", unsafe_allow_html=True)
        display_stat_square('Damage Dealt', player_data['Damage Dealt'])
        display_stat_square('Damage Taken', player_data['Damage Taken'])
        display_stat_square('Damage Ratio', f"{player_data['Damage Ratio']:.2f}")
        display_stat_square('Builds', player_data['Builds'])
        display_stat_square('Farmed', player_data['Farmed'])

    # Center the subheader for the duo
    with cols[1]:
        st.markdown(f"<h4 style='text-align: center;'>Duo ({player_data['Duo']}):</h4>", unsafe_allow_html=True)
        display_stat_square('Damage Dealt', player_data['Duo Damage Dealt'])
        display_stat_square('Damage Taken', player_data['Duo Damage Taken'])
        display_stat_square('Damage Ratio', f"{player_data['Duo Damage Ratio']:.2f}")
        display_stat_square('Builds', player_data['Duo Builds'])
        display_stat_square('Farmed', player_data['Duo Farmed'])
