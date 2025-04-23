"""Advanced features for the Word Definition Memory Game."""

import streamlit as st
import pandas as pd
import random
import time
from typing import List, Dict, Tuple, Optional
import base64
from io import BytesIO

# Game difficulty settings
DIFFICULTIES = {
    "Easy": {"pairs": 4, "color": "#28a745", "icon": "😊", "desc": "Perfect for beginners", "time_limit": 120},
    "Medium": {"pairs": 6, "color": "#ffc107", "icon": "🧠", "desc": "A good challenge", "time_limit": 180},
    "Hard": {"pairs": 8, "color": "#dc3545", "icon": "🔥", "desc": "For memory masters", "time_limit": 240}
}

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
        transition: transform 0.3s, background-color 0.3s;
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
    
    /* Matched pairs - using a more accessible light green */
    .matched-card {
        background-color: #d4edda !important;
        color: #155724 !important;
        border: 2px solid #28a745 !important;
        position: relative;
    }
    
    /* Checkmark icon for matched pairs */
    .matched-card:after {
        content: "✓";
        position: absolute;
        top: 5px;
        right: 5px;
        font-size: 1.2rem;
        color: #28a745;
    }
    
    /* Adding a pattern for additional visual differentiation */
    .matched-card {
        background-image: linear-gradient(45deg, rgba(40, 167, 69, 0.05) 25%, transparent 25%, 
                          transparent 50%, rgba(40, 167, 69, 0.05) 50%, rgba(40, 167, 69, 0.05) 75%, 
                          transparent 75%, transparent) !important;
        background-size: 10px 10px !important;
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
    
    /* Difficulty button styles */
    .difficulty-btn {
        border-radius: 5px;
        padding: 10px;
        text-align: center;
        margin-bottom: 10px;
        cursor: pointer;
        transition: all 0.3s;
    }
    
    .difficulty-btn:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    
    .difficulty-btn.selected {
        border-width: 2px;
        box-shadow: 0 0 0 2px rgba(0,0,0,0.1);
    }
    
    /* Game info panel */
    .game-info-panel {
        background-color: #f8f9fa;
        border-radius: 5px;
        padding: 15px;
        margin-bottom: 20px;
        border-left: 4px solid #6c757d;
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
    
def apply_matched_card_style(placeholder, card_text, card_type):
    """
    Apply custom HTML/CSS for matched cards for better accessibility.
    
    Args:
        placeholder: Streamlit container to render HTML
        card_text: Text content of the card
        card_type: Type of card ("word" or "definition")
    """
    # Create accessible matched card with appropriate styling and ARIA attributes
    if card_type == "word":
        html_content = f"""
        <div class="matched-card-container" style="height: 120px; margin: 5px;">
            <button 
                class="matched-card" 
                style="width: 100%; height: 100%; padding: 10px; font-weight: bold; font-size: 1.2rem;" 
                disabled 
                aria-label="Matched word: {card_text}" 
                aria-disabled="true" 
                role="button">
                {card_text}
                <span class="visually-hidden">(Matched)</span>
            </button>
        </div>
        """
    else:
        html_content = f"""
        <div class="matched-card-container" style="height: 120px; margin: 5px;">
            <button 
                class="matched-card" 
                style="width: 100%; height: 100%; padding: 10px; font-size: 0.9rem;" 
                disabled 
                aria-label="Matched definition: {card_text}" 
                aria-disabled="true" 
                role="button">
                {card_text}
                <span class="visually-hidden">(Matched)</span>
            </button>
        </div>
        """
    
    placeholder.markdown(html_content, unsafe_allow_html=True)

def render_difficulty_selector():
    """
    Render a compact but accessible difficulty selector.
    
    Returns:
        str: The selected difficulty level
    """
    st.subheader("Select Difficulty")
    
    # Initialize selected difficulty if needed
    if 'selected_difficulty' not in st.session_state:
        st.session_state.selected_difficulty = "Easy"
    
    # Layout options in a more compact horizontal format
    cols = st.columns(3)
    
    # Define a more compact representation
    diff_options = {
        "Easy": {"icon": "😊", "color": "#28a745", "pairs": 4},
        "Medium": {"icon": "🧠", "color": "#ffc107", "pairs": 6},
        "Hard": {"icon": "🔥", "color": "#dc3545", "pairs": 8}
    }
    
    # Render the buttons in a row
    for i, (diff_name, diff_info) in enumerate(diff_options.items()):
        with cols[i]:
            is_selected = st.session_state.selected_difficulty == diff_name
            button_type = "primary" if is_selected else "secondary"
            
            if st.button(
                f"{diff_info['icon']} {diff_name}",
                key=f"diff_{diff_name}",
                type=button_type,
                use_container_width=True,
                help=f"{diff_name}: {diff_info['pairs']} pairs to match"
            ):
                st.session_state.selected_difficulty = diff_name
                st.rerun()
    
    # Display a compact info box with difficulty details
    selected = st.session_state.selected_difficulty
    diff_info = DIFFICULTIES[selected]
    
    # More compact info display
    st.markdown(
        f"""<div style="padding:8px; background-color:{diff_info['color']}20; border-left:3px solid {diff_info['color']}; font-size:0.9em;">
        <strong>{selected}</strong> · {diff_info['pairs']} pairs · {diff_info['time_limit']//60}min
        </div>""", 
        unsafe_allow_html=True
    )
    
    return st.session_state.selected_difficulty