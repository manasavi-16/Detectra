# CHANGE THIS LINE in your main.py:
# model_path = "./distilbert_model" 

# TO THIS (Replace with your actual HF username):
model_path = "Manasavi-7953/detectra-distilbert" 

tokenizer = DistilBertTokenizerFast.from_pretrained(model_path)
model = DistilBertForSequenceClassification.from_pretrained(model_path)