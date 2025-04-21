"""Advanced features for the Word Definition Memory Game."""

import streamlit as st
import pandas as pd
import random
import time
from typing import List, Dict, Tuple, Optional
import base64
from io import BytesIO

def add_custom_css():
    """Add custom CSS styles to the Streamlit app."""
    css = """
    <style>
    /* Card styling */
    div[data-testid="stButton"] > button {
        height: 120px;
        display: flex;
        align-items: center;
        justify-content: center;
        text-align: center;
        transition: transform 0.3s;
        margin: 5px;
    }
    
    /* Card hover effect */
    div[data-testid="stButton"] > button:hover:not([disabled]) {
        transform: scale(1.03);
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }
    
    /* Question mark style */
    div[data-testid="stButton"] > button:not([disabled]) {
        font-size: 2rem;
        font-weight: bold;
    }
    
    /* Matched pairs */
    .matched {
        background-color: #d4edda !important;
        color: #155724 !important;
    }
    
    /* Title styling */
    h1 {
        color: #4527a0;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.1);
    }
    
    /* Game timer */
    .timer {
        font-family: monospace;
        font-size: 1.5rem;
        color: #555;
    }
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

def create_leaderboard_placeholder():
    """Create an empty leaderboard if it doesn't exist in session state."""
    if 'leaderboard' not in st.session_state:
        st.session_state.leaderboard = pd.DataFrame(
            columns=['Player', 'Category', 'Difficulty', 'Score', 'Time', 'Date']
        )

def add_to_leaderboard(player_name: str, category: str, 
                      difficulty: str, score: int, time_seconds: int):
    """
    Add a new entry to the leaderboard.
    
    Args:
        player_name: Name of the player
        category: Game category played
        difficulty: Difficulty level
        score: Final score (0-100)
        time_seconds: Time taken in seconds
    """
    create_leaderboard_placeholder()
    
    # Format time as minutes:seconds
    minutes, seconds = divmod(time_seconds, 60)
    time_str = f"{minutes:02d}:{seconds:02d}"
    
    # Add timestamp
    import datetime
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    
    # Create new entry
    new_entry = pd.DataFrame([{
        'Player': player_name,
        'Category': category,
        'Difficulty': difficulty,
        'Score': score,
        'Time': time_str,
        'Date': now
    }])
    
    # Append to existing leaderboard
    st.session_state.leaderboard = pd.concat([st.session_state.leaderboard, new_entry], ignore_index=True)
    
    