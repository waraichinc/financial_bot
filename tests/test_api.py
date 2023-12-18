import os
import pandas as pd
from fastapi.testclient import TestClient
from unittest.mock import patch
from dotenv import load_dotenv
from app.api.main import app
from fastapi import HTTPException
from pandas import DataFrame

# Load environment variables from .env file
load_dotenv()

client = TestClient(app)

def test_welcome() -> None:
    """
    Test the welcome endpoint to ensure it returns the correct response.
    """
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == "Hello! Welcome to the NLP Market Data Query API"

# @patch('app.api.llm.process_query')
# @patch('app.api.data_handler.get_market_data')
# def test_market_data_query_success(mock_get_market_data: patch, mock_process_query: patch) -> None:
#     """
#     Test the market data query endpoint for successful query processing.

#     Args:
#         mock_get_market_data (patch): Mock for the get_market_data function.
#         mock_process_query (patch): Mock for the process_query function.
#     """
#     # Create mock data as a DataFrame
#     mock_data: DataFrame = pd.DataFrame({
#         "Date": ["2023-05-30"],
#         "Symbol": ["AAPL"],
#         "Volume": [55964401],
#         "Open": [176.57],
#         "High": [178.99],
#         "Low": [176.96],
#         "Close": [177.3],
#         "Adj Close": [177.3]
#     })

#     # Mock get_market_data to return the DataFrame
#     mock_get_market_data.return_value = mock_data

#     # Mock the process_query function to return a predetermined response
#     mock_response: str = "The volume for AAPL on 30th May 2023 is 55964401."
#     mock_process_query.return_value = mock_response

#     test_query: str = "What is the volume for AAPL on 30th May 2023?"
#     response = client.post("/api/v1/marketdataquery", json={"query": test_query})
#     assert response.status_code == 200
#     response_data = response.json()
#     assert "response_id" in response_data
#     assert response_data["response"] == mock_response

def test_market_data_query_validation_error() -> None:
    """
    Test the market data query endpoint to handle validation errors.
    """
    response = client.post("/api/v1/marketdataquery", json={"invalid_key": "value"})
    assert response.status_code == 422

@patch('app.api.data_handler.get_market_data')
@patch('app.api.llm.process_query')
def test_market_data_query_internal_server_error(mock_process_query: patch, mock_get_market_data: patch) -> None:
    """
    Test the market data query endpoint to handle internal server errors.

    Args:
        mock_process_query (patch): Mock for the process_query function.
        mock_get_market_data (patch): Mock for the get_market_data function.
    """
    mock_get_market_data.side_effect = Exception("Internal error")

    response = client.post("/api/v1/marketdataquery", json={"query": "test query"})
    assert response.status_code == 500
    assert response.json() == {"detail": "Internal Server Error"}
