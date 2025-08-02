import os
import shutil
from PIL import Image
from datetime import datetime
from subprocess import call
from helpers import get_date_taken

def convert_heic_to_jpeg(path_to_heic, heic_name, testing=False):

    # Open HEIF or HEIC file
    image = Image.open(f"{path_to_heic}/{heic_name}")
    new_image_name = heic_name.split(".")[0] + '.jpeg'
    new_path = os.path.join(path_to_heic, new_image_name)

    # Convert to JPEG
    image.convert('RGB').save(new_path)

    if not testing:
        os.remove(f"{path_to_heic}/{heic_name}")

    return new_image_name

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

def set_new_creation_date(path_to_file, new_date):
    cmd = 'SetFile -d ' + f'"{new_date.strftime("%m/%d/%Y %H:%M:%S")}" ' + f'"{path_to_file}"'
    call(cmd, shell=True)

def set_new_modification_date(path_to_file, new_date):
    cmd = 'SetFile -m ' + f'"{new_date.strftime("%m/%d/%Y %H:%M:%S")}" ' + f'"{path_to_file}"'
    call(cmd, shell=True)

def transfer_photos(start_date, external_hd_path, path_to_photos, end_on="", testing=False):
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
    count = 0
    for photo in photos:
        count += 1
        if photo.is_file():
            photo_name = photo.name
            path_to_photo = f"{path_to_photos}/{photo_name}"

            # MacOS creates files that start with ._ to contain even more metadata of specific files
            if photo_name[:2] == "._":
                continue

            # .DS_Store is included in directories because of MacOS, .AAE files are apple side car for photos edits
            if photo_name == ".DS_Store" or path_to_photo.split(".")[1] == "AAE":
                continue

            photo_info = get_date_taken(path_to_photo)

            if photo_info == "File Format Not Supported":
                unsupported_path = f"{external_hd_path}/unsupported"
                copy_file_to_path(path_to_photo, unsupported_path)
                continue
            else:
                # method = photo_info[0]
                date = photo_info[1]

            # Get date_taken when the file is still HEIC, after date_taken is got, convert to jpeg
            if photo_name.split(".")[1] == "HEIC":
                jpeg_photo_name = convert_heic_to_jpeg(path_to_photos, photo_name, testing=testing)
                photo_name = jpeg_photo_name
                path_to_photo = f"{path_to_photos}/{photo_name}"

            if date > start_date and image_before_end_on_date(date, end_on):
                year = date.strftime("%Y")
                month = date.strftime("%b")
                day = date.strftime("%d")
                new_path_to_photos = f"{external_hd_path}/{year}-transfer/{month}/{month}_{day}"

                copy_file_to_path(path_to_photo, new_path_to_photos)
                set_new_creation_date(f"{new_path_to_photos}/{photo_name}", date)
                set_new_modification_date(f"{new_path_to_photos}/{photo_name}", date)

                if is_lowest_date(lowest_date, date):
                    # Starter values are written into the csv file for tracking
                    starter_image = photo_name
                    starter_date = date
                    lowest_date = date

                if is_highest_date(highest_date, date):
                    # End values are written into the csv file for tracking
                    end_image = photo_name
                    end_date = date
                    highest_date = date

        # Every 333 photos, let user know it is still looping
        if count == 333:
            count = 0
            print("\nSearching photos...\n")

    try:
        csv_line = [starter_image, starter_date.strftime("%Y-%m-%d %H:%M:%S"), end_image, end_date.strftime("%Y-%m-%d %H:%M:%S")]
    except NameError:
        return "did not contain any supported files"
    
    return csv_line

                

                    



