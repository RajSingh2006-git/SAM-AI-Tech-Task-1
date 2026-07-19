"""
app.py — Flask backend for the Mail Spam Detector web application.

Loads pre-trained model & vectorizer and exposes a /predict endpoint.
"""

import os
import pickle
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# ── Load model artifacts ──────────────────────────────────────────
MODEL_PATH = os.path.join(os.path.dirname(__file__), "model.pkl")
VECTORIZER_PATH = os.path.join(os.path.dirname(__file__), "vectorizer.pkl")


def load_artifacts():
    """Load the trained model and TF-IDF vectorizer from disk."""
    if not os.path.exists(MODEL_PATH) or not os.path.exists(VECTORIZER_PATH):
        raise FileNotFoundError(
            "model.pkl or vectorizer.pkl not found. "
            "Run `python train_model.py` first."
        )
    with open(MODEL_PATH, "rb") as f:
        model = pickle.load(f)
    with open(VECTORIZER_PATH, "rb") as f:
        vectorizer = pickle.load(f)
    return model, vectorizer


model, vectorizer = load_artifacts()


# ── Routes ────────────────────────────────────────────────────────
@app.route("/")
def home():
    """Serve the main UI page."""
    return render_template("index.html")


@app.route("/predict", methods=["POST"])
def predict():
    """
    Accept a JSON payload { "message": "..." } and return
    { "prediction": "Ham" | "Spam", "confidence": float }.
    """
    data = request.get_json(force=True)
    message = data.get("message", "").strip()

    if not message:
        return jsonify({"error": "Please enter a message."}), 400

    # Transform the input through the same TF-IDF pipeline
    features = vectorizer.transform([message])

    # Predict
    prediction = model.predict(features)[0]
    confidence = model.predict_proba(features).max() * 100

    result = "Ham" if int(prediction) == 1 else "Spam"
    return jsonify({"prediction": result, "confidence": round(confidence, 2)})


# ──────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    app.run(debug=True, port=5000)
