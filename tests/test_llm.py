import pytest
from unittest.mock import patch, MagicMock
from app.llm import process_query
from dotenv import load_dotenv

load_dotenv()

def test_process_query_success():
    # Mock the create_agent function and the agent's run method
    with patch('app.llm.create_agent') as mock_create_agent:
        mock_agent = MagicMock()
        mock_agent.run.return_value = "mocked response"
        mock_create_agent.return_value = mock_agent

        # Execute the process_query function
        response = process_query("test query", "mocked data")

        # Assertions
        assert response == "mocked response"
        mock_create_agent.assert_called_once_with("mocked data")
        mock_agent.run.assert_called_once_with("test query")

def test_process_query_exception_handling():
    # Mock create_agent to raise an exception
    with patch('app.llm.create_agent', side_effect=Exception("test error")):
        with pytest.raises(Exception) as excinfo:
            process_query("test query", "mocked data")
        assert "test error" in str(excinfo.value)
