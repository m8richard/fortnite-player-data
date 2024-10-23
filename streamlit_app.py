import streamlit as st
import pandas as pd
import random
import math
from pathlib import Path

# Set the title and logo for the page
st.set_page_config(
    page_title='M8 Fortnite Data Overview',
    page_icon="assets/M8Patch.png",  # Set the path to your logo in the "assets" folder
)

# -----------------------------------------------------------------------------
# Add the logo and title side by side
col1, col2 = st.columns([1, 3])  # Adjust the column proportions as needed

with col1:
    st.image("assets/M8Patch.png", width=75)  # Display the logo on the left

with col2:
    st.title("M8 Fortnite Data Overview TEST")  # Display the updated title on the right

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

# -----------------------------------------------------------------------------
# Page layout: Player and Tournament selection

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

# -----------------------------------------------------------------------------
# Function to display data in squares (customized aesthetic)

def display_stat_square(label, value):
    st.markdown(
        f"""
        <div style="background-color: #f9f9f9; padding: 20px; border-radius: 10px; border: 2px solid #ddd; text-align: center;">
            <h4 style="margin: 0;">{label}</h4>
            <p style="font-size: 24px; margin: 0; font-weight: bold;">{value}</p>
        </div>
        """, unsafe_allow_html=True
    )

# -----------------------------------------------------------------------------
# Display Player and Duo's Tournament Data

st.header(f'{selected_player} - {selected_tournament}', divider='gray')

if filtered_df.empty:
    st.warning(f"No data available for {selected_player} in {selected_tournament}")
else:
    player_data = filtered_df.iloc[0]  # Get the first (and only) row for the player and tournament

    # Display Rank and Points Earned above the two columns
    cols = st.columns([1, 1])  # Create two equally wide columns
    with cols[0]:
        display_stat_square('Rank', player_data['Rank'])
    with cols[1]:
        display_stat_square('Points Earned', player_data['Points Earned'])

    st.header(f'', divider='gray')
    # Now create two columns for other stats: one for the player, one for the duo
    cols = st.columns(2)

    # Display Player's Stats in Squares
    with cols[0]:
        st.subheader(f"{selected_player} :")
        display_stat_square('Damage Dealt', player_data['Damage Dealt'])
        display_stat_square('Damage Taken', player_data['Damage Taken'])
        display_stat_square('Damage Ratio', f"{player_data['Damage Ratio']:.2f}")
        display_stat_square('Builds', player_data['Builds'])
        display_stat_square('Farmed', player_data['Farmed'])

    # Display Duo's Stats in Squares
    with cols[1]:
        st.subheader(f"{player_data['Duo']} (duo) :")
        display_stat_square('Duo Damage Dealt', player_data['Duo Damage Dealt'])
        display_stat_square('Duo Damage Taken', player_data['Duo Damage Taken'])
        display_stat_square('Duo Damage Ratio', f"{player_data['Duo Damage Ratio']:.2f}")
        display_stat_square('Duo Builds', player_data['Duo Builds'])
        display_stat_square('Duo Farmed', player_data['Duo Farmed'])
