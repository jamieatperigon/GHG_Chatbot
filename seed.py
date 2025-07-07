from db import save_user_profile
import datetime

save_user_profile(
    user_id="jamie@perigonpartners.co.uk",
    home_postcode="EH39",
    office_postcode="EC1A 1AA",
    created_at=str(datetime.datetime.now())
)


