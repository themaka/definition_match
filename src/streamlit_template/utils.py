"""Utility functions for the Word Definition Memory Game."""

import pandas as pd
import random
from typing import List, Dict, Tuple, Optional

def load_custom_word_pairs(file_path: str) -> Dict[str, str]:
    """
    Load custom word-definition pairs from a CSV file.
    
    Args:
        file_path: Path to CSV file with 'word' and 'definition' columns
        
    Returns:
        Dictionary mapping words to their definitions
    """
    try:
        df = pd.read_csv(file_path)
        
        # Validate the dataframe has required columns
        required_cols = ['word', 'definition']
        missing_cols = [col for col in required_cols if col not in df.columns]
        
        if missing_cols:
            raise ValueError(f"CSV is missing required columns: {', '.join(missing_cols)}")
        
        # Convert to dictionary
        word_dict = {row['word']: row['definition'] for _, row in df.iterrows()}
        return word_dict
    except Exception as e:
        raise Exception(f"Error loading custom word pairs: {str(e)}")

def create_sample_csv() -> pd.DataFrame:
    """
    Create a sample CSV dataframe with word-definition pairs.
    
    Returns:
        DataFrame with sample word-definition pairs
    """
    data = {
        'word': [
            'Algorithm', 'Bandwidth', 'Cache', 'Database',
            'Atom', 'Biology', 'Chemistry', 'DNA',
            'Allegory', 'Metaphor', 'Protagonist', 'Sonnet'
        ],
        'definition': [
            'A step-by-step procedure for solving a problem or accomplishing a task',
            'The maximum rate of data transfer across a given path',
            'A temporary storage area where frequently accessed data can be stored for rapid access',
            'An organized collection of structured information or data',
            'The basic unit of matter consisting of a nucleus and electrons',
            'The study of living organisms and their interactions with the environment',
            'The study of matter, its properties, and the changes it undergoes',
            'A molecule that carries genetic instructions for development and functioning of organisms',
            'A story with hidden meaning, typically with moral or political significance',
            'A figure of speech making an implicit comparison without using \'like\' or \'as\'',
            'The main character in a story, often in conflict with an antagonist',
            'A 14-line poem with a specific rhyme scheme and structure'
        ],
        'category': [
            'Technology', 'Technology', 'Technology', 'Technology',
            'Science', 'Science', 'Science', 'Science',
            'Literature', 'Literature', 'Literature', 'Literature'
        ]
    }
    
    return pd.DataFrame(data)

def calculate_score(pairs_found: int, total_pairs: int, attempts: int, time_seconds: int) -> int:
    """
    Calculate a score based on game performance.
    
    Args:
        pairs_found: Number of pairs correctly matched
        total_pairs: Total number of pairs in the game
        attempts: Number of attempts made
        time_seconds: Time taken in seconds
        
    Returns:
        Score as an integer from 0-100
    """
    # Perfect score would be finding all pairs in minimum attempts (equal to total_pairs)
    # and in reasonable time
    
    # Calculate completion percentage (50% of score)
    completion_score = (pairs_found / total_pairs) * 50
    
    # Calculate efficiency (attempts compared to minimum possible) (30% of score)
    min_attempts = total_pairs
    max_attempts = total_pairs * 3  # Arbitrary upper bound
    
    efficiency = max(0, 1 - ((attempts - min_attempts) / (max_attempts - min_attempts)))
    efficiency_score = efficiency * 30
    
    # Calculate time factor (20% of score)
    # Assuming 5 seconds per pair is a good target time
    target_time = total_pairs * 5
    max_time = total_pairs * 15  # Arbitrary upper bound
    
    time_factor = max(0, 1 - ((time_seconds - target_time) / (max_time - target_time)))
    time_score = time_factor * 20
    
    # Combine scores
    total_score = int(completion_score + efficiency_score + time_score)
    
    # Ensure score is between 0 and 100
    return max(0, min(100, total_score))

def get_difficulty_settings(difficulty: str) -> Dict:
    """
    Get game settings based on difficulty level.
    
    Args:
        difficulty: Difficulty level (Easy, Medium, Hard)
        
    Returns:
        Dictionary with game settings
    """
    settings = {
        "Easy": {
            "pairs": 4,
            "time_limit": 120,  # 2 minutes
            "reveal_time": 1.0  # seconds to show non-matching cards
        },
        "Medium": {
            "pairs": 6,
            "time_limit": 180,  # 3 minutes
            "reveal_time": 0.8
        },
        "Hard": {
            "pairs": 8,
            "time_limit": 240,  # 4 minutes
            "reveal_time": 0.5
        },
        "Expert": {
            "pairs": 10,
            "time_limit": 300,  # 5 minutes
            "reveal_time": 0.3
        }
    }
    
    return settings.get(difficulty, settings["Easy"])

def split_words_into_categories(word_dict: Dict[str, str], 
                               categories: Optional[List[str]] = None) -> Dict[str, Dict[str, str]]:
    """
    Split a flat dictionary of words into categories.
    
    Args:
        word_dict: Dictionary mapping words to definitions
        categories: Optional list of category names (generates random assignment if None)
        
    Returns:
        Dictionary mapping category names to word-definition dictionaries
    """
    all_words = list(word_dict.keys())
    result = {}
    
    # If no categories provided, create generic ones
    if not categories:
        categories = ["Set 1", "Set 2", "Set 3"]
    
    # Calculate words per category
    words_per_category = max(1, len(all_words) // len(categories))
    
    # Shuffle words for random assignment
    random.shuffle(all_words)
    
    # Assign words to categories
    for i, category in enumerate(categories):
        start_idx = i * words_per_category
        end_idx = start_idx + words_per_category if i < len(categories) - 1 else len(all_words)
        
        category_words = all_words[start_idx:end_idx]
        result[category] = {word: word_dict[word] for word in category_words}
    
    return result