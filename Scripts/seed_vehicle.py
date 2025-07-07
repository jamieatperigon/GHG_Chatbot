from GHG_bot.db import add_user_vehicle, get_user_vehicles

# Example: Add a car
add_user_vehicle(
    user_id="jamie@perigonpartners.co.uk",
    name="Audi A3 e-tron",
    fuel_type="Petrol Plug-in Hybrid",
    factor_id=1234  # replace with the actual factor ID from your DEFRA table
)

# Verify
print(get_user_vehicles("jamie@perigonpartners.co.uk"))

