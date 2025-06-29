from flask import Flask, render_template, request, jsonify
import random
import joblib
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification

model_name = "Goodmotion/spam-mail-classifier"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(model_name)

app = Flask(__name__)

import os
model_filename = os.path.join(os.path.dirname(__file__), 'notebooks/spam_detection_model.joblib')
#model_filename = 'notebooks/spam_detection_model.joblib'
loaded_model = joblib.load(model_filename)
# Simulación de un modelo de clasificación de spam
def classify_message(text):
    #spam_keywords = ["win", "free", "money", "offer", "click"]
    predictions = loaded_model.predict([text])
    if predictions[0] == 1:
        return "Spam"
    else:
        return "Not Spam"

def classify_message_with_deep(text):
    inputs = tokenizer(text, padding=True, truncation=True, max_length=128, return_tensors="pt")
    with torch.no_grad(): 
        outputs = model(**inputs)
    logits = outputs.logits
    probabilities = torch.softmax(logits, dim=1)
    labels = ["Not Spam", "Spam"]
    results = [
        {"text": text, "label": labels[torch.argmax(prob).item()], "confidence": prob.max().item()}
        for text, prob in zip(text, probabilities)
    ]
    if results[0]['label'] == "Spam":
        return "Spam"
    else:
        return "Not Spam"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/classify", methods=["POST"])
def classify():
    data = request.get_json()
    message = data.get("message", "")   
    #result = classify_message(message)
    result = classify_message_with_deep(message)
    return jsonify({"result": result})

if __name__ == "__main__":
    app.run(debug=False)