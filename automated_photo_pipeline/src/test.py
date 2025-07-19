from transfer_photos import transfer_photos
from datetime import datetime, timezone
import os

from write_to_excel import write_to_migration_table
from initialize import initialize_table

# transfer_photos(datetime(2024, 6, 4, 11, 54), "/Volumes/kl", "/Volumes/SD_CARD_1/DCIM/100CANON", end_on="2024-07-03 11:56:00")

# print(datetime.now(timezone.utc).astimezone().tzinfo)
# datetime.timezone(datetime.timedelta(seconds=36000), 'AEST')

DEVICE = "camera"
START_DIR = "/path"
START_IMAGE = "something.JPG"
START_DATE = "2024-05-05 15:15:15"
END_DIR = "/end_path"
END_IMAGE = "end.JPG"
END_DATE = "2025-05-05 15:15:15"
TABLE_PATH = "../tables/test.csv"
MIGRATION_NAME = "test"

# initialize_table(TABLE_PATH)
write_to_migration_table(DEVICE, START_DIR, START_IMAGE, START_DATE, END_DIR, END_IMAGE, END_DATE, TABLE_PATH)
write_to_migration_table(DEVICE, START_DIR, START_IMAGE, START_DATE, END_DIR, END_IMAGE, END_DATE, TABLE_PATH)