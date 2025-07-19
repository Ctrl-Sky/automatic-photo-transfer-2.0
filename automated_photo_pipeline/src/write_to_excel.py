import csv
import os
from datetime import datetime, timezone

def write_to_migration_table(device, start_and_end_values, table_path, migration_name=""):
    start_dir = start_and_end_values[0]
    start_image = start_and_end_values[1]
    start_date = start_and_end_values[2]
    end_dir = start_and_end_values[3]
    end_image = start_and_end_values[4]
    end_date = start_and_end_values[5]

    if migration_name == "":
        pretty_start = start_date.split()[0]
        pretty_end = end_date.split()[0]
        migration_name = f"{pretty_start}_{pretty_end}"

    current_timezone = datetime.now(timezone.utc).astimezone().tzinfo

    today = datetime.now().strftime("%Y-%m-%d")

    data = [today, migration_name, device, start_dir, start_image, start_date, end_dir, end_image, end_date, current_timezone]

    if not os.path.exists(table_path):
        raise Exception(f"{table_path} does not exist")

    print(f"Writing to {table_path}")
    with open(table_path, 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(data)
