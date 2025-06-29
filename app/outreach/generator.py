## outreach/ generator.py

import os
import pickle
from ollama import Client

client = Client(host='http://localhost:11434')
CACHE_FILE = "template_cache.pkl"

# Load template cache from disk (if exists)
if os.path.exists(CACHE_FILE):
    with open(CACHE_FILE, "rb") as f:
        template_cache = pickle.load(f)
else:
    template_cache = {}

def generate_template_prompt(city, tone, channel="WhatsApp"):
    return f"""You are a real estate outreach assistant. Generate a reusable message template for WhatsApp outreach.

The message should target potential clients from {city} in a {tone} tone.

Avoid sounding like spam. Make the message concise, trustworthy, and persuasive. Focus on one selling point like high ROI, developer tie-ups, or no property tax.

Use placeholders like {{name}} and {{city}} so we can personalize later.
"""

def get_or_create_template(city, tone):
    key = f"{city}_{tone}"
    if key in template_cache:
        return template_cache[key]

    prompt = generate_template_prompt(city, tone)
    response = client.chat(model='mistral', messages=[
        {"role": "system", "content": "You generate message templates for real estate outreach."},
        {"role": "user", "content": prompt}
    ])
    message = response['message']['content']
    template_cache[key] = message

    # Save updated cache to disk
    with open(CACHE_FILE, "wb") as f:
        pickle.dump(template_cache, f)

    return message


