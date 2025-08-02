import os
import shutil
from datetime import datetime
from src.transfer_photos import is_lowest_date, image_before_end_on_date, copy_file_to_path, transfer_photos, convert_heic_to_jpeg
from src.helpers import get_date_taken

PATH_TO_PHOTOS="tests/resources/phone"
EXTERNAL_HD_PATH = "tests/resources/external_hd"
PATH_TO_PHOTOS_2 = "tests/resources/DCIM/101CANON"
PATH_TO_PHOTOS_3 = "tests/resources/DCIM/103CANON"

def test_is_lowest_date_yes_lower():
    assert is_lowest_date(datetime(2025, 5, 6, 2, 5, 3), datetime(2025, 5, 6, 2, 4, 3)) == True

def test_is_lowest_date_no_lower():
    assert is_lowest_date(datetime(2025, 5, 6, 2, 5, 3), datetime(2025, 5, 6, 2, 6, 3)) == False

def test_image_before_end_on_date_empty():
    assert image_before_end_on_date(datetime(2025, 5, 6, 2, 5, 3), "") == True

def test_image_before_end_on_date_is_before():
    assert image_before_end_on_date(datetime(2025, 5, 6, 2, 5, 3), "2025-06-06") == True

def test_image_before_end_on_date_is_not_before():
    assert image_before_end_on_date(datetime(2025, 5, 6, 2, 5, 3), "2025-04-06") == False

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

def test_convert_heic_to_jpg():
    convert_heic_to_jpeg(PATH_TO_PHOTOS_3, "IMG_0034.HEIC", testing=True)
    path = f"{PATH_TO_PHOTOS_3}/IMG_0034.jpeg"
    assert os.path.exists(path)
    os.remove(path)

def test_transfer_photos_move_all():
    start_date = datetime(2023, 5, 2)
    end_on = ""

    assert transfer_photos(start_date, EXTERNAL_HD_PATH, PATH_TO_PHOTOS_2, end_on, testing=True) == ['IMG_0034.jpeg', '2024-06-30 14:06:31','IMG_2687.MOV', '2025-07-05 16:23:23']
    assert os.path.exists(f"{EXTERNAL_HD_PATH}/2024-transfer/Jun/Jun_30/IMG_0034.jpeg")
    assert os.path.exists(f"{EXTERNAL_HD_PATH}/2024-transfer/Oct/Oct_02/IMG_1137.PNG")
    assert os.path.exists(f"{EXTERNAL_HD_PATH}/2024-transfer/Oct/Oct_02/JMTO8755.MP4")
    assert os.path.exists(f"{EXTERNAL_HD_PATH}/2024-transfer/Oct/Oct_31/IMG_4600.JPG")
    assert os.path.exists(f"{EXTERNAL_HD_PATH}/2025-transfer/Feb/Feb_27/IMG_6050.JPEG")
    assert os.path.exists(f"{EXTERNAL_HD_PATH}/2025-transfer/Jul/Jul_05/IMG_2687.MOV")

    # Clean up
    os.remove(f"{PATH_TO_PHOTOS_2}/{"IMG_0034.jpeg"}")
    shutil.rmtree(f"{EXTERNAL_HD_PATH}/2024-transfer", ignore_errors=True)
    shutil.rmtree(f"{EXTERNAL_HD_PATH}/2025-transfer", ignore_errors=True)

def test_transfer_photos_move_with_start_date_restriction():
    start_date = datetime(2024, 10, 5)
    end_on = ""

    assert transfer_photos(start_date, EXTERNAL_HD_PATH, PATH_TO_PHOTOS_2, end_on, testing=True) == ['IMG_4600.JPG', '2024-10-31 23:45:45', 'IMG_2687.MOV', '2025-07-05 16:23:23']
    assert not os.path.exists(f"{EXTERNAL_HD_PATH}/2024-transfer/Jun/Jun_30/IMG_0034.jpeg")
    assert not os.path.exists(f"{EXTERNAL_HD_PATH}/2024-transfer/Oct/Oct_02/IMG_1137.PNG")
    assert not os.path.exists(f"{EXTERNAL_HD_PATH}/2024-transfer/Oct/Oct_02/JMTO8755.MP4")
    assert os.path.exists(f"{EXTERNAL_HD_PATH}/2024-transfer/Oct/Oct_31/IMG_4600.JPG")
    assert os.path.exists(f"{EXTERNAL_HD_PATH}/2025-transfer/Feb/Feb_27/IMG_6050.JPEG")
    assert os.path.exists(f"{EXTERNAL_HD_PATH}/2025-transfer/Jul/Jul_05/IMG_2687.MOV")

    # Clean up
    shutil.rmtree(f"{EXTERNAL_HD_PATH}/2024-transfer", ignore_errors=True)
    shutil.rmtree(f"{EXTERNAL_HD_PATH}/2025-transfer", ignore_errors=True)

def test_transfer_photos_move_with_end_on_restriction():
    start_date = datetime(2023, 10, 5)
    end_on = "2024-10-05"

    assert transfer_photos(start_date, EXTERNAL_HD_PATH, PATH_TO_PHOTOS_2, end_on, testing=True) == ['IMG_0034.jpeg', '2024-06-30 14:06:31', 'JMTO8755.MP4', '2024-10-02 16:04:44']
    assert os.path.exists(f"{EXTERNAL_HD_PATH}/2024-transfer/Jun/Jun_30/IMG_0034.jpeg")
    assert os.path.exists(f"{EXTERNAL_HD_PATH}/2024-transfer/Oct/Oct_02/IMG_1137.PNG")
    assert os.path.exists(f"{EXTERNAL_HD_PATH}/2024-transfer/Oct/Oct_02/JMTO8755.MP4")
    assert not os.path.exists(f"{EXTERNAL_HD_PATH}/2024-transfer/Oct/Oct_31/IMG_4600.JPG")
    assert not os.path.exists(f"{EXTERNAL_HD_PATH}/2025-transfer/Feb/Feb_27/IMG_6050.JPEG")
    assert not os.path.exists(f"{EXTERNAL_HD_PATH}/2025-transfer/Jul/Jul_05/IMG_2687.MOV")

    # Clean up
    os.remove(f"{PATH_TO_PHOTOS_2}/{"IMG_0034.jpeg"}")
    shutil.rmtree(f"{EXTERNAL_HD_PATH}/2024-transfer", ignore_errors=True)

def test_transfer_photos_move_unsuppored_and_supported():
    path_to_copy = f"{PATH_TO_PHOTOS_2}/IMG_0034.WHAT"
    shutil.copy(f"{PATH_TO_PHOTOS_2}/IMG_0034.HEIC", path_to_copy)
    start_date = datetime(2023, 10, 5)
    end_on = ""

    assert transfer_photos(start_date, EXTERNAL_HD_PATH, PATH_TO_PHOTOS_2, end_on, testing=True) == ['IMG_0034.jpeg', '2024-06-30 14:06:31', 'IMG_2687.MOV', '2025-07-05 16:23:23']
    assert os.path.exists(f"{EXTERNAL_HD_PATH}/2024-transfer/Jun/Jun_30/IMG_0034.jpeg")
    assert os.path.exists(f"{EXTERNAL_HD_PATH}/2024-transfer/Oct/Oct_02/IMG_1137.PNG")
    assert os.path.exists(f"{EXTERNAL_HD_PATH}/2024-transfer/Oct/Oct_02/JMTO8755.MP4")
    assert os.path.exists(f"{EXTERNAL_HD_PATH}/2024-transfer/Oct/Oct_31/IMG_4600.JPG")
    assert os.path.exists(f"{EXTERNAL_HD_PATH}/2025-transfer/Feb/Feb_27/IMG_6050.JPEG")
    assert os.path.exists(f"{EXTERNAL_HD_PATH}/2025-transfer/Jul/Jul_05/IMG_2687.MOV")
    assert os.path.exists(f"{EXTERNAL_HD_PATH}/unsupported/IMG_0034.WHAT")

    # Clean up
    os.remove(path_to_copy)
    os.remove(f"{PATH_TO_PHOTOS_2}/{"IMG_0034.jpeg"}")
    shutil.rmtree(f"{EXTERNAL_HD_PATH}/2024-transfer", ignore_errors=True)
    shutil.rmtree(f"{EXTERNAL_HD_PATH}/2025-transfer", ignore_errors=True)
    shutil.rmtree(f"{EXTERNAL_HD_PATH}/unsupported", ignore_errors=True)

def test_transfer_photos_move_only_unsupported():
    start_date = datetime(2023, 10, 5)
    end_on = ""

    assert transfer_photos(start_date, EXTERNAL_HD_PATH, "tests/resources/DCIM/102CANON", end_on) == "did not contain any supported files"
    assert os.path.exists(f"{EXTERNAL_HD_PATH}/unsupported/IMG_0034.WHAT")
    assert os.path.exists(f"{EXTERNAL_HD_PATH}/unsupported/IMG_1137.WHAT")

    # Clean up
    shutil.rmtree(f"{EXTERNAL_HD_PATH}/unsupported", ignore_errors=True)
