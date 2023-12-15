from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn
from data_handler import get_market_data
from llm import process_query
from response_generator import generate_response

app = FastAPI()

class Query(BaseModel):
    query:str

@app.post("/api/v1/marketdataquery")
async def market_data_query(query: Query):
    try:
        query_terms = process_query(query.query)
        data = get_market_data(query_terms)
        response = generate_response(data)
        return response 
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__=="__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)