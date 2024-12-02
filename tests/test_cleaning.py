import sys

from dotenv import find_dotenv, dotenv_values
import pandas as pd
import pytest

sys.path.append("./")
from src.make_data import clean_and_normalize_movie_title


@pytest.fixture(scope="session", autouse=True)
def load_env():
    """Load the .env file before running tests."""
    config = dotenv_values(find_dotenv(".env"))
    return config


def load_test_movie_data():
    return pd.read_csv(config["data_path_cleaned"]) 


# test titles individually
@pytest.mark.parametrize("input_title, expected_output", [
    (" Inception", "inception"),  # Leading spaces
    ("Inception ", "inception"),  # Trailing spaces
    (" Inception ", "inception"),  # Leading/Trailing spaces
    ("The   Dark   Knight", "the dark knight"),  # Multiple spaces
    ("Pulp Fiction!", "pulp fiction!"),  # Valid punctuation
    ("Shrek 2", "shrek 2"),  # Numbers preserved
    ("Lord of the Rings: The Two Towers", "lord of the rings the two towers"),  # Colon removed (franchise should be captured later)
    ("  A Beautiful Mind ", "a beautiful mind"),  # Combination of trim and normalization
    ("Spider-Man", "spider-man")  # Dash preserved
])
def test_clean_and_normalize_movie_title(input_title, expected_output):
    """comments about what to expect inline"""
    assert clean_and_normalize_movie_title(input_title) == expected_output

def test_empty_string():
    """Test handling of an empty string"""
    assert clean_and_normalize_movie_title("") == ""

def test_only_special_characters():
    """Test handling of a string with only invalid characters"""
    assert clean_and_normalize_movie_title("@#$") == ""
