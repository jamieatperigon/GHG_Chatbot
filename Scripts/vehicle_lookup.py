import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


import sqlite3
from GHG_bot.db import add_user_vehicle

DB_PATH = "GHG_chatbot_data.db"

def get_connection():
    return sqlite3.connect(DB_PATH)

def fetch_all_passenger_vehicles():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT factor_id, level_2, level_3
        FROM conversion_factors
        WHERE type = 'Direct' AND level_1 = 'Passenger vehicles'
    ''')
    rows = cursor.fetchall()
    conn.close()
    return rows

def find_vehicle_matches(model_name: str) -> list:
    all_vehicles = fetch_all_passenger_vehicles()
    matches = []
    for factor_id, level_2, level_3 in all_vehicles:
        combined = f"{level_2 or ''} {level_3 or ''}".lower()
        if model_name.lower() in combined:
            matches.append((factor_id, level_2, level_3))
    return matches

def match_vehicle_model(model_name: str):
    matches = find_vehicle_matches(model_name)
    
    if not matches:
        print(f"❌ No match found for: {model_name}")
        return None

    if len(matches) == 1:
        print("✅ Unique match found.")
        return matches[0]

    # Prompt user if multiple matches exist
    print("⚠️ Multiple possible matches found. Please clarify:")
    for idx, (factor_id, level_2, level_3) in enumerate(matches, 1):
        print(f"{idx}. Fuel Type: {level_2}, Size: {level_3}")
    
    while True:
        choice = input("Enter the number corresponding to your vehicle: ")
        try:
            index = int(choice) - 1
            if 0 <= index < len(matches):
                return matches[index]
        except ValueError:
            pass
        print("Invalid input. Please enter a valid number.")

def add_vehicle_for_user(user_id: str, vehicle_name: str, model_input: str):
    result = match_vehicle_model(model_input)
    if result is None:
        print("❌ Vehicle not added.")
        return
    factor_id, fuel_type, _ = result
    add_user_vehicle(user_id=user_id, name=vehicle_name, fuel_type=fuel_type, factor_id=factor_id)
    print(f"✅ Vehicle '{vehicle_name}' added for user {user_id} with factor_id {factor_id}.")

# Example usage
if __name__ == "__main__":
    user_id = "jamie@perigonpartners.co.uk"
    vehicle_name = "Audi A6 PHEV"
    model_input = "plug-in hybrid diesel"
    
    add_vehicle_for_user(user_id, vehicle_name, model_input)
