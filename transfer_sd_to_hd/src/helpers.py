import os
from datetime import datetime
from PIL import Image

def get_date_taken(image_path):
    image_file_ext = image_path.split(".")[-1]
    if image_file_ext == "HEIC":
        pass
    if image_file_ext == "PNG":
        pass
    if image_file_ext == "JPG" or image_file_ext == "JPEG":
        return get_JPG_date_taken(image_path)
    
def get_JPG_date_taken(image_path):
    """
        Get the date a JPG photo was taken
        
        :param image_path: The full path including file name of the image
        :type image_path: string
        :return: the date the photo was taken
        :rtype: string
    """
    exif = Image.open(image_path)._getexif()
    if not exif:
        return get_date_taken_os(image_path)
    
    try:
        date = exif[36867]
    except KeyError:
        return get_date_taken_os(image_path)
    
    datetime_date = datetime.strptime(date, "%Y:%m-%d %H:%M:%S")
    return ("exif", datetime_date)

def get_date_taken_os(image_path):
    posix_date = os.stat(image_path).st_birthtime
    datetime_date = datetime.fromtimestamp(posix_date)
    return ("os", datetime_date)

def convert_to_pretty_date(date, include_day=True):
    """
        Convert an exif date in the form YYYY:MM:DD HH:MM:SS into a pretty print of just month-year or month-date-year
        
        :param exif_date: A date in pulled from the EXIF
        :type exif_date: string
        :param include_date: Whether or not to return the date, default to False
        :type include_date: bool, optional
        :return: An easier to read string of the date
        :rtype: string
    """
    datetime_obj = datetime.strptime(date)
    
    if include_day:
        return datetime_obj.strftime("%b-%d-%Y")
    else:
        return datetime_obj.strftime("%b-%Y")