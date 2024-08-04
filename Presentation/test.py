from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

class InputData(BaseModel):
    input_value: str

@app.get("/get-data/")
async def get_data(input_value: str):
    return {"result": process_data(input_value)}

def process_data(input_value):
    # Placeholder function to process the input
    return f"Processed GET input: {input_value}"