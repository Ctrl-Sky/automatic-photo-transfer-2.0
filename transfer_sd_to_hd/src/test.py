import os
import datetime
PATH="/Volumes/SD_CARD_1/DCIM/100CANON"
# count = 0
# for file in os.listdir(PATH):
#     count += 1
#     date = os.stat(f"{PATH}/{file}").st_birthtime
#     print(file, datetime.datetime.fromtimestamp(date))
#     if count == 50:
#         break

print(os.stat(f"tests/resources/IMG_0034.HEIC"))