# What This App Does
This app is an automated standardization pipeline for transfering photos from one folder to another, keeping track of each migration in a CSV file. 

My main purpose for this is to automate the process of moving photos from my SD card/Iphone into my external hard drive and organizing them. So I just need to plug in my destination and source and then give the application a run. It copies every photo from the source directory into the destination directory, organizing each into folders based on the date they were taken. Out of all the photos, it will note down the photo that was taken the most recently and write that date into the csv file. This will act as a save point. Now if I have to run it again, it will pull that date from the csv file, and only upload the photos that were taken after said date. 

In the `build_config.yaml` file, you will find the parameters needed for this application:
- device
- path-to-photos
- destination-path
- migration-name (optional)
- end-on (optional)

The device parameter will decide which table the app will write to. Currently, I have a `phone` and a `camera` option which will write and read from their respective tables. This is done to avoid any mix ups.

The migration name is purely for user experience and will fill out one column in the CSV file. Is used to title specific migrations. It will default to (date_of_oldest_photo_taken)-(date_of_newest_photo_taken)

The `end-on`option takes a date value and acts as an optional stopping point for the application. Say you don't want to copy every photo and want to stop at a certain date, enter that date in the `end-on` option

The current supported file types are:
- JPEG
- JPG
- PNG
- HEIC
- MP4
- MOV

Any unknown files encountered during the migration will be transfered to the source directory within a folder known as `unsupported`, where it will need to be manually sorted. Will also convert HEIC files into jpeg files. Will not save edits made to photos.

# Reccomended Use
Run this in photo batches based on timezones. So run the application for all your photos taken in Hong Kong and then run it again on
al your photos taken in Toronto. This is done to avoid timezone errors. Make sure the inputted timezone value in `build_config.yaml`
matches the system timezone

# How to use
- Fill in the parameters in the `build_config.yaml`
- Remember to alter the CSV table for any timezone changes
- Run `bash execute_application.sh` in the terminal

# Things to note
- Sending photos over instagram will scrub the metadata(exif) and return it as a JPG
- Sending photos from apple phone over Imessage will keep file format and metatdata
- Getting sent a video (.MOV), on a date different from the orginial date taken, will not mess up birthtime value. It will still return the orginial date taken.
- Live photos create a HEIC and a MOV file, I don't want the MOV file so as a bandaid fix for skipping live photos, so any MOV file that is less than 3 seconds will be skipped.
