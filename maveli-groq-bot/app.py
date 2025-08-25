from flask import Flask, request, jsonify, render_template
import requests
import os
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"
MODEL = "llama3-8b-8192"

MAVELI_PROMPT = """
You are Maveli Raja (മഹാബലി രാജാവ്), the legendary king of Kerala.
Speak only in Malayalam. Your replies should be filled with cultural wisdom, Onam stories, kindness,
and a bit of humor. Begin each reply with “മാവേലി:”
"""

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message")

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": MAVELI_PROMPT},
            {"role": "user", "content": user_message}
        ]
    }

    response = requests.post(GROQ_URL, headers=headers, json=payload)
    reply = response.json()["choices"][0]["message"]["content"]
    return jsonify({"reply": reply})
