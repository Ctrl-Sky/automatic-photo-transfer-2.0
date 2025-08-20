from transfer_photos import transfer_photos
from datetime import datetime, timezone
import os
from helpers import get_date_taken_os, get_date_taken
import transfer_photos

PATH_TO_PHOTOS="tests/resources/phone"
EXTERNAL_HD_PATH = "tests/resources/external_hd"
PATH_TO_PHOTOS_2 = "tests/resources/DCIM/101CANON"
PATH_TO_PHOTOS_3 = "tests/resources/DCIM/103CANON"

# print(get_date_taken(f"{PATH_TO_PHOTOS_2}/IMG_1137.PNG"))

def get_mov_timestamps(filename):
    ''' Get the creation and modification date-time from .mov metadata.

        Returns None if a value is not available.
    '''
    from datetime import datetime as DateTime
    import struct

    ATOM_HEADER_SIZE = 8
    # difference between Unix epoch and QuickTime epoch, in seconds
    EPOCH_ADJUSTER = 2082844800

    creation_time = None

    # search for moov item
    with open(filename, "rb") as f:
        while True:
            atom_header = f.read(ATOM_HEADER_SIZE)
            #~ print('atom header:', atom_header)  # debug purposes
            if atom_header[4:8] == b'moov':
                break  # found
            else:
                atom_size = struct.unpack('>I', atom_header[0:4])[0]
                f.seek(atom_size - 8, 1)

        # found 'moov', look for 'mvhd' and timestamps
        atom_header = f.read(ATOM_HEADER_SIZE)
        if atom_header[4:8] == b'cmov':
            raise RuntimeError('moov atom is compressed')
        elif atom_header[4:8] != b'mvhd':
            raise RuntimeError('expected to find "mvhd" header.')
        else:
            f.seek(4, 1)
            creation_time = struct.unpack('>I', f.read(4))[0] - EPOCH_ADJUSTER
            creation_time = DateTime.fromtimestamp(creation_time)
            if creation_time.year < 1990:  # invalid or censored data
                creation_time = None

    return creation_time

# print(get_mov_timestamps(f"/Users/sky/Downloads/IMG_2136_1754242566780.mov"))
# print(get_date_taken(f"/Volumes/kl/unsupported/video_01-22-2025_18-16-40.mp4"))

# print(os.environ.get("hello"))

# {366783: "2025-02-02"}

# date = datetime(2015, 6, 9)
# new_path_to_photos = "hello"

# transfer_photos.set_new_creation_date(new_path_to_photos, date)
# transfer_photos.set_new_modification_date(new_path_to_photos, date)

# print(get_date_taken_os("/Users/Sky/Downloads/Skys_iPhone/IMG_0007.HEIC"))

image_path = "/Volumes/kl/2025-transfer/08.Aug/Aug_17/IMG_0147.jpeg"
posix_date = os.stat(image_path).st_birthtime
datetime_date = datetime.fromtimestamp(posix_date)
print(datetime_date)