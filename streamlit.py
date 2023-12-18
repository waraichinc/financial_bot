import streamlit as st
import requests
import os

# API Configuration
API_URL = os.getenv('API_URL', 'http://fastapi:8000')

st.title('NLP Market Data Query Interface')

# Input for the user to enter their query
user_query = st.text_input("Enter your market data query:")

# Function to send the query to the FastAPI backend
def send_query(query):
    response = requests.post(f"{API_URL}/api/v1/marketdataquery", json={"query": query})
    if response.status_code == 200:
        return response.json()
    else:
        st.error("Error in API response")
        return None

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
    welcome_message = requests.get(f"{API_URL}/")
    if welcome_message.status_code == 200:
        st.write(welcome_message.text)
    else:
        st.error("Failed to get welcome message from API.")

st.markdown(
    """
    ---
    Made by [Jaspreet Singh](https://www.linkedin.com/in/waraichinc/) | [GitHub](https://github.com/waraichinc)
    """,
    unsafe_allow_html=True
)