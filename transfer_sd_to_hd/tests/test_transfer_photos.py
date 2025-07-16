import os
import shutil
from datetime import datetime
from src.transfer_photos import is_lowest_date, image_before_end_on_date, copy_file_to_path
from src.helpers import get_date_taken, convert_to_pretty_date

PATH_TO_PHOTOS="tests/resources/phone"

def test_is_lowest_date_yes_lower():
    assert is_lowest_date(datetime(2025, 5, 6, 2, 5, 3), datetime(2025, 5, 6, 2, 4, 3)) == True

def test_is_lowest_date_no_lower():
    assert is_lowest_date(datetime(2025, 5, 6, 2, 5, 3), datetime(2025, 5, 6, 2, 6, 3)) == False

def test_image_before_end_on_date_empty():
    assert image_before_end_on_date("", datetime(2025, 5, 6, 2, 5, 3)) == True

def test_image_before_end_on_date_is_before():
    assert image_before_end_on_date("2025:06:06", datetime(2025, 5, 6, 2, 5, 3)) == True

def test_image_before_end_on_date_is_not_before():
    assert image_before_end_on_date("2025:04:06", datetime(2025, 5, 6, 2, 5, 3)) == False

def test_copy_file_to_path_dir_exists():
    path_to_copy_dir = f"{PATH_TO_PHOTOS}/2025-transfer/Jul/Jul_06-exif"
    path_to_copy=f"{path_to_copy_dir}/IMG_0034.HEIC"

    copy_file_to_path(f"{PATH_TO_PHOTOS}/IMG_0034.HEIC", path_to_copy_dir)
    assert os.path.exists(path_to_copy)
    assert get_date_taken(path_to_copy)[1].strftime("%Y-%b-%d") == "2024-Jun-30"

    # Clean up
    os.remove(path_to_copy)

def test_copy_file_path_dir_not_exists():
    dir = "2024-transfer"
    image = "IMG_0034.HEIC"
    path_to_copy_dir = f"{PATH_TO_PHOTOS}/{dir}/Jul/Jul_06-exif"
    path_to_copy=f"{path_to_copy_dir}/{image}"

    copy_file_to_path(f"{PATH_TO_PHOTOS}/{image}", path_to_copy_dir)
    assert os.path.exists(path_to_copy)
    assert get_date_taken(path_to_copy)[1].strftime("%Y-%b-%d") == "2024-Jun-30"

    # Clean up
    os.remove(path_to_copy)
    shutil.rmtree(f"{PATH_TO_PHOTOS}/2024-transfer")