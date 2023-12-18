import pytest
from unittest.mock import patch, MagicMock
from app.api.llm import process_query
from dotenv import load_dotenv
from typing import Any

# Load environment variables
load_dotenv()

def test_process_query_success() -> None:
    """
    Test if process_query successfully returns a response using a mocked agent.
    """
    # Mock the create_agent function and the agent's run method
    with patch('app.api.llm.create_agent') as mock_create_agent:
        mock_agent = MagicMock()
        mock_agent.run.return_value = "mocked response"
        mock_create_agent.return_value = mock_agent

        # Execute the process_query function
        response = process_query("test query", "mocked data")

        # Assertions
        assert response == "mocked response"
        mock_create_agent.assert_called_once_with("mocked data")
        mock_agent.run.assert_called_once_with("test query")

def test_process_query_exception_handling() -> None:
    """
    Test if process_query properly handles exceptions raised by create_agent.
    """
    # Mock create_agent to raise an exception
    with patch('app.api.llm.create_agent', side_effect=Exception("test error")):
        # Execute the process_query function and expect an exception
        with pytest.raises(Exception) as excinfo:
            process_query("test query", "mocked data")
        assert "test error" in str(excinfo.value)
