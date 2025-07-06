import os
import shutil
from datetime import datetime
import transfer_sd_to_hd.src.helpers as helpers

        
def image_before_end_on_date(end_on, image_path):
    if end_on == "":
        return True
    else:
        image_date = helpers.get_date_taken(image_path)
        image_date = datetime.strptime(image_date.split()[0], "%Y:%m:%d")
        end_on = datetime.strptime(end_on, "%Y:%m:%d")
        if image_date >= end_on:
            return False
        else:
            return True


def transfer_photos(start_dir, start_image, external_hd_path, include_day=True, end_on=""):
    """
        Transfers photos from an SD card directory to an external hard drive, organizing them by the month and year the photo was taken.

        The function starts at the specified directory and image, and continues transferring sequential images until it reaches a file that does not exist.
        Each photo is moved into a subdirectory on the external hard drive named after the month and year the photo was taken (e.g., "Jul-2025").
        If the end of a directory or image sequence is reached, it automatically shifts to the next directory or wraps around as needed.

        :param start_dir: The full path of the directory the start image is located in
        :type start_dir: string
        :param start_image: The file name of the start image
        :type start_image: string
        :param external_hd_path: The full path to the external hard drive the photos will be moved to
        :type external_hd_path: string
        :param include_day: Optional flag whether to organize photos into directory based off specific date and not month
        :type include_day: bool, Optional
        :param end_on: Date to end on (exclusive). SHould be in form of YYYY:MM:DD
        :type end_on: string
        :return: two values, the start directory and image for the next migration
        :rtype: string, string
    """

    current_dir = start_dir
    current_image = start_image
    current_path = f"{current_dir}/{current_image}"

    while os.path.exists(current_path) and image_before_end_on_date(end_on, current_path) :
        current_date = helpers.get_date_taken(current_path)
        pretty_date = helpers.convert_to_month_year(current_date, include_day)

        hd_pretty_date_path = f"{external_hd_path}/{pretty_date}"
        if not os.path.exists(hd_pretty_date_path):
            os.makedirs(hd_pretty_date_path)

        # Move the photo to the external hard drive
        print(f"Moving {current_path} to {hd_pretty_date_path}/{current_image}")
        shutil.copy(current_path, f"{hd_pretty_date_path}/{current_image}")

        current_image = helpers.image_shift_up(current_image)
        if current_image == "Hit Photo Limit":
            current_image = "IMG_0001.JPG"
            current_dir = helpers.directory_shift_up(current_dir)
        current_path = f"{current_dir}/{current_image}"

    return get_end_values(current_dir, current_image, current_date)