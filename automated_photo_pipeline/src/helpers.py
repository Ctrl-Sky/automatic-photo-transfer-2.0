import os
import subprocess
from datetime import datetime
from PIL import Image, ExifTags
from pillow_heif import register_heif_opener

def get_date_taken(image_path):
    """
        Get the date a photo or video was taken, based on file extension and available metadata.

        :param image_path: The full path including file name of the image or video
        :type image_path: string
        :return: a tuple with the source ("exif" or "os") and the datetime object of the date taken
        :rtype: tuple[str, datetime.datetime]
    """
    image_file_ext = image_path.split(".")[-1]
    if image_file_ext == "HEIC" or image_file_ext == "heic":
        return get_HEIC_date_taken(image_path)
    elif image_file_ext == "MP4" or image_file_ext == "mp4" or image_file_ext == "PNG":
        return get_date_taken_os(image_path)
    elif image_file_ext == "JPG" or image_file_ext == "JPEG" or image_file_ext == "jpeg" or image_file_ext == "jpg":
        return get_JPG_date_taken(image_path)
    elif image_file_ext == "MOV" or image_file_ext == "mov":
        return get_MOV_date_taken(image_path)
    else:
        return "File Format Not Supported"
    
def get_JPG_date_taken(image_path):
    """
        Get the date a JPG photo was taken using EXIF data if available, otherwise fallback to file creation date.

        :param image_path: The full path including file name of the JPG image
        :type image_path: string
        :return: a tuple with the source ("exif" or "os") and the datetime object of the date taken
        :rtype: tuple[str, datetime.datetime]
    """
    try:
        exif = Image.open(image_path)._getexif()
    except AttributeError:
        exif = Image.open(image_path).getexif()
    if not exif:
        return get_date_taken_os(image_path)
    try:
        date = exif[36867] # Get date taken value
    except KeyError:
        return get_date_taken_os(image_path)
    
    datetime_date = datetime.strptime(date, "%Y:%m:%d %H:%M:%S")
    return ("exif", datetime_date)

def get_HEIC_date_taken(image_path):
    """
        Get the date a HEIC photo was taken using EXIF data if available, otherwise fallback to file creation date.

        :param image_path: The full path including file name of the HEIC image
        :type image_path: string
        :return: a tuple with the source ("exif" or "os") and the datetime object of the date taken
        :rtype: tuple[str, datetime.datetime]
    """
    register_heif_opener()
    exif = Image.open(image_path).getexif()
    if not exif:
        return get_date_taken_os(image_path)
    try:
        date = exif[306]
    except KeyError:
        return get_date_taken_os(image_path)

    datetime_date = datetime.strptime(date, "%Y:%m:%d %H:%M:%S")
    return ("exif", datetime_date)

def get_date_taken_os(image_path):
    """
        Get the file creation date from the operating system for images or videos without EXIF data.

        :param image_path: The full path including file name of the image or video
        :type image_path: string
        :return: a tuple with the source ("os") and the datetime object of the file creation date
        :rtype: tuple[str, datetime.datetime]
    """
    posix_date = os.stat(image_path).st_birthtime
    datetime_date = datetime.fromtimestamp(posix_date)
    return ("os", datetime_date)

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

def get_MOV_date_taken(image_path):
    try:
        datetime_date = get_mov_timestamps(image_path)
        if datetime_date == None:
            return get_date_taken_os(image_path)
        return ("exif", datetime_date)
    except:
        return get_date_taken_os(image_path)