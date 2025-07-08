import os
from src.transfer_photos import copy_file_to_path

PATH_TO_PHOTOS="tests/resources/phone"

def test_copy_file_to_path():
    copy_file_to_path(f"{PATH_TO_PHOTOS}/IMG_0034.HEIC", f"{PATH_TO_PHOTOS}/2025-transfer/Jul/Jul_06-exif")
    assert os.path.exists(f"{PATH_TO_PHOTOS}/2025-transfer/Jul/Jul_06-exif")