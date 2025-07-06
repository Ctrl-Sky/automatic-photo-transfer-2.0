import csv
import os

def does_path_exist(path):
    if not os.path.exists(path):
        raise Exception(f"{path} does not exist")

def initialize_table(table_path):
    """
        Takes a path to a csv file and if it doesn't exist, creates the file and adds the header

        :param table_path: The full path including the file name to a csv table
        :type table_path: string
    """
    # Create Parent Directories
    if os.path.dirname(table_path) != "" and not os.path.exists(os.path.dirname(table_path)):
        os.makedirs(os.path.dirname(table_path))

    # Create csv file
    with open(table_path, 'w') as file:
        writer = csv.writer(file)
        writer.writerow(["migration_name", "sd_card_name", "start_dir", "start_image", "start_date", "end_dir", "end_image", "end_date"])

def get_end_date_from_table(table_path, sd_card_path):
    """
        If the sd card is referenced within the table, get the date of the most recent photo that was uploaded from the sd card

        :param table_path: The full path to a csv table
        :type table_path: string
        :param sd_card_path: The full path to a sd card
        :type sd_card_path: string
        :return: date of photo most recently uploaded
        :rtype: string
    """
    sd_card_name = os.path.basename(sd_card_path)
    with open(table_path, 'r') as file:
        reversed_reader = reversed(list(csv.reader(file)))
        for row in reversed_reader:
            if row[1] == sd_card_name:
                # Return the end_date
                return row[7]
        return "1990:03:24 12:34:56"

def initialize_repo(sd_card_path, external_hd_path, table_path):
    """
        Within the table path, if the SD card had a recorded migration, pulls the most recent photo that was migrated from the SD 
        card and uses that as references for the next starting point for the next migration.
        If the SD card has never had a recorded migration, use the default values as the starting point

        :param sd_card_path: The full path to a sd card
        :type sd_card_path: string
        :param external_hd_path: The full path to a external hd
        :type external_hd_path: string
        :param table_path: The full path to a csv table
        :type table_path: string
        :return: date of photo most recently uploaded
        :rtype: string
    """
    does_path_exist(sd_card_path)
    does_path_exist(external_hd_path)

    # If table does not exist, create it and add headers
    if not os.path.exists(table_path):
        initialize_table(table_path)
    
    return get_end_date_from_table(table_path, sd_card_path)
