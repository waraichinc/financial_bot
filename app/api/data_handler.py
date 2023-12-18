import pandas as pd
import logging
from typing import Union
from pandas import DataFrame
from pathlib import Path

# Initialize logging
logging.basicConfig(level=logging.INFO)

def get_market_data(path: Union[str, Path]) -> DataFrame:
    """
    Loads market data from a CSV file.

    Args:
        path (Union[str, Path]): The file path to the CSV file containing market data.

    Returns:
        DataFrame: A Pandas DataFrame containing the market data.

    Raises:
        FileNotFoundError: If the specified file does not exist.
        ValueError: If the file is not a CSV or if it cannot be read into a DataFrame.
        Exception: For other unexpected errors.
    """
    try:
        if not Path(path).is_file():
            raise FileNotFoundError(f"File not found at path: {path}")

        data = pd.read_csv(path)
        logging.info("Market data loaded successfully.")
        return data
    except FileNotFoundError as e:
        logging.error(f"File not found error: {e}")
        raise
    except pd.errors.EmptyDataError:
        logging.error("No data: The file is empty.")
        raise ValueError("No data: The file is empty.")
    except pd.errors.ParserError:
        logging.error("Error parsing CSV file.")
        raise ValueError("Error parsing CSV file.")
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        raise