import argparse
import os
from initialize import initialize_repo
from transfer_photos import transfer_photos
from write_to_excel import write_to_migration_table

CAMERA_TABLE_PATH = "../tables/camera_migration_table.csv"
PHONE_TABLE_PATH = "../tables/phone_migration_table.csv"

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--device")
    parser.add_argument("--path_to_photos")
    parser.add_argument("--destination_path", default="/Volumes/kl")
    parser.add_argument("--migration_name", required=False, default="")
    parser.add_argument("--end_on", required=False, default="")
    args = parser.parse_args()

    device = args.device
    path_to_photos = args.path_to_photos
    destination_path = args.destination_path
    migration_name = args.migration_name
    end_on = args.end_on
    unique_path = path_to_photos

    print(end_on)

    # if device == "camera":
    #     table_path = CAMERA_TABLE_PATH
    # elif device == "phone":
    #     table_path = PHONE_TABLE_PATH
    # else:
    #     raise Exception(f"{device} is not supported")

    # start_date = initialize_repo(path_to_photos, destination_path, table_path)
    # start_and_end_values = transfer_photos(start_date[2], destination_path, path_to_photos, end_on=end_on)

    # if start_and_end_values == "did not contain any supported files":
    #     print(f"No photos were moved, nothing written to {table_path}")
    # else:
    #     write_to_migration_table(unique_path, start_and_end_values, table_path, migration_name=migration_name)
        
    print("Complete")