import os
import shutil
from datetime import datetime
from src.transfer_photos import is_lowest_date, image_before_end_on_date, copy_file_to_path, transfer_photos
from src.helpers import get_date_taken

PATH_TO_PHOTOS="tests/resources/phone"

def test_is_lowest_date_yes_lower():
    assert is_lowest_date(datetime(2025, 5, 6, 2, 5, 3), datetime(2025, 5, 6, 2, 4, 3)) == True

def test_is_lowest_date_no_lower():
    assert is_lowest_date(datetime(2025, 5, 6, 2, 5, 3), datetime(2025, 5, 6, 2, 6, 3)) == False

def test_image_before_end_on_date_empty():
    assert image_before_end_on_date(datetime(2025, 5, 6, 2, 5, 3), "") == True

def test_image_before_end_on_date_is_before():
    assert image_before_end_on_date(datetime(2025, 5, 6, 2, 5, 3), "2025:06:06") == True

def test_image_before_end_on_date_is_not_before():
    assert image_before_end_on_date(datetime(2025, 5, 6, 2, 5, 3), "2025:04:06") == False

def test_copy_file_to_path_dir_exists():
    path_to_copy_dir = f"{PATH_TO_PHOTOS}/2025-transfer/Jul/Jul_06"
    path_to_copy=f"{path_to_copy_dir}/IMG_0034.HEIC"

    copy_file_to_path(f"{PATH_TO_PHOTOS}/IMG_0034.HEIC", path_to_copy_dir)
    assert os.path.exists(path_to_copy)

    # Clean up
    os.remove(path_to_copy)

def test_copy_file_path_dir_not_exists():
    dir = "2024-transfer"
    image = "IMG_0034.HEIC"
    path_to_copy_dir = f"{PATH_TO_PHOTOS}/{dir}/Jul/Jul_06"
    path_to_copy=f"{path_to_copy_dir}/{image}"

    copy_file_to_path(f"{PATH_TO_PHOTOS}/{image}", path_to_copy_dir)
    assert os.path.exists(path_to_copy)

    # Clean up
    os.remove(path_to_copy)
    shutil.rmtree(f"{PATH_TO_PHOTOS}/2024-transfer")

def test_copy_file_path_maintains_birthtime():
    path_to_copy_dir = f"{PATH_TO_PHOTOS}/2025-transfer/Jul/Jul_06"
    path_to_copy=f"{path_to_copy_dir}/IMG_0034.HEIC"

    copy_file_to_path(f"{PATH_TO_PHOTOS}/IMG_0034.HEIC", path_to_copy_dir)
    assert get_date_taken(path_to_copy)[1].strftime("%Y-%b-%d") == "2024-Jun-30"

    # Clean up
    os.remove(path_to_copy)

def test_transfer_photos_move_all():
    start_date = datetime(2023, 5, 2)
    external_hd_path = "tests/resources/external_hd"
    path_to_photos = "tests/resources/DCIM/101CANON"
    end_on = ""

    assert transfer_photos(start_date, external_hd_path, path_to_photos, end_on) == ['tests/resources/DCIM/101CANON', 'IMG_0034.HEIC', '2024:06:30 14:06:31', 'tests/resources/DCIM/101CANON', 'IMG_2687.MOV', '2025:07:05 16:23:23']
    assert os.path.exists(f"{external_hd_path}/2024-transfer/Jun/Jun_30/IMG_0034.HEIC")
    assert os.path.exists(f"{external_hd_path}/2024-transfer/Oct/Oct_02/IMG_1137.PNG")
    assert os.path.exists(f"{external_hd_path}/2024-transfer/Oct/Oct_02/JMTO8755.MP4")
    assert os.path.exists(f"{external_hd_path}/2024-transfer/Oct/Oct_31/IMG_4600.JPG")
    assert os.path.exists(f"{external_hd_path}/2025-transfer/Feb/Feb_27/IMG_6050.JPEG")
    assert os.path.exists(f"{external_hd_path}/2025-transfer/Jul/Jul_05/IMG_2687.MOV")

    # Clean up
    shutil.rmtree(f"{external_hd_path}/2024-transfer", ignore_errors=True)
    shutil.rmtree(f"{external_hd_path}/2025-transfer", ignore_errors=True)

# def test_transfer_photos_move_unsuppored_and_supported():
#     # move supported and unsupported photos

# def test_transfer_photos_move_only_unsupported():
#     # move only unsupported