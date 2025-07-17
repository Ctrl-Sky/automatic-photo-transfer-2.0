import subprocess
import os
from datetime import datetime
from transfer_photos import transfer_photos

# def get_creation_time_mac(path):
#     output = subprocess.check_output(['stat', '-f%B', path])
#     timestamp = int(output.strip())
#     return datetime.datetime.fromtimestamp(timestamp)

# print(get_creation_time_mac('/Volumes/SDCARD/file.jpg'))


# start_date = datetime(2023, 5, 2)
# external_hd_path = "tests/resources/external_hd"
path_to_photos = "tests/resources/DCIM/101CANON"
# end_on = ""

# transfer_photos(start_date, external_hd_path, path_to_photos, end_on=end_on)

photos = list(os.scandir(path_to_photos))
print(photos)