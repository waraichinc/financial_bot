import os
from langchain.agents.agent_types import AgentType
from langchain.chat_models import ChatOpenAI
from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent
from typing import Any

# Load API key from environment variable
API_KEY = os.getenv('API_KEY')

def create_agent(data: Any) -> Any:
    """
    Creates a Pandas DataFrame agent using the specified data.

    Args:
        data (Any): The data to be used by the agent.

    Returns:
        Any: An agent configured with the provided data.
    """
    agent = create_pandas_dataframe_agent(
        ChatOpenAI(temperature=0, model="gpt-4", api_key=API_KEY),
        data,
        agent_type=AgentType.OPENAI_FUNCTIONS,
    )
    return agent

def process_query(query: str, data: Any) -> Any:
    """
    Processes a query using an agent created with the given data.

    Args:
        query (str): The query to be processed.
        data (Any): The data to be used for creating the agent.

    Returns:
        Any: The response from the agent.
    """
    try:
        agent = create_agent(data)
        response = agent.run(query)
        return response
    except Exception as e:
        # Implement appropriate error handling
        raise Exception(f"Error processing query: {e}")
