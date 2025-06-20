from flask import Flask, render_template, request, jsonify
import random
import joblib

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

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/classify", methods=["POST"])
def classify():
    data = request.get_json()
    message = data.get("message", "")   
    result = classify_message(message)
    return jsonify({"result": result})

if __name__ == "__main__":
   
    
    app.run(debug=True)