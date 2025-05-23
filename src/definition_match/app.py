"""Main Streamlit application for Word Definition Memory Game."""

import streamlit as st
import pandas as pd
import random
import time
from typing import List, Dict, Tuple

# Import custom modules
from custom_features import add_custom_css, apply_matched_card_style, DIFFICULTIES, render_difficulty_selector

# Set page configuration
st.set_page_config(
    page_title="Word Definition Memory Game",
    page_icon="🧠",
    layout="wide"
)

# Apply custom CSS
add_custom_css()

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
if 'just_uploaded_csv' not in st.session_state:
    st.session_state.just_uploaded_csv = False

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
    # Get number of pairs based on difficulty from shared DIFFICULTIES constant
    count = DIFFICULTIES.get(difficulty, DIFFICULTIES["Easy"])["pairs"]
    
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
    # First check if we are showing a non-match already
    # If so, prevent further card selection until the player clicks "Continue"
    if st.session_state.showing_non_match:
        # We don't process any new card clicks when showing non-matched pairs
        # The UI will show a message instructing the player to click "Continue"
        return
    
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
        is_match = (card1_type != card2_type) and (card1_pair == card2_text) and (card2_pair == card1_text)
        
        if is_match:
            # It's a match! Add both cards to matched pairs
            st.session_state.matched_pairs.extend(st.session_state.selected_cards)
            # Clear selected cards
            st.session_state.selected_cards = []
            # Play success sound (could be added in future version)
            # st.session_state.play_success_sound = True
        else:
            # It's not a match - Add a button to flip cards back
            st.session_state.showing_non_match = True

def verify_game_state() -> None:
    """
    Verify and repair game state if inconsistencies are found.
    This helps prevent game-breaking bugs if unexpected interactions occur.
    """
    # Check if selected cards is somehow greater than 2 (which shouldn't happen)
    if hasattr(st.session_state, 'selected_cards') and len(st.session_state.selected_cards) > 2:
        # Reset to a consistent state
        st.session_state.selected_cards = []
        st.session_state.showing_non_match = False
    
    # Ensure showing_non_match is False if we don't have exactly 2 selected cards
    if (hasattr(st.session_state, 'showing_non_match') and 
        hasattr(st.session_state, 'selected_cards') and
        st.session_state.showing_non_match and 
        len(st.session_state.selected_cards) != 2):
        st.session_state.showing_non_match = False

