from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import torch
# These imports fix the "NameError" you encountered
from transformers import DistilBertTokenizerFast, DistilBertForSequenceClassification
from deep_translator import GoogleTranslator

app = FastAPI()

# 1. Load Model from Hugging Face
# REPLACE 'Manasavi-7953/detectra-distilbert' with your actual Hugging Face path
model_path = "Manasavi-7953/detectra-distilbert" 

try:
    tokenizer = DistilBertTokenizerFast.from_pretrained(model_path)
    model = DistilBertForSequenceClassification.from_pretrained(model_path)
    model.eval()
except Exception as e:
    print(f"Error loading model: {e}")

class MessageInput(BaseModel):
    text: str

def translate_to_english(text):
    try:
        # Translates Indian regional languages to English
        return GoogleTranslator(source='auto', target='en').translate(text)
    except:
        return text

@app.post("/detect")
async def detect_scam(input_data: MessageInput):
    # Process the text
    translated_text = translate_to_english(input_data.text)
    
    # Tokenize for DistilBERT
    inputs = tokenizer(
        translated_text, 
        return_tensors="pt", 
        truncation=True, 
        padding=True, 
        max_length=128
    )
    
    # AI Prediction
    with torch.no_grad():
        outputs = model(**inputs)
        prob = torch.softmax(outputs.logits, dim=1)[0][1].item()

    # Your "Professional" Intent Boosting Logic
    text_lower = translated_text.lower()
    intent_keywords = [
        "send otp", "share otp", "click link", 
        "update kyc", "account blocked", "urgent action"
    ]
    
    if any(word in text_lower for word in intent_keywords):
        prob = min(prob + 0.2, 1.0)

    verdict = "SCAM" if prob > 0.5 else "GENUINE"
    
    return {
        "verdict": verdict,
        "probability": round(prob * 100, 2),
        "translated_text": translated_text
    }

# Render requires the app to run on a specific port
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=10000)
