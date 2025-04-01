"""Test cases for utility functions."""

import pandas as pd

from streamlit_template.utils import get_data, process_data


def test_get_data():
    """Test that get_data returns a properly structured dataframe."""
    data = get_data()
    assert isinstance(data, pd.DataFrame)
    assert data.shape[1] == 2
    assert all(col in data.columns for col in ["A", "B"])


def test_process_data(sample_dataframe):
    """Test that process_data correctly adds computed columns."""
    result = process_data(sample_dataframe)
    assert "C" in result.columns
    assert all(result["C"] == sample_dataframe["A"] + sample_dataframe["B"])
