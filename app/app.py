from flask import Flask, render_template, request, jsonify
import random

app = Flask(__name__)

# Simulación de un modelo de clasificación de spam
def classify_message(text):
    spam_keywords = ["win", "free", "money", "offer", "click"]
    if any(word in text.lower() for word in spam_keywords):
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