import pytest
from app.data_handler import get_market_data
import pandas as pd
from dotenv import load_dotenv
from pandas.errors import EmptyDataError, ParserError
from pathlib import Path
import os


load_dotenv()

def test_get_market_data_success(tmp_path):
    # Create a temporary CSV file with some test data
    df = pd.DataFrame({'A': [1, 2], 'B': [3, 4]})
    file_path = tmp_path / "test_data.csv"
    df.to_csv(file_path, index=False)

    # Test successful data loading
    result = get_market_data(file_path)
    assert isinstance(result, pd.DataFrame)
    assert not result.empty

def test_get_market_data_file_not_found():
    # Test file not found error handling
    with pytest.raises(FileNotFoundError):
        get_market_data("non_existent_file.csv")

def test_get_market_data_empty_data_error(tmp_path):
    # Create an empty CSV file
    file_path = tmp_path / "empty.csv"
    file_path.touch()

    # Test empty data error handling
    with pytest.raises(ValueError, match="No data: The file is empty."):
        get_market_data(file_path)


def test_get_market_data_csv_parsing_error(tmp_path):
    # Create a malformed CSV file with inconsistent column counts
    file_path = tmp_path / "malformed.csv"
    with open(file_path, 'w') as f:
        f.write("header1,header2\n1,2\n3,4,5")  # Extra column in the last row

    # Test CSV parsing error handling
    with pytest.raises(ValueError, match="Error parsing CSV file."):
        get_market_data(file_path)

