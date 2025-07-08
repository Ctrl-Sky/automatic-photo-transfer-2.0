import os
import shutil
from datetime import datetime
from helpers import get_date_taken

        
def image_before_end_on_date(end_on, image_date):
    if end_on == "":
        return True
    else:
        end_on = datetime.strptime(end_on, "%Y:%m:%d")
        if image_date >= end_on:
            return False
        else:
            return True
        
def copy_file_to_path(file, path):
    if not os.path.exists(path):
        os.makedirs(path, exist_ok=True)
    print(f"Copying {file} to {path}...")
    shutil.copy(file, path)

def transfer_photos(start_date, external_hd_path, path_to_photos, end_on=""):
    counter = 0
    photos = [file for file in os.scandir(path_to_photos) if file.is_file()]
    photos.sort(key=lambda photo: photo.os.stat(path_to_photos).st_birthtime)
    
    for photo in photos:
        if photo.is_file():
            path_to_photo = f"{path_to_photos}/{photo}"
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

                if counter == 0:
                    starter_dir = path_to_photos
                    starter_image = photo
                    starter_date = date.strftime("%Y:%m:%d %H:%M:%S")
                    counter+=1

                end_dir = path_to_photo
                end_image = photo
                end_date = date.strftime("%Y:%m:%d %H:%M:%S")

    return [starter_dir, starter_image, starter_date, end_dir, end_image, end_date]

                

                    



