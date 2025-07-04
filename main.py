from fastapi import FastAPI
from pydantic import BaseModel
from db import init_db, get_user_profile, save_user_profile

import os
import openai
from dotenv import load_dotenv
from pydantic import BaseModel

app = FastAPI()
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

init_db()  # Run this on app startup

@app.get("/")
def read_root():
    return {"message": "GHG chatbot is running."}

@app.get("/profile/{user_id}")
def read_profile(user_id: str):
    profile = get_user_profile(user_id)
    if not profile:
        return {"message": "User not found."}
    return profile

class ProfileInput(BaseModel):
    home_postcode: str
    office_postcode: str
    car_type: str
    engine_size: str
    fuel_type: str
    heating_type: str

@app.post("/profile/{user_id}")
def save_profile(user_id: str, input: ProfileInput):
    data = input.dict()
    data["setup_complete"] = True
    save_user_profile(user_id, data)
    return {"message": f"Profile for {user_id} saved."}


class MessageInput(BaseModel):
    user_id: str
    message: str

@app.post("/message")
def handle_message(input: MessageInput):
    profile = get_user_profile(input.user_id)
    if not profile:
        profile = {}


    # Build GPT prompt
    profile_lines = []

    if profile.get("home_postcode"):
        profile_lines.append(f"The user's home postcode is {profile['home_postcode']}.")
    if profile.get("office_postcode"):
        profile_lines.append(f"Their office postcode is {profile['office_postcode']}.")
    if profile.get("car_type"):
        profile_lines.append(f"They drive a {profile['car_type']} with a {profile.get('engine_size', '')} engine on {profile.get('fuel_type', '')}.")
    if profile.get("heating_type"):
        profile_lines.append(f"Their home uses {profile['heating_type']} for heating.")

    context = " ".join(profile_lines) or "The user has not provided any profile data yet."

    prompt = (
        f"{context}\n\n"
        f"The user says: \"{input.message}\"\n\n"
        "Estimate GHG emissions in kgCO₂e based on the message. "
        "If essential info is missing, ask the user a clarifying question. "
        "If they provide new facts like postcode or heating type, you may infer and suggest saving it for later."
    )


    # Send to GPT
    response = openai.ChatCompletion.create(
    model="gpt-4",
    messages=[
        {"role": "system", "content": "You are a GHG emissions calculator assistant. Be concise and helpful."},
        {"role": "user", "content": prompt}
    ]
)

    reply = response["choices"][0]["message"]["content"]
    return {"reply": reply}

# Optional: if GPT extracts new structured facts, update profile
def maybe_enrich_profile(message, user_id):
    if "my home is at" in message or "I live in" in message:
        # crude postcode grabber
        import re
        match = re.search(r"(EH\d+\s?\d?[A-Z]{2}?)", message, re.IGNORECASE)
        if match:
            postcode = match.group(1).strip()
            existing = get_user_profile(user_id) or {}
            existing["home_postcode"] = postcode
            save_user_profile(user_id, existing)

    # More logic could go here, e.g. checking for "we use oil heating"

# Call this inside /message
maybe_enrich_profile(input.message, input.user_id)
