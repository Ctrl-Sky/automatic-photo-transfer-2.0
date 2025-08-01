import pytest
import os
import csv
from datetime import datetime
from initialize import initialize_table, get_end_date_from_table, initialize_repo

CSV_PATH = "tests/resources/test.csv"
CAMERA = "tests/resources/camera"
PHONE = "phone"
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
            assert row == ['date_run', 'migration_name', 'unique_path', 'start_image', 'start_date', 'end_image', 'end_date', 'timezone']
            break

    # Clean up test environment
    os.remove(CSV_PATH)

def test_get_end_date_exist():
    # Initialize environment for testing get_end_date_from_table()
    initialize_table(CSV_PATH)
    with open(CSV_PATH, 'a') as file:
        writer = csv.writer(file)
        writer.writerow(['2025-05-05', "vacation_2024",CAMERA,"IMG_0001.JPG","2024-07-01 09:00:00","IMG_0150.JPG","2024-07-01 18:30:00", 'EST'])

    # Test SD_CARD_NAME does exist in csv file
    assert get_end_date_from_table(CSV_PATH, CAMERA) == "2024-07-01 18:30:00"

    # Clean up test environment
    os.remove(CSV_PATH)

def test_get_end_value_not_exist():
    # Initialize environment for testing get_end_date_from_table()
    initialize_table(CSV_PATH)
    with open(CSV_PATH, 'a') as file:
        writer = csv.writer(file)
        writer.writerow(['2025-05-05', "vacation_2024",CAMERA,"IMG_0001.JPG","2024-07-01 09:00:00","IMG_0150.JPG","2024-07-01 18:30:00", 'EST'])

    # Test SD_CARD_NAME does NOT exist in csv file
    assert get_end_date_from_table(CSV_PATH, PHONE) == "1990-03-24 12:34:56"

    # Clean up test environment
    os.remove(CSV_PATH)

def test_initialize_repo_table_exist():
    '''
        Test when table already exist and sd card name exist in table
    '''
    # Initialize Environment for testing initialize_repo()
    os.makedirs(HARD_DRIVE)
    os.makedirs(CAMERA)
    initialize_table(CSV_PATH)
    with open(CSV_PATH, 'a') as file:
        writer = csv.writer(file)
        writer.writerow(['2025-05-05', "vacation_2024",CAMERA,"IMG_0001.JPG","2024-07-01 09:00:00","IMG_8422.JPG","2024-07-02 10:19:42", "EST"])

    assert initialize_repo(CAMERA, HARD_DRIVE, CSV_PATH) == datetime(2024, 7, 2, 10, 19, 42)

    # Clean up test environment
    os.rmdir(HARD_DRIVE)
    os.rmdir(CAMERA)
    os.remove(CSV_PATH)

def test_initialize_repo_table_not_exist():
    '''
        Test when table does not exist and sd card name does not exist within table
    '''
    # Initialize Environment for testing initialize_repo()
    os.makedirs(HARD_DRIVE)
    os.makedirs(CAMERA)

    assert initialize_repo(CAMERA, HARD_DRIVE, CSV_PATH) == datetime(1990, 3, 24, 12, 34, 56)

    # Clean up environment
    os.rmdir(CAMERA)
    os.rmdir(HARD_DRIVE)
    os.remove(CSV_PATH)