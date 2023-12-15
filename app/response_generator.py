import json
import uuid

def generate_response(data):
    response_id = str(uuid.uuid4())
    return {"response_id": response_id, "data": data}