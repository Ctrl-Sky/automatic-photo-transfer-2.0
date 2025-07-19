from transfer_photos import transfer_photos
from datetime import datetime, timezone
import os

# transfer_photos(datetime(2024, 6, 4, 11, 54), "/Volumes/kl", "/Volumes/SD_CARD_1/DCIM/100CANON", end_on="2024-07-03 11:56:00")

print(datetime.now(timezone.utc).astimezone().tzinfo)
# datetime.timezone(datetime.timedelta(seconds=36000), 'AEST')