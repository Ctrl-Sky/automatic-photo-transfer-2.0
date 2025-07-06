import datetime
from src.helpers import get_date_taken_os, get_JPG_date_taken, get_HEIC_date_taken, get_date_taken

PATH_TO_PHOTOS="tests/resources"
PATH_TO_GOOD_JPG="tests/resources/DCIM/100CANON/IMG_0032.JPG"

# --------- Test get_date_taken_os for diff file types --------- 
def test_get_date_taken_os_HEIC():
    assert get_date_taken_os(f"{PATH_TO_PHOTOS}/IMG_0034.HEIC") == ("os", datetime.datetime(2024, 6, 30, 14, 6, 31))

def test_get_date_taken_os_PNG():
    assert get_date_taken_os(f"{PATH_TO_PHOTOS}/IMG_1137.PNG") == ("os", datetime.datetime(2024, 10, 2, 8, 44, 57))

def test_get_date_taken_os_JPG():
    assert get_date_taken_os(f"{PATH_TO_PHOTOS}/IMG_4600.JPG") == ("os", datetime.datetime(2024, 10, 31, 23, 45, 45))

def test_get_date_taken_os_JPEG():
    assert get_date_taken_os(f"{PATH_TO_PHOTOS}/IMG_6050.JPEG") == ("os", datetime.datetime(2025, 2, 27, 18, 11, 48))

def test_get_date_taken_os_MP4():
    assert get_date_taken_os(f"{PATH_TO_PHOTOS}/JMTO8755.MP4") == ("os", datetime.datetime(2024, 10, 2, 16, 4, 44))

def test_get_date_taken_os_MOV():
    assert get_date_taken_os(f"{PATH_TO_PHOTOS}/IMG_2687.MOV") == ("os", datetime.datetime(2025, 7, 5, 16, 23, 23))

# --------- Test get_JPG_date_taken for diff file types --------- 
def test_get_JPG_date_taken_yes_exif():
    assert get_JPG_date_taken(PATH_TO_GOOD_JPG) == ("exif", datetime.datetime(2024, 7, 24, 6, 35, 20))

def test_get_JPG_date_taken_no_exif():
    assert get_JPG_date_taken(f"{PATH_TO_PHOTOS}/IMG_4600.JPG") == ("os", datetime.datetime(2024, 10, 31, 23, 45, 45))

# --------- Test get_HEIC_date_taken for diff file types --------- 
def test_get_HEIC_date_taken_yes_exif():
    assert get_HEIC_date_taken(f"{PATH_TO_PHOTOS}/IMG_0034.HEIC") == ("exif", datetime.datetime(2024, 6, 30, 14, 6, 31))

def test_get_HEIC_date_taken_no_exif():
    assert get_HEIC_date_taken(f"{PATH_TO_PHOTOS}/IMG_4600.JPG") == ("os", datetime.datetime(2024, 10, 31, 23, 45, 45))

# --------- Test get_date_taken for diff file types --------- 
def test_get_date_taken_HEIC():
    assert get_date_taken(f"{PATH_TO_PHOTOS}/IMG_0034.HEIC") == ("exif", datetime.datetime(2024, 6, 30, 14, 6, 31))

def test_get_date_taken_PNG():
    assert get_date_taken(f"{PATH_TO_PHOTOS}/IMG_1137.PNG") == ("os", datetime.datetime(2024, 10, 2, 8, 44, 57))

def test_get_date_taken_JPG():
    assert get_date_taken(f"{PATH_TO_PHOTOS}/IMG_4600.JPG") == ("os", datetime.datetime(2024, 10, 31, 23, 45, 45))

def test_get_date_taken_good_JPG():
    assert get_date_taken(PATH_TO_GOOD_JPG) == ("exif", datetime.datetime(2024, 7, 24, 6, 35, 20))

def test_get_date_taken_JPEG():
    assert get_date_taken(f"{PATH_TO_PHOTOS}/IMG_6050.JPEG") == ("os", datetime.datetime(2025, 2, 27, 18, 11, 48))

def test_get_date_taken_MP4():
    assert get_date_taken(f"{PATH_TO_PHOTOS}/JMTO8755.MP4") == ("os", datetime.datetime(2024, 10, 2, 16, 4, 44))

def test_get_date_taken_MOV():
    assert get_date_taken(f"{PATH_TO_PHOTOS}/IMG_2687.MOV") == ("os", datetime.datetime(2025, 7, 5, 16, 23, 23))

def test_get_date_take_unsupported():
    assert get_date_taken(f"{PATH_TO_PHOTOS}/IMG_2687.WHAT") == "File Format Not Supported"