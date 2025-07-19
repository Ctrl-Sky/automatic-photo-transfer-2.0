import os
import shutil
from datetime import datetime
from helpers import get_date_taken

def is_highest_date(highest_date, image_date):
    if image_date > highest_date:
        return True
    else:
        return False

def is_lowest_date(lowest_date, image_date):
    if image_date < lowest_date:
        return True
    else:
        return False
        
def image_before_end_on_date(image_date, end_on):
    if end_on == "":
        return True
    else:
        try:
            end_on = datetime.strptime(end_on, "%Y-%m-%d %H:%M:%S")
        except ValueError:
            end_on = datetime.strptime(end_on, "%Y-%m-%d")
        if image_date < end_on:
            return True
        else:
            return False
        
def copy_file_to_path(file, path):
    if not os.path.exists(path):
        os.makedirs(path, exist_ok=True)
    print(f"Copying {file} to {path}...")
    shutil.copy(file, path)

def transfer_photos(start_date, external_hd_path, path_to_photos, end_on=""):
    """
    Transfers photos from the specified path to an external hard drive, organizing them by date.
    Copies unsupported files to a separate folder.
    Tracks the earliest and latest photo dates transferred.

    :param start_date: The earliest date to transfer photos from (datetime object)
    :type start_date: datetime
    :param external_hd_path: The destination path on the external hard drive
    :type external_hd_path: string
    :param path_to_photos: The source path containing photos to transfer
    :type path_to_photos: string
    :param end_on: The latest date to transfer photos to (string, format "YYYY-MM-DD", optional)
    :type end_on: string
    :return: List containing info about the first and last transferred photo, or error message
    :rtype: list or string
    """
    # Arbitrary values meant to be replaced
    lowest_date = datetime(2100, 1, 1)
    highest_date = datetime(1990, 1, 1)

    photos = list(os.scandir(path_to_photos))
    for photo in photos:
        if photo.is_file():
            photo_name = photo.name
            path_to_photo = f"{path_to_photos}/{photo_name}"
            photo_info = get_date_taken(path_to_photo)

            # Directory included in other dir because of MacOS
            if photo_name == ".DS_Store":
                continue

            if photo_info == "File Format Not Supported":
                copy_file_to_path(path_to_photo, f"{external_hd_path}/unsupported")
                continue
            else:
                # method = photo_info[0]
                date = photo_info[1]

            if date > start_date and image_before_end_on_date(date, end_on):
                year = date.strftime("%Y")
                month = date.strftime("%b")
                day = date.strftime("%d")
                new_path_to_photos = f"{external_hd_path}/{year}-transfer/{month}/{month}_{day}"

                copy_file_to_path(path_to_photo, new_path_to_photos)

                if is_lowest_date(lowest_date, date):
                    # Starter values are written into the csv file for tracking
                    starter_dir = path_to_photos
                    starter_image = photo_name
                    starter_date = date
                    lowest_date = date

                if is_highest_date(highest_date, date):
                    # End values are written into the csv file for tracking
                    end_dir = path_to_photos
                    end_image = photo_name
                    end_date = date
                    highest_date = date

    try:
        csv_line = [starter_dir, starter_image, starter_date.strftime("%Y:%m:%d %H:%M:%S"), end_dir, end_image, end_date.strftime("%Y:%m:%d %H:%M:%S")]
    except NameError:
        return "did not contain any supported files"
    
    return csv_line

                

                    



