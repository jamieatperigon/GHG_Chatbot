import sqlite3
from typing import Optional



DB_PATH = "ghg_bot.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_profiles (
            id TEXT PRIMARY KEY,
            home_postcode TEXT,
            office_postcode TEXT,
            car_type TEXT,
            engine_size TEXT,
            fuel_type TEXT,
            heating_type TEXT,
            setup_complete BOOLEAN DEFAULT 0
        )
    ''')
    conn.commit()
    conn.close()

def get_user_profile(user_id: str) -> Optional[dict]:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM user_profiles WHERE id = ?", (user_id,))
    row = cursor.fetchone()
    conn.close()
    if row:
        keys = ["id", "home_postcode", "office_postcode", "car_type", "engine_size", "fuel_type", "heating_type", "setup_complete"]
        return dict(zip(keys, row))
    return None

def save_user_profile(user_id: str, profile_data: dict):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO user_profiles (id, home_postcode, office_postcode, car_type, engine_size, fuel_type, heating_type, setup_complete)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(id) DO UPDATE SET
            home_postcode=excluded.home_postcode,
            office_postcode=excluded.office_postcode,
            car_type=excluded.car_type,
            engine_size=excluded.engine_size,
            fuel_type=excluded.fuel_type,
            heating_type=excluded.heating_type,
            setup_complete=excluded.setup_complete
    ''', (
        user_id,
        profile_data.get("home_postcode"),
        profile_data.get("office_postcode"),
        profile_data.get("car_type"),
        profile_data.get("engine_size"),
        profile_data.get("fuel_type"),
        profile_data.get("heating_type"),
        profile_data.get("setup_complete", False)
    ))
    conn.commit()
    conn.close()
