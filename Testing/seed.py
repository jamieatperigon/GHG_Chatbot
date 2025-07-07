from db import save_user_profile, get_user_profile
import datetime

userID="jamie@perigonpartners.co.uk"

save_user_profile(
    user_id= userID,
    home_postcode="SL4 6DW",
    office_postcode="EC1A 1AA",
    created_at=str(datetime.datetime.now())
)

print("✅ User profile inserted.")
print("🔍 Verifying saved profile...")
print(get_user_profile(userID))