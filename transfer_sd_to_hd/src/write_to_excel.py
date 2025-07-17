import csv
import os
from helpers import convert_to_month_year

def write_to_migration_table(sd_card_path, start_dir, start_image, start_date, end_dir, end_image, end_date, table_path, migration_name=""):
    if migration_name == "":
        pretty_start = convert_to_month_year(start_date, include_day=True)
        pretty_end = convert_to_month_year(end_date, include_day=True)
        migration_name = f"{pretty_start}_{pretty_end}"

    sd_card_name = os.path.basename(sd_card_path)

    data = [migration_name, sd_card_name, start_dir, start_image, start_date, end_dir, end_image, end_date]

    if not os.path.exists(table_path):
        raise Exception(f"{table_path} does not exist")

    with open(table_path, 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(data)
