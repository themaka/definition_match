#!/bin/bash

# Create app.py
cat > src/streamlit_template/app.py << 'EOF'
"""Main Streamlit application module."""
from typing import Optional
import streamlit as st
import pandas as pd

from streamlit_template.utils import get_sample_data, process_data


def main() -> None:
    """Main Streamlit application entry point."""
    st.set_page_config(
        page_title="Streamlit Template",
        page_icon="📊",
        layout="wide"
    )

    st.title("Streamlit Template App")
    st.write("Welcome to your new Streamlit app!")

    # Create two columns for layout
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Sample Data")
        # Get and display sample data
        data = get_sample_data()
        st.dataframe(data, use_container_width=True)

    with col2:
        st.subheader("Processed Data")
        # Process and display the data
        processed_data = process_data(data)
        st.dataframe(processed_data, use_container_width=True)

    # Add some interactive elements
    if st.button("Show Statistics"):
        st.subheader("Data Statistics")
        st.write(processed_data.describe())

    # Add a file uploader for custom data
    st.subheader("Upload Your Own Data")
    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
    if uploaded_file is not None:
        try:
            user_data = pd.read_csv(uploaded_file)
            st.write("Your uploaded data:")
            st.dataframe(user_data)
            processed_user_data = process_data(user_data)
            st.write("Processed version of your data:")
            st.dataframe(processed_user_data)
        except Exception as e:
            st.error(f"Error processing file: {str(e)}")


if __name__ == "__main__":
    main()
EOF

# Create utils.py
cat > src/streamlit_template/utils.py << 'EOF'
"""Utility functions for data processing and analysis."""
from typing import Optional
import pandas as pd
import numpy as np


def get_sample_data(rows: int = 10) -> pd.DataFrame:
    """Generate sample data for demonstration.

    Args:
        rows: Number of rows to generate, defaults to 10

    Returns:
        DataFrame with sample data including random numbers and dates
    """
    np.random.seed(42)  # For reproducibility

    return pd.DataFrame({
        'date': pd.date_range(start='2024-01-01', periods=rows),
        'value_a': np.random.randn(rows),
        'value_b': np.random.randn(rows),
        'category': np.random.choice(['A', 'B', 'C'], size=rows)
    })


def process_data(df: pd.DataFrame) -> pd.DataFrame:
    """Process input dataframe by adding computed columns.

    Args:
        df: Input DataFrame that should contain 'value_a' and 'value_b' columns

    Returns:
        DataFrame with additional computed columns
    """
    # Create a copy to avoid modifying the input
    processed = df.copy()

    # Add some computed columns if the required columns exist
    if 'value_a' in processed.columns and 'value_b' in processed.columns:
        processed['sum'] = processed['value_a'] + processed['value_b']
        processed['mean'] = (processed['value_a'] + processed['value_b']) / 2
        processed['abs_diff'] = abs(processed['value_a'] - processed['value_b'])

    return processed


def validate_dataframe(
    df: pd.DataFrame,
    required_columns: Optional[list[str]] = None
) -> bool:
    """Validate that a DataFrame meets the required schema.

    Args:
        df: DataFrame to validate
        required_columns: List of column names that must be present

    Returns:
        True if validation passes, raises ValueError otherwise
    """
    if required_columns is None:
        required_columns = ['value_a', 'value_b']

    missing_cols = [col for col in required_columns if col not in df.columns]
    if missing_cols:
        raise ValueError(
            f"DataFrame is missing required columns: {', '.join(missing_cols)}"
        )

    return True
EOF