def main() -> None:
    """Main application function."""
    st.title("🧠 Word Definition Memory Game")
    
    # Use a purely client-side approach for showing mobile tips only on small screens
    st.markdown("""
    <div id="mobile-tip" style="display: none;">
        <div style="padding: 1rem; border-radius: 0.5rem; background-color: #cfe2ff; border-left: 4px solid #084298; margin-bottom: 1rem;">
            <span style="font-size: 1.2rem;">ℹ️</span> 
            <strong>Small screen detected</strong>: For the best experience, try landscape mode and tap the '>' at top-left to access settings.
        </div>
    </div>
    
    <script>
        // Only show the mobile tip if screen width is under 600px and we haven't shown it before
        function updateMobileTip() {
            const mobileTip = document.getElementById('mobile-tip');
            if (mobileTip) {
                const isSmallScreen = window.innerWidth < 600;
                const tipAlreadyShown = sessionStorage.getItem('mobile_tip_shown') === 'true';
                
                if (isSmallScreen && !tipAlreadyShown) {
                    mobileTip.style.display = "block";
                    sessionStorage.setItem('mobile_tip_shown', 'true');
                } else {
                    mobileTip.style.display = "none";
                }
            }
        }
        
        // Run immediately
        updateMobileTip();
    </script>
    """, unsafe_allow_html=True)
    
    # Verify game state for consistency
    verify_game_state()
    
    # Sidebar for game controls
    with st.sidebar:
        st.markdown("### Game Settings")
        
        # Group categories to separate built-in from custom categories
        built_in_categories = [cat for cat in WORD_SETS.keys() if not cat.startswith("Custom")]
        custom_categories = [cat for cat in WORD_SETS.keys() if cat.startswith("Custom")]
        
        # If we have custom categories, show them in an organized dropdown
        if custom_categories:
            all_categories = built_in_categories + ["---"] + custom_categories
            selected_index = 0  # Default to first built-in category
            
            # If this is right after a CSV upload, default to the first custom category
            if 'just_uploaded_csv' in st.session_state and st.session_state.just_uploaded_csv:
                selected_index = len(built_in_categories) + 1  # +1 for the separator
                st.session_state.just_uploaded_csv = False
            
            # Create an organized category selection dropdown
            category_option = st.selectbox(
                "Category", 
                options=all_categories,
                index=selected_index,
                format_func=lambda x: "──────────" if x == "---" else x
            )
            
            # Handle the separator option
            if category_option == "---":
                # If they select the separator, default to the first custom category if available
                if custom_categories:
                    category = custom_categories[0]
                else:
                    category = built_in_categories[0]
            else:
                category = category_option
        else:
            # Simple selection for built-in categories only
            category = st.selectbox(
                "Category", 
                options=built_in_categories,
                index=0
            )
        
        # Use our new compact difficulty selector
        selected_difficulty = render_difficulty_selector()
        
        # Start game button - make it more prominent but compact
        if st.button("🎮 Start New Game", type="primary", use_container_width=True):
            start_game(category, selected_difficulty)
        
        # Show instructions in a compact expander
        with st.expander("How to Play"):
            st.markdown("""
            - Click cards to flip them over
            - Match each word with its definition
            - Game completes when all pairs are matched
            - Fewer attempts = better score
            """)
        
        # Display stats during active game in a more compact form
        if st.session_state.game_active:
            st.markdown("---")
            st.markdown("### Game Stats")
            
            # Calculate completion percentage
            total_pairs = len(st.session_state.all_cards) // 2
            matched_count = len(st.session_state.matched_pairs) // 2
            completion = (matched_count / total_pairs) * 100
            
            # More compact stats display
            cols = st.columns(2)
            
            with cols[0]:
                st.metric("Progress", f"{matched_count}/{total_pairs}")
            
            with cols[1]:
                st.metric("Attempts", st.session_state.attempts)
            
            # Progress bar doesn't need a label
            st.progress(completion / 100)
            
            # Display timer if game is in progress
            if st.session_state.start_time and matched_count < total_pairs:
                elapsed = int(time.time() - st.session_state.start_time)
                minutes, seconds = divmod(elapsed, 60)
                st.metric("Time", f"{minutes:02d}:{seconds:02d}")
    
    # Initialize the showing_non_match state variable if it doesn't exist
    if 'showing_non_match' not in st.session_state:
        st.session_state.showing_non_match = False
    
    # Main game area
    if not st.session_state.game_active:
        # Welcome screen design - more compact
        st.header("Word Definition Memory Game")
        st.write("Select a category and difficulty in the sidebar, then click 'Start New Game'.")
        
        # Use tabs for sample words and custom upload to save vertical space
        tab1, tab2 = st.tabs(["Sample Categories", "Upload Custom Words"])
        
        with tab1:
            # Display sample words from each category in a more compact layout
            for cat_name, word_dict in WORD_SETS.items():
                # Skip custom categories in the samples tab
                if "Custom" in cat_name:
                    continue
                    
                with st.expander(f"{cat_name}"):
                    sample_words = list(word_dict.keys())[:3]
                    for word in sample_words:
                        st.markdown(f"**{word}**: {word_dict[word]}")
        
        with tab2:
            # Add file uploader for custom words
            uploaded_file = st.file_uploader("Choose a CSV file with words and definitions", type="csv")
            
            # Add CSV format helper information
            with st.expander("CSV File Format"):
                st.markdown("""
                Your CSV file needs these columns:
                - **word**: The term to match
                - **definition**: The meaning
                - **category**: (Optional) For grouping terms
                
                **Example:**
                ```
                word,definition,category
                Algorithm,Step-by-step procedure,Computer Science
                Photosynthesis,Process using sunlight,Biology
                ```
                """)
                
                # Add a download link for a sample CSV template
                sample_csv = """word,definition,category
Algorithm,Step-by-step procedure for calculations or problem-solving,Computer Science
Photosynthesis,Process by which plants use sunlight to create energy,Biology
Metaphor,Figure of speech that makes an implicit comparison,Literature
Velocity,Rate of change of position with respect to time,Physics
Database,Organized collection of structured information,Computer Science
"""
                
                st.download_button(
                    label="Download Template",
                    data=sample_csv,
                    file_name="custom_words_template.csv",
                    mime="text/csv"
                )
            
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
                                WORD_SETS[f"Custom: {category_name}"] = word_dict
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
            
            # Get difficulty info for the current difficulty including emoji
            current_category = category
            current_difficulty = st.session_state.difficulty
            difficulty_info = DIFFICULTIES.get(current_difficulty, DIFFICULTIES["Easy"])
            difficulty_emoji = difficulty_info["icon"]
            
            # Format the category name nicely
            category_display = current_category
            
            # Add a category emoji based on the category type
            category_emoji = "📚" # Default
            if "Technology" in current_category:
                category_emoji = "💻"
            elif "Science" in current_category:
                category_emoji = "🔬"
            elif "Literature" in current_category:
                category_emoji = "📖"
            elif "Custom" in current_category:
                category_emoji = "✨"
            
            # Single, clearer play again button with category and difficulty info
            if st.button(f"🎮 Play Again with {category_emoji} {category_display} ({current_difficulty} {difficulty_emoji})", 
                         type="primary", use_container_width=True):
                # Start a new game with these settings
                start_game(current_category, current_difficulty)
                
                # Force a rerun to immediately update the UI with the new game
                st.rerun()
            
            # Add a reminder about the sidebar for changing settings
            st.info("💡 You can change the category or difficulty in the sidebar before starting a new game.")
        else:
            # Active game - display the card grid
            # Determine grid layout based on screen width using a placeholder
            layout_check = st.empty()
            layout_check.markdown("""
            <script>
                // Get screen width and set a session storage item
                const screenWidth = window.innerWidth;
                sessionStorage.setItem('screen_width', screenWidth);
                
                // Update a hidden element with the screen info
                const infoElement = document.createElement('div');
                infoElement.id = 'screen-info';
                infoElement.style.display = 'none';
                infoElement.innerText = screenWidth.toString();
                document.body.appendChild(infoElement);
            </script>
            """, unsafe_allow_html=True)
            
            # Determine grid layout based on number of cards and screen size
            # Default to 4 columns, but we'll reduce for smaller screens
            cols_per_row = 4
            num_cards = len(st.session_state.all_cards)
            
            # Small screens get fewer columns based on card count
            # These values would ideally be determined by actual screen width
            # but for now we'll base it on card count as a simple adaptive approach
            if num_cards <= 8:
                cols_per_row = 4  # 2x2 grid for 4 pairs
            elif num_cards <= 12:
                cols_per_row = 3  # 4x3 grid for 6 pairs 
            else:
                cols_per_row = 4  # 4x4 grid for 8 pairs
            
            # Add a CSS class to help with responsive sizing
            card_count_class = f"card-count-{num_cards}"
            
            # Create rows of cards with responsive layout
            for row_idx in range(0, num_cards, cols_per_row):
                cols = st.columns(cols_per_row)
                
                for i in range(cols_per_row):
                    card_idx = row_idx + i
                    if card_idx < num_cards:
                        card_type, card_text, pair_text = st.session_state.all_cards[card_idx]
                        card_key = f"{card_idx}:{card_text}"
                        
                        # Determine card state
                        if card_key in st.session_state.matched_pairs:
                            # Matched card - show with special styling
                            with cols[i]:
                                # Use custom HTML/CSS for matched cards with improved accessibility
                                card_html = f"""
                                <div class="matched-card-container">
                                    <button class="matched-card" 
                                        style="width: 100%; height: 120px; {'font-size: 1.2rem; font-weight: bold;' if card_type == 'word' else 'font-size: 0.9rem;'}" 
                                        disabled 
                                        aria-label="Matched {'word' if card_type == 'word' else 'definition'}: {card_text}" 
                                        role="button">
                                        {card_text}
                                        <span class="visually-hidden">(Matched)</span>
                                    </button>
                                </div>
                                """
                                st.markdown(card_html, unsafe_allow_html=True)
                        elif card_key in st.session_state.selected_cards:
                            # Selected card - show content
                            card_color = "secondary"
                            with cols[i]:
                                if card_type == "word":
                                    # Words get a header style
                                    st.button(
                                        f"## {card_text}",
                                        key=f"card_{card_idx}",
                                        type=card_color,
                                        disabled=True,
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
                                        disabled=True,
                                        use_container_width=True,
                                        on_click=handle_card_click,
                                        args=(card_idx,)
                                    )
                        else:
                            # Unselected card - show back
                            card_color = "secondary"
                            # For hidden cards, show a question mark
                            with cols[i]:
                                # Disable all unselected cards if we're showing a non-match
                                is_disabled = st.session_state.showing_non_match
                                
                                # Add a tooltip if cards are disabled due to non-match state
                                tooltip = None
                                if is_disabled:
                                    tooltip = "Click 'Continue' before selecting more cards"
                                
                                st.button(
                                    "❓",
                                    key=f"card_{card_idx}",
                                    type=card_color,
                                    disabled=is_disabled,
                                    use_container_width=True,
                                    on_click=handle_card_click,
                                    args=(card_idx,),
                                    help=tooltip
                                )
            
            # If we're showing a non-match, display a "Continue" button
            if st.session_state.showing_non_match and len(st.session_state.selected_cards) == 2:
                # Create a colored info box with more prominent message
                st.markdown("""
                <div style="background-color: #e9f5fe; color: #084298; padding: 15px; border-radius: 5px; 
                border-left: 5px solid #084298; margin: 10px 0;">
                    <h3 style="margin-top: 0;">These cards don't match</h3>
                    <p>You need to click "Continue" before selecting more cards.</p>
                </div>
                """, unsafe_allow_html=True)
                
                if st.button("Continue", type="primary"):
                    st.session_state.selected_cards = []
                    st.session_state.showing_non_match = False
                    st.rerun()

if __name__ == "__main__":
    main()