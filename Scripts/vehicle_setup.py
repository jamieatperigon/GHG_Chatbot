import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from db import find_best_vehicle_factor, add_user_vehicle
import datetime

def run_vehicle_setup():
    print("🔧 Let's register a vehicle for your profile.")

    user_id = input("Enter your email address: ").strip()
    name = input("What would you like to name this vehicle? ").strip()
    fuel_type = input("Fuel type? (e.g. Petrol, Diesel, Plug-in Hybrid Petrol, Electric): ").strip()
    engine_size = input("Engine size or category (e.g. Small, Medium, 2.0L, N/A for EVs): ").strip()

    print("\n🔍 Searching for DEFRA conversion factors...")
    matches = find_best_vehicle_factor(fuel_type, engine_size)

    if not matches:
        print("⚠️ No clear match found. Please double-check fuel type or engine size.")
        return

    print(f"\nFound {len(matches)} potential matches:")
    for i, m in enumerate(matches, 1):
        print(f"{i}. ID: {m['factor_id']}, {m['level_2']} – {m['level_3']} ({m['conversion_factor']} {m['ghg_unit']})")

    selection = input("\n✅ Enter the number of the matching factor: ").strip()
    try:
        index = int(selection) - 1
        chosen = matches[index]
    except (IndexError, ValueError):
        print("❌ Invalid selection.")
        return

    confirm = input(f"Add this vehicle with factor ID {chosen['factor_id']}? (yes/no): ").strip().lower()
    if confirm != "yes":
        print("🚫 Cancelled.")
        return

    add_user_vehicle(user_id, name, fuel_type, chosen["factor_id"])
    print(f"✅ Vehicle '{name}' saved successfully for {user_id}.")

if __name__ == "__main__":
    run_vehicle_setup()
