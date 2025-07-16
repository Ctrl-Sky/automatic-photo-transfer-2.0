import os
import shutil
from datetime import datetime
from helpers import get_date_taken

def is_lowest_date(lowest_date, image_date):
    if image_date < lowest_date:
        return True
    else:
        return False
        
def image_before_end_on_date(image_date, end_on):
    if end_on == "":
        return True
    else:
        end_on = datetime.strptime(end_on, "%Y:%m:%d")
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
    lowest_date = start_date

    for photo in os.scandir(path_to_photos):
        if photo.is_file():
            photo_name = photo.name
            path_to_photo = f"{path_to_photos}/{photo_name}"
            photo_info = get_date_taken(path_to_photo)

            if photo_info == "File Format Not Supported":
                copy_file_to_path(path_to_photo, f"{external_hd_path}/unsupported")
                continue
            else:
                method = photo_info[0]
                date = photo_info[1]

            if date > start_date and image_before_end_on_date(date, end_on):
                year = date.strftime("%Y")
                month = date.strftime("%b")
                day = date.strftime("%d")
                new_path_to_photos = f"{external_hd_path}/{year}-transfer/{month}/{month}_{day}-{method}"

                copy_file_to_path(path_to_photo, new_path_to_photos)
                
                # Write these values into csv table
                if is_lowest_date(lowest_date, date):
                    starter_dir = path_to_photos
                    starter_image = photo_name
                    starter_date = date
                    lowest_date = date

                end_dir = path_to_photo
                end_image = photo_name
                end_date = date

    return [starter_dir, starter_image, starter_date.strftime("%Y:%m:%d %H:%M:%S"), end_dir, end_image, end_date.strftime("%Y:%m:%d %H:%M:%S")]

                

                    



