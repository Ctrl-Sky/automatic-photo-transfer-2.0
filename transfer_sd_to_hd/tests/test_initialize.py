import pytest
import os
import csv
from initialize import initialize_table, get_end_date_from_table, initialize_repo

CSV_PATH = "tests/resources/test.csv"
SD_CARD_1 = "tests/resources"
SD_CARD_2 = "SD_CARD_2"
HARD_DRIVE = "tests/resources/HARD_DRIVE"

def remove_csv_path(path):
    os.remove(path)
    if os.path.dirname(path) != "":
        os.rmdir(os.path.dirname(path))

def test_initialize_table():
    initialize_table(CSV_PATH)
    assert os.path.exists(CSV_PATH) == True
    with open(CSV_PATH, 'r') as file:
        read = csv.reader(file)
        for row in read:
            assert row == ['migration_name', 'sd_card_name', 'start_dir', 'start_image', 'start_date', 'end_dir', 'end_image', 'end_date']
            break

    # Clean up test environment
    os.remove(CSV_PATH)

def test_get_end_date_exist():
    # Initialize environment for testing get_end_date_from_table()
    initialize_table(CSV_PATH)
    with open(CSV_PATH, 'a') as file:
        writer = csv.writer(file)
        writer.writerow(["vacation_2024",os.path.basename(SD_CARD_1),"/DCIM/100CANON","IMG_0001.JPG","2024-07-01 09:00:00","/DCIM/101CANON","IMG_0150.JPG","2024-07-01 18:30:00"])

    # Test SD_CARD_NAME does exist in csv file
    assert get_end_date_from_table(CSV_PATH, SD_CARD_1) == "2024-07-01 18:30:00"

    # Clean up test environment
    os.remove(CSV_PATH)

def test_get_end_value_not_exist():
    # Initialize environment for testing get_end_date_from_table()
    initialize_table(CSV_PATH)
    with open(CSV_PATH, 'a') as file:
        writer = csv.writer(file)
        writer.writerow(["vacation_2024",os.path.basename(SD_CARD_1),"/DCIM/100CANON","IMG_0001.JPG","2024-07-01 09:00:00","/DCIM/101CANON","IMG_0150.JPG","2024-07-01 18:30:00"])

    # Test SD_CARD_NAME does NOT exist in csv file
    assert get_end_date_from_table(CSV_PATH, SD_CARD_2) == "1990:03:24 12:34:56"

    # Clean up test environment
    os.remove(CSV_PATH)

def test_initialize_repo_table_exist():
    '''
        Test when table already exist and sd card name exist in table
    '''
    # Initialize Environment for testing initialize_repo()
    os.makedirs(HARD_DRIVE)
    initialize_table(CSV_PATH)
    with open(CSV_PATH, 'a') as file:
        writer = csv.writer(file)
        writer.writerow(["vacation_2024",os.path.basename(SD_CARD_1),f"{SD_CARD_1}/DCIM/100CANON","IMG_0001.JPG","2024-07-01 09:00:00",f"{SD_CARD_1}/DCIM/101CANON","IMG_8422.JPG","2024:07:02 10:19:42"])

    assert initialize_repo(SD_CARD_1, HARD_DRIVE, CSV_PATH) == "2024:07:02 10:19:42"

    # Clean up test environment
    os.rmdir(HARD_DRIVE)
    os.remove(CSV_PATH)

def test_initialize_repo_table_not_exist():
    '''
        Test when table does not exist and sd card name does not exist within table
    '''
    # Initialize Environment for testing initialize_repo()
    os.makedirs(HARD_DRIVE)

    assert initialize_repo(SD_CARD_1, HARD_DRIVE, CSV_PATH) == "1990:03:24 12:34:56"

    # Clean up environment
    os.rmdir(HARD_DRIVE)
    os.remove(CSV_PATH)