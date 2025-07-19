import os
from datetime import datetime, timezone
from src.write_to_excel import write_to_migration_table
from src.initialize import initialize_table

DEVICE = "camera"
START_DIR = "/path"
START_IMAGE = "something.JPG"
START_DATE = "2024-05-05 15:15:15"
END_DIR = "/end_path"
END_IMAGE = "end.JPG"
END_DATE = "2025-05-05 15:15:15"
TABLE_PATH = "../tables/test.csv"
MIGRATION_NAME = "test"

def test_appending_data():
    initialize_table(TABLE_PATH)
    start_and_end_values = [START_DIR, START_IMAGE, START_DATE, END_DIR, END_IMAGE, END_DATE]
    write_to_migration_table(DEVICE, start_and_end_values, TABLE_PATH)

    with open(TABLE_PATH, 'r') as file:
        line = file.readline()
        line = file.readline()
        assert line.strip() == f'{datetime.now().strftime("%Y-%m-%d")},2024-05-05_2025-05-05,{DEVICE},{START_DIR},{START_IMAGE},{START_DATE},{END_DIR},{END_IMAGE},{END_DATE},{datetime.now(timezone.utc).astimezone().tzinfo}'

    # Clean up
    os.remove(TABLE_PATH)

def test_timezone_reminder():

    tz = datetime.now(timezone.utc).astimezone().tzinfo
    if str(tz) == "EST" or str(tz) == "EDT":
        assert True
    else:
        raise Exception("You are in a different timezone, make sure to shift times accordingly")

