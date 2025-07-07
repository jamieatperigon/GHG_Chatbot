import sqlite3
from typing import Optional, List, Dict

# Unified database file name
DB_PATH = "GHG_chatbot_data.db"

def get_connection():
    return sqlite3.connect(DB_PATH)

# --------------------------
# USER PROFILES
# --------------------------

def get_user_profile(user_id: str) -> Optional[dict]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM user_profiles WHERE user_id = ?", (user_id,))
    row = cursor.fetchone()
    conn.close()
    if row:
        keys = ["user_id", "home_postcode", "office_postcode", "created_at"]
        return dict(zip(keys, row))
    return None

def save_user_profile(user_id, home_postcode, office_postcode, created_at):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        '''
        INSERT INTO user_profiles (user_id, home_postcode, office_postcode, created_at)
        VALUES (?, ?, ?, ?)
        ON CONFLICT(user_id) DO UPDATE SET
            home_postcode=excluded.home_postcode,
            office_postcode=excluded.office_postcode,
            created_at=excluded.created_at
        ''',
        (user_id, home_postcode, office_postcode, created_at)
    )
    conn.commit()
    conn.close()

# --------------------------
# USER VEHICLES
# --------------------------

def add_user_vehicle(user_id: str, name: str, fuel_type: str, factor_id: int):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO user_vehicles (user_id, name, fuel_type, factor_id)
        VALUES (?, ?, ?, ?)
    ''', (user_id, name, fuel_type, factor_id))
    conn.commit()
    conn.close()

def get_user_vehicles(user_id: str) -> List[dict]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT vehicle_id, name, fuel_type, factor_id FROM user_vehicles WHERE user_id = ?", (user_id,))
    rows = cursor.fetchall()
    conn.close()
    return [dict(zip(["vehicle_id", "name", "fuel_type", "factor_id"], row)) for row in rows]

# --------------------------
# USER ENERGY SOURCES
# --------------------------

def add_user_energy_source(user_id: str, fuel_type: str, factor_id: int, share_percent: float):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO user_energy_sources (user_id, fuel_type, factor_id, share_percent)
        VALUES (?, ?, ?, ?)
    ''', (user_id, fuel_type, factor_id, share_percent))
    conn.commit()
    conn.close()

def get_user_energy_sources(user_id: str) -> List[dict]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT energy_id, fuel_type, factor_id, share_percent FROM user_energy_sources WHERE user_id = ?", (user_id,))
    rows = cursor.fetchall()
    conn.close()
    return [dict(zip(["energy_id", "fuel_type", "factor_id", "share_percent"], row)) for row in rows]

# --------------------------
# CONVERSION FACTORS
# --------------------------

def get_conversion_factor_by_id(factor_id: int) -> Optional[dict]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM conversion_factors WHERE factor_id = ?", (factor_id,))
    row = cursor.fetchone()
    conn.close()
    if row:
        keys = ["factor_id", "type", "level_1", "level_2", "level_3", "level_4", "unit", "ghg_unit", "conversion_factor", "scope"]
        return dict(zip(keys, row))
    return None

# --------------------------
# EMISSION LOGGING
# --------------------------

def log_emission_entry(entry: Dict):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO emission_logs (
            user_id, date, route_description, distance_km,
            factor_id, wtt_factor_id, tnd_factor_id,
            emissions_direct, emissions_wtt, emissions_total,
            mode, vehicle_id, scope
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        entry["user_id"],
        entry["date"],
        entry["route_description"],
        entry["distance_km"],
        entry["factor_id"],
        entry.get("wtt_factor_id"),
        entry.get("tnd_factor_id"),
        entry["emissions_direct"],
        entry.get("emissions_wtt", 0),
        entry["emissions_total"],
        entry["mode"],
        entry.get("vehicle_id"),
        entry["scope"]
    ))
    conn.commit()
    conn.close()
