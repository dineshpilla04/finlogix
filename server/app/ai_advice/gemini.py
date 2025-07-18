import os
import requests

def get_budget_advice(prompt):
    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent"
    headers = {"Content-Type": "application/json"}
    payload = {
        "contents": [{"parts": [{"text": prompt}]}]
    }
    params = {"key": os.getenv("GEMINI_API_KEY")}
    response = requests.post(url, headers=headers, json=payload, params=params)
    return response.json()
