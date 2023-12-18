import streamlit as st
import requests
import os
from typing import Optional, Dict, Any

# API Configuration
API_URL = os.getenv('API_URL', 'http://fastapi:8000')

st.title('NLP Market Data Query Interface')

def send_query(query: str) -> Optional[Dict[str, Any]]:
    """
    Send a query to the FastAPI backend and return the response.

    Args:
        query (str): The market data query string entered by the user.

    Returns:
        Optional[Dict[str, Any]]: The response from the API as a dictionary, or None if there's an error.
    """
    try:
        response = requests.post(f"{API_URL}/api/v1/marketdataquery", json={"query": query})
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        st.error(f"Error in API response: {e}")
        return None

def fetch_welcome_message() -> str:
    """
    Fetch and return the welcome message from the API.

    Returns:
        str: The welcome message from the API.
    """
    try:
        response = requests.get(f"{API_URL}/")
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        st.error(f"Failed to get welcome message from API: {e}")
        return "No welcome message available."

# Input for the user to enter their query
user_query = st.text_input("Enter your market data query:")

# Button to send the query
if st.button("Submit Query"):
    if user_query:
        with st.spinner('Processing...'):
            result = send_query(user_query)
            if result:
                st.success("Query processed successfully!")
                st.json(result)  
    else:
        st.error("Please enter a query.")

# Display a welcome message by querying the root endpoint
if st.checkbox("Show API Welcome Message"):
    welcome_message = fetch_welcome_message()
    st.write(welcome_message)

st.markdown(
    """
    ---
    Made by [Jaspreet Singh](https://www.linkedin.com/in/waraichinc/) | [GitHub](https://github.com/waraichinc)
    """,
    unsafe_allow_html=True
)
