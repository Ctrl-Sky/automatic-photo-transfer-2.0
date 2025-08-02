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
    if image_file_ext == "HEIC":
        return get_HEIC_date_taken(image_path)
    elif image_file_ext == "PNG" or image_file_ext == "MP4" or image_file_ext == "MOV":
        return get_date_taken_os(image_path)
    elif image_file_ext == "JPG" or image_file_ext == "JPEG" or image_file_ext == "jpeg" or image_file_ext == "jpg":
        return get_JPG_date_taken(image_path)
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
    exif = Image.open(image_path)._getexif()
    if not exif:
        return get_date_taken_os(image_path)
    try:
        date = exif[36867]
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