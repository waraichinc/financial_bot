import uvicorn
import uuid
import os
import logging
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, ValidationError
from typing import Dict, Any, Callable
from app.api.data_handler import get_market_data
from app.api.llm import process_query

# Initialize logging
logging.basicConfig(level=logging.INFO)

# Configuration
DATA_FILE_PATH: str = os.getenv('DATA_FILE_PATH')
HOST: str = os.getenv('HOST')
PORT: int = os.getenv('PORT')

app = FastAPI()

class Query(BaseModel):
    query: str

@app.get("/", response_model=str, status_code=200)
def welcome() -> str:
    """
    Root endpoint that returns a welcome message.

    Returns:
        str: A welcome message.
    """
    return "Hello! Welcome to the NLP Market Data Query API"

@app.post("/api/v1/marketdataquery", response_model=Dict[str, Any], status_code=200)
def market_data_query(query: Query) -> Dict[str, Any]:
    """
    Endpoint for processing market data queries.

    Args:
        query (Query): The market data query.

    Returns:
        Dict[str, Any]: A dictionary containing the response ID and the processed answer.

    Raises:
        HTTPException: For any exceptions that occur during processing.
    """
    try:
        data = get_market_data(DATA_FILE_PATH)
        answer = process_query(query.query, data)
        response_id = str(uuid.uuid4())
        return {"response_id": response_id, "response": answer}
    except ValidationError as e:
        logging.error(f"Validation error in market_data_query: {e}")
        raise HTTPException(status_code=422, detail="Invalid input data")
    except Exception as e:
        logging.error(f"Error in market_data_query: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

if __name__ == "__main__":
    uvicorn.run(app, host=HOST, port=PORT)