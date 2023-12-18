import os
import pandas as pd
from fastapi.testclient import TestClient
from unittest.mock import patch
from dotenv import load_dotenv
from app.main import app

# Load environment variables from .env file
load_dotenv()

client = TestClient(app)

def test_welcome():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == "Hello! Welcome to the NLP Market Data Query API"

@patch('app.llm.process_query')
@patch('app.data_handler.get_market_data')
def test_market_data_query_success(mock_get_market_data, mock_process_query):
    # Create mock data as a DataFrame
    mock_data = pd.DataFrame({
        "Date": ["2023-05-30"],
        "Symbol": ["AAPL"],
        "Volume": [55964401],
        "Open": [176.57],
        "High": [178.99],
        "Low": [176.96],
        "Close": [177.3],
        "Adj Close": [177.3]
    })

    # Mock get_market_data to return the DataFrame
    mock_get_market_data.return_value = mock_data

    # Mock the process_query function to return a predetermined response
    mock_response = "The volume for AAPL on 30th May 2023 is 55964401."
    mock_process_query.return_value = mock_response

    test_query = "What is the volume for AAPL on 30th May 2023?"
    response = client.post("/api/v1/marketdataquery", json={"query": test_query})
    assert response.status_code == 200
    response_data = response.json()
    assert "response_id" in response_data
    assert response_data["response"] == mock_response

def test_market_data_query_validation_error():
    response = client.post("/api/v1/marketdataquery", json={"invalid_key": "value"})
    assert response.status_code == 422

@patch('app.data_handler.get_market_data')
@patch('app.llm.process_query')
def test_market_data_query_internal_server_error(mock_process_query, mock_get_market_data):
    mock_get_market_data.side_effect = Exception("Internal error")

    response = client.post("/api/v1/marketdataquery", json={"query": "test query"})
    assert response.status_code == 500
    assert response.json() == {"detail": "Internal Server Error"}
