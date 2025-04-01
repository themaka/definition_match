"""Main Streamlit application module."""

import streamlit as st
import pandas as pd

from streamlit_template.utils import get_sample_data, process_data


def main() -> None:
    """Main Streamlit application entry point."""
    st.set_page_config(page_title="Streamlit Template", page_icon="📊", layout="wide")

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
