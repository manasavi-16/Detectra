import requests
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# REPLACE these with your actual details
HF_TOKEN = "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" 
MODEL_ID = "Manasavi-7953/detectra-distilbert" 
API_URL = f"https://api-inference.huggingface.co/models/{MODEL_ID}"

class MessageInput(BaseModel):
    text: str

@app.post("/detect")
async def detect_scam(input_data: MessageInput):
    headers = {"Authorization": f"Bearer {HF_TOKEN}"}
    response = requests.post(API_URL, headers=headers, json={"inputs": input_data.text})
    
    # Hugging Face returns a list of scores
    result = response.json()
    
    # Logic to pick the highest score (Scam vs Genuine)
    # This keeps your REAL model at the center of the app
    return result 

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=10000)
