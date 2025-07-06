from src.helpers import get_date_taken
import os

PATH_TO_PHOTOS="tests/resources"

def test_get_date_taken_os_HEIC():
    assert get_date_taken(f"{PATH_TO_PHOTOS}/IMG_0034.HEIC") == ("os", "hi")

def test_get_date_taken_os_PNG():
    assert get_date_taken(f"{PATH_TO_PHOTOS}/IMG_1137.PNG") == ("os", "hi")

def test_get_date_taken_os_JPG():
    assert get_date_taken(f"{PATH_TO_PHOTOS}/IMG_4600.JPG") == ("os", "hi")

def test_get_date_taken_os_JPEG():
    assert get_date_taken(f"{PATH_TO_PHOTOS}/IMG_6050.JPEG") == ("os", "hi")

def test_get_date_taken_os_MP4():
    assert get_date_taken(f"{PATH_TO_PHOTOS}/JMT08755.MP4") == ("os", "hi")

def test_get_date_taken_os_MOV():
    assert get_date_taken(f"{PATH_TO_PHOTOS}/IMG_2687.MOV") == ("os", "hi")