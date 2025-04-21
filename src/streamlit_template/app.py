"""Main Streamlit application for Word Definition Memory Game."""

import streamlit as st
import pandas as pd
import random
import time
from typing import List, Dict, Tuple

# Set page configuration
st.set_page_config(
    page_title="Word Definition Memory Game",
    page_icon="🧠",
    layout="wide"
)

# Initialize session state variables if they don't exist
if 'game_active' not in st.session_state:
    st.session_state.game_active = False
if 'selected_cards' not in st.session_state:
    st.session_state.selected_cards = []
if 'matched_pairs' not in st.session_state:
    st.session_state.matched_pairs = []
if 'attempts' not in st.session_state:
    st.session_state.attempts = 0
if 'start_time' not in st.session_state:
    st.session_state.start_time = None
if 'difficulty' not in st.session_state:
    st.session_state.difficulty = "Easy"

# Sample word-definition pairs for different categories
WORD_SETS = {
    "Technology": {
        "Algorithm": "A step-by-step procedure for solving a problem or accomplishing a task",
        "Bandwidth": "The maximum rate of data transfer across a given path",
        "Cache": "A temporary storage area where frequently accessed data can be stored for rapid access",
        "Database": "An organized collection of structured information or data",
        "Encryption": "The process of converting information into a code to prevent unauthorized access",
        "Firewall": "A network security system that monitors and controls incoming and outgoing network traffic",
        "GUI": "Graphical User Interface - a visual way of interacting with a computer using icons and graphics",
        "HTTP": "Hypertext Transfer Protocol - the foundation of data communication for the World Wide Web"
    },
    "Science": {
        "Atom": "The basic unit of matter consisting of a nucleus and electrons",
        "Biology": "The study of living organisms and their interactions with the environment",
        "Chemistry": "The study of matter, its properties, and the changes it undergoes",
        "DNA": "A molecule that carries genetic instructions for development and functioning of organisms",
        "Ecosystem": "A community of living organisms together with the nonliving components of their environment",
        "Fusion": "The process of combining atomic nuclei to form heavier nuclei, releasing energy",
        "Gravity": "The force that attracts objects toward one another, especially the attraction of earth's mass",
        "Hypothesis": "A proposed explanation for a phenomenon that can be tested through further investigation"
    },
    "Literature": {
        "Allegory": "A story with hidden meaning, typically with moral or political significance",
        "Metaphor": "A figure of speech making an implicit comparison without using 'like' or 'as'",
        "Protagonist": "The main character in a story, often in conflict with an antagonist",
        "Sonnet": "A 14-line poem with a specific rhyme scheme and structure",
        "Irony": "The expression of meaning using language that normally signifies the opposite",
        "Narrative": "A spoken or written account of connected events; a story",
        "Imagery": "Visually descriptive or figurative language in a literary work",
        "Foreshadowing": "A warning or indication of a future event in the narrative"
    }
}

def get_word_pairs(category: str, count: int) -> List[Tuple[str, str]]:
    """
    Get a subset of word-definition pairs for the game.
    
    Args:
        category: The category to select words from
        count: Number of pairs to select
        
    Returns:
        List of (word, definition) tuples
    """
    all_pairs = list(WORD_SETS[category].items())
    return random.sample(all_pairs, min(count, len(all_pairs)))

def reset_game() -> None:
    """Reset the game state."""
    st.session_state.game_active = False
    st.session_state.selected_cards = []
    st.session_state.matched_pairs = []
    st.session_state.attempts = 0
    st.session_state.start_time = None

def start_game(category: str, difficulty: str) -> None:
    """
    Start a new game with the given parameters.
    
    Args:
        category: Category for word pairs
        difficulty: Difficulty level determining number of pairs
    """
    # Determine number of pairs based on difficulty
    pair_counts = {"Easy": 4, "Medium": 6, "Hard": 8}
    count = pair_counts.get(difficulty, 4)
    
    # Get word pairs and set up the game
    pairs = get_word_pairs(category, count)
    
    # Create a list of all cards (words and definitions)
    all_cards = []
    for word, definition in pairs:
        all_cards.append(("word", word, definition))
        all_cards.append(("definition", definition, word))
    
    # Shuffle the cards
    random.shuffle(all_cards)
    
    # Store the game state
    st.session_state.all_cards = all_cards
    st.session_state.game_active = True
    st.session_state.matched_pairs = []
    st.session_state.selected_cards = []
    st.session_state.attempts = 0
    st.session_state.start_time = time.time()
    st.session_state.difficulty = difficulty

def handle_card_click(card_index: int) -> None:
    """
    Handle a card click event.
    
    Args:
        card_index: Index of the clicked card
    """
    # Skip if card is already matched or selected
    card_type, card_text, pair_text = st.session_state.all_cards[card_index]
    
    card_key = f"{card_index}:{card_text}"
    if card_key in st.session_state.matched_pairs or card_key in st.session_state.selected_cards:
        return
    
    # Add to selected cards
    st.session_state.selected_cards.append(card_key)
    
    # If we have two selected cards, check for a match
    if len(st.session_state.selected_cards) == 2:
        st.session_state.attempts += 1
        
        # Get the details of both selected cards
        idx1, text1 = st.session_state.selected_cards[0].split(":", 1)
        idx2, text2 = st.session_state.selected_cards[1].split(":", 1)
        
        card1_type, card1_text, card1_pair = st.session_state.all_cards[int(idx1)]
        card2_type, card2_text, card2_pair = st.session_state.all_cards[int(idx2)]
        
        # Check if they form a matching pair (one word, one definition)
        if (card1_type != card2_type) and (card1_pair == card2_text) and (card2_pair == card1_text):
            # It's a match! Add both cards to matched pairs
            st.session_state.matched_pairs.extend(st.session_state.selected_cards)
            
            # Clear selected cards immediately for matches
            st.session_state.selected_cards = []
        else:
            # For non-matches, we'll keep the cards in the selected_cards list
            # They will be displayed until the next interaction
            
            # Store the non-matching pair in session state
            if 'non_match_time' not in st.session_state:
                st.session_state.non_match_time = time.time()
                
            # We'll clear these in the main loop rather than here
            # This allows both cards to remain visible

