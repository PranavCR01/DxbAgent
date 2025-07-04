# outreach/generator.py

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

def generate_template_prompt(city, tone, usp="high ROI"):
    return f"""You are a real estate outreach assistant. Generate a reusable WhatsApp message template.

You are a real estate consultant operating from Bangalore. You are reaching out to potential clients in {city}, inviting them to invest in properties located in Dubai.

Requirements:
- Use a {tone} tone.
- DO NOT include any 'Subject:' line.
- DO NOT include emojis.
- DO NOT include placeholders other than {{name}} and {{city}}.
- DO NOT include '[Your Name]', '[Contact Info]', or signature placeholders.
- Use WhatsApp-friendly formatting with line breaks between thoughts.
- The message should be short, human, and persuasive.
- Focus on this selling point: {usp}
- End with: Would you like more details or a quick call?
- Sign off with: Best regards, Chaitanya J Reddy
"""

def get_or_create_template(city, tone, usp):
    key = f"{city}_{tone}_{usp}"
    if key in template_cache:
        return template_cache[key]

    prompt = generate_template_prompt(city, tone, usp)
    response = client.chat(model='mistral', messages=[
        {"role": "system", "content": "You generate message templates for real estate outreach."},
        {"role": "user", "content": prompt}
    ])
    message = response['message']['content']
    if '{name}' not in message:
        message += "\n{name}"
    if '{city}' not in message:
        message += "\n{city}"
    template_cache[key] = message

    with open(CACHE_FILE, "wb") as f:
        pickle.dump(template_cache, f)

    return message
