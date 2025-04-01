"""Test fixtures and configuration."""

import pytest
import pandas as pd


@pytest.fixture
def sample_dataframe():
    """Fixture providing a sample dataframe for testing."""
    return pd.DataFrame({"A": [1, 2, 3], "B": [4, 5, 6]})