def main() -> None:
    """Main application function."""
    st.title("🧠 Word Definition Memory Game")
    
    # Sidebar for game controls
    with st.sidebar:
        st.header("Game Settings")
        
        # Category selection
        category = st.selectbox(
            "Select Category", 
            options=list(WORD_SETS.keys()),
            index=0
        )
        
        # Difficulty selection
        difficulty = st.select_slider(
            "Difficulty",
            options=["Easy", "Medium", "Hard"],
            value=st.session_state.difficulty
        )
        
        # Start game button
        if st.button("New Game"):
            start_game(category, difficulty)
        
        # Show instructions
        with st.expander("How to Play"):
            st.markdown("""
            1. Click on cards to flip them over
            2. Try to match each word with its correct definition
            3. The game is complete when all pairs are matched
            4. Fewer attempts = better score!
            """)
        
        # Display stats during active game
        if st.session_state.game_active:
            st.divider()
            st.subheader("Game Statistics")
            
            # Calculate completion percentage
            total_pairs = len(st.session_state.all_cards) // 2
            matched_count = len(st.session_state.matched_pairs) // 2
            completion = (matched_count / total_pairs) * 100
            
            st.metric("Progress", f"{matched_count}/{total_pairs} pairs")
            st.progress(completion / 100)
            st.metric("Attempts", st.session_state.attempts)
            
            # Display timer if game is in progress
            if st.session_state.start_time and matched_count < total_pairs:
                elapsed = int(time.time() - st.session_state.start_time)
                minutes, seconds = divmod(elapsed, 60)
                st.metric("Time", f"{minutes:02d}:{seconds:02d}")
    
    # Check if we need to clear non-matching cards
    if 'non_match_time' in st.session_state and st.session_state.selected_cards:
        current_time = time.time()
        # Give players 2 seconds to see both cards
        if current_time - st.session_state.non_match_time > 2.0:
            # Clear the selected cards after delay
            st.session_state.selected_cards = []
            # Reset the timer
            del st.session_state.non_match_time
            # Force a rerun to update the UI
            st.rerun()
    
    # Main game area
    if not st.session_state.game_active:
        # Show welcome screen when no game is active
        st.header("Welcome to the Word Definition Memory Game!")
        st.write("Select a category and difficulty level, then click 'New Game' to start.")
        
        # Display sample words from each category
        for cat_name, word_dict in WORD_SETS.items():
            with st.expander(f"Sample Words: {cat_name}"):
                sample_words = list(word_dict.keys())[:3]
                for word in sample_words:
                    st.markdown(f"**{word}**: {word_dict[word]}")
                    
        # Add file uploader for custom words
        st.subheader("Upload Custom Words")
        uploaded_file = st.file_uploader("Choose a CSV file with words and definitions", type="csv")
        if uploaded_file is not None:
            try:
                df = pd.read_csv(uploaded_file)
                
                # Validate the dataframe has required columns
                required_cols = ['word', 'definition']
                missing_cols = [col for col in required_cols if col not in df.columns]
                
                if missing_cols:
                    st.error(f"CSV is missing required columns: {', '.join(missing_cols)}")
                else:
                    # Process the custom words
                    if 'category' in df.columns:
                        # Group by category
                        for category_name, group in df.groupby('category'):
                            word_dict = {row['word']: row['definition'] for _, row in group.iterrows()}
                            WORD_SETS[category_name] = word_dict
                    else:
                        # No category column, use a default category
                        word_dict = {row['word']: row['definition'] for _, row in df.iterrows()}
                        WORD_SETS["Custom Words"] = word_dict
                    
                    st.success(f"Successfully loaded {len(df)} custom words!")
            except Exception as e:
                st.error(f"Error processing file: {str(e)}")
    else:
        # Game board
        cols_per_row = 4
        num_cards = len(st.session_state.all_cards)
        
        # Check if the game is completed
        total_pairs = num_cards // 2
        matched_count = len(st.session_state.matched_pairs) // 2
        
        if matched_count >= total_pairs:
            # Game completed
            elapsed = int(time.time() - st.session_state.start_time)
            minutes, seconds = divmod(elapsed, 60)
            
            st.markdown("### 🎉 Congratulations! You completed the game!")
            st.markdown(f"⏱️ Time: {minutes:02d}:{seconds:02d} | 🔄 Attempts: {st.session_state.attempts}")
            
            efficiency = (total_pairs / st.session_state.attempts) * 100
            st.metric("Efficiency Score", f"{efficiency:.1f}%", 
                      help="100% means you found all pairs without any mistakes")
            
            if st.button("Play Again"):
                reset_game()
        else:
            # Active game - display the card grid
            # Determine grid layout based on number of cards
            if num_cards <= 8:
                cols_per_row = 4
            elif num_cards <= 12:
                cols_per_row = 4
            else:
                cols_per_row = 4
            
            # Create rows of cards
            for row_idx in range(0, num_cards, cols_per_row):
                cols = st.columns(cols_per_row)
                
                for i in range(cols_per_row):
                    card_idx = row_idx + i
                    if card_idx < num_cards:
                        card_type, card_text, _ = st.session_state.all_cards[card_idx]
                        card_key = f"{card_idx}:{card_text}"
                        
                        # Determine card state
                        if card_key in st.session_state.matched_pairs:
                            # Matched card - show as green
                            card_color = "primary"
                            disabled = True
                            show_content = True
                        elif card_key in st.session_state.selected_cards:
                            # Selected card - show content
                            card_color = "secondary"
                            disabled = True
                            show_content = True
                        else:
                            # Unselected card - show back
                            card_color = "secondary"
                            disabled = False
                            show_content = False
                        
                        # Create the card button
                        with cols[i]:
                            # Use different styles for word and definition cards
                            if show_content:
                                if card_type == "word":
                                    # Words get a header style
                                    st.button(
                                        f"## {card_text}",
                                        key=f"card_{card_idx}",
                                        type=card_color,
                                        disabled=disabled,
                                        use_container_width=True,
                                        on_click=handle_card_click,
                                        args=(card_idx,)
                                    )
                                else:
                                    # Definitions get a smaller text style
                                    st.button(
                                        card_text,
                                        key=f"card_{card_idx}",
                                        type=card_color,
                                        disabled=disabled,
                                        use_container_width=True,
                                        on_click=handle_card_click,
                                        args=(card_idx,)
                                    )
                            else:
                                # For hidden cards, show a question mark
                                st.button(
                                    "❓",
                                    key=f"card_{card_idx}",
                                    type=card_color,
                                    disabled=disabled,
                                    use_container_width=True,
                                    on_click=handle_card_click,
                                    args=(card_idx,)
                                )

if __name__ == "__main__":
    main()