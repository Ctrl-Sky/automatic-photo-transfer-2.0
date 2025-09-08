import csv
import os
from datetime import datetime, timezone

def verify_timezone(photo_timezone):
    current_timezone = datetime.now(timezone.utc).astimezone().tzinfo
    if photo_timezone != current_timezone:
        raise Exception("Timezone of photos does not match system timezone, please change it")

def does_path_exist(path):
    """
    Checks if the given path exists. Raises an Exception if it does not.

    :param path: The path to check.
    :type path: str
    :raises Exception: If the path does not exist.
    """
    if not os.path.exists(path):
        raise Exception(f"{path} does not exist")

def initialize_table(table_path):
    """
    Creates a CSV file at the specified path with the appropriate header if it does not exist.
    Also creates any necessary parent directories.

    :param table_path: The full path, including the file name, to the CSV table.
    :type table_path: str
    """
    # Create Parent Directories
    if os.path.dirname(table_path) != "" and not os.path.exists(os.path.dirname(table_path)):
        os.makedirs(os.path.dirname(table_path))

    # Create csv file
    with open(table_path, 'w') as file:
        writer = csv.writer(file)
        writer.writerow(["date_run", "migration_name", "unique_path", "start_image", "start_date", "end_image", "end_date", "timezone"])

def get_end_date_from_table(table_path, unqiue_path):
    """
    Retrieves the most recent migration information for the specified device from the CSV table.

    :param table_path: The full path to the CSV table.
    :type table_path: str
    :param device: The device name to look for ("camera" or "phone").
    :type device: str
    :return: A list containing [end_dir, end_image, end_date] of the most recent migration, or default values if not found.
    :rtype: list[str]
    """
    with open(table_path, 'r') as file:
        reversed_reader = reversed(list(csv.reader(file)))
        for row in reversed_reader:
            if row[2] == unqiue_path:
                # end_date
                return row[6]
        return "1990-03-24 12:34:56"

def initialize_repo(unique_path, external_hd_path, table_path, photo_timezone):
    """
    Initializes the migration repository for the specified device.
    Checks if the external HD path exists, creates the migration table if necessary,
    and retrieves the most recent migration information for the device.

    :param device: The device name ("camera" or "phone").
    :type device: str
    :param external_hd_path: The full path to the external hard drive.
    :type external_hd_path: str
    :param table_path: The full path to the CSV table.
    :type table_path: str
    :return: A list containing [end_dir, end_image, end_date as datetime] of the most recent migration.
    :rtype: list
    :raises Exception: If the device is not supported or the external HD path does not exist.
    """
    verify_timezone(photo_timezone)
    does_path_exist(external_hd_path)
    does_path_exist(unique_path)

    # If table does not exist, create it and add headers
    if not os.path.exists(table_path):
        initialize_table(table_path)
    
    image_info = get_end_date_from_table(table_path, unique_path)
    return datetime.strptime(image_info, "%Y-%m-%d %H:%M:%S")
