import os
from datetime import datetime
from PIL import Image, ExifTags
from pillow_heif import register_heif_opener

PATH="/Volumes/SD_CARD_1/DCIM/100CANON"
# count = 0
# for file in os.listdir(PATH):
#     count += 1
#     date = os.stat(f"{PATH}/{file}").st_birthtime
#     print(file, datetime.datetime.fromtimestamp(date))
#     if count == 50:
#         break

# posix_date = os.stat("tests/resources/IMG_0034.HEIC").st_birthtime
# datetime_date = datetime.fromtimestamp(posix_date)
# print(datetime_date)

# def get_HEIC_date_taken(image_path):
#     register_heif_opener()
#     image = Image.open(image_path)
#     print(image.getexif()[306])

# get_HEIC_date_taken("tests/resources/IMG_2525.HEIC")

with os.scandir("tests/resources/phone") as d:
    for e in d:
        if e.is_file():
            print(e.name)