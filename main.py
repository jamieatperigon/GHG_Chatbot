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
    if not profile or not profile.get("setup_complete"):
        return {"reply": "You need to complete your profile setup first."}

    # Build GPT prompt
    prompt = (
        f"The user's home is {profile['home_postcode']}, office is {profile['office_postcode']}, "
        f"car is a {profile['car_type']} with a {profile['engine_size']} engine, running on {profile['fuel_type']}. "
        f"Their heating type is {profile['heating_type']}.\n\n"
        f"They said: \"{input.message}\"\n\n"
        f"Calculate GHG emissions in kgCO₂e based on this input or ask for clarification if needed."
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

