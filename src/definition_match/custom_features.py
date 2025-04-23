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
    Render a visually appealing difficulty selector.
    
    Returns:
        str: The selected difficulty level
    """
    st.subheader("Select Difficulty")
    
    # Initialize selected difficulty if needed
    if 'selected_difficulty' not in st.session_state:
        st.session_state.selected_difficulty = "Easy"
        
    # Create columns for the difficulty options
    diff_cols = st.columns(3)
    
    # Render each difficulty option
    for i, (diff_name, diff_info) in enumerate(DIFFICULTIES.items()):
        with diff_cols[i]:
            is_selected = st.session_state.selected_difficulty == diff_name
            diff_style = "selected" if is_selected else ""
            
            # Render custom button with HTML
            html = f"""
            <div class="difficulty-btn {diff_style}" 
                 style="background-color: {diff_info['color']}20; 
                        border: 2px solid {diff_info['color'] if is_selected else diff_info['color'] + '40'};
                        color: {diff_info['color']};">
                <div style="font-size: 1.5rem;">{diff_info['icon']}</div>
                <div style="font-weight: bold;">{diff_name}</div>
                <div style="font-size: 0.8rem;">{diff_info['pairs']} pairs</div>
            </div>
            """
            
            # Use a button with the same name to handle clicks
            if st.button(diff_name, key=f"diff_{diff_name}", use_container_width=True):
                st.session_state.selected_difficulty = diff_name
                st.rerun()
    
    # Display more info about selected difficulty
    selected = st.session_state.selected_difficulty
    diff_info = DIFFICULTIES[selected]
    
    st.markdown(
        f"""
        <div style="padding: 10px; border-radius: 5px; 
             background-color: {diff_info['color']}20; 
             border-left: 4px solid {diff_info['color']};">
            <h4 style="margin: 0; color: {diff_info['color']};">
                {selected} Mode {diff_info['icon']}
            </h4>
            <p>{diff_info['desc']}</p>
            <p><strong>Cards to match:</strong> {diff_info['pairs']} pairs</p>
            <p><strong>Time limit:</strong> {diff_info['time_limit'] // 60} minutes</p>
        </div>
        """, 
        unsafe_allow_html=True
    )
    
    return st.session_state.selected_difficulty