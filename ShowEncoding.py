import os
import ftplib
import datetime
import subprocess
import time

# Get today's date
today2 = datetime.date.today()

# Subtract one day to get yesterday's date
yesterday = today2 - datetime.timedelta(days=1)

# Format the date as a string in the format 'YYYYMMDD'
day3 = yesterday.strftime('%Y%m%d')
#day2=datetime.date.today().strftime('%Y%m%d')
print(day3)
#sleep for 59 minutes to make sure record is done
#time.sleep(3540)
# FTP connection details
server_ip = "10.33.97.2"
port = 21
username = "user"
password = "user"

day2=datetime.date.today().strftime('%Y%m%d')
# Local folders
download_folder = "E:\\PReNewsCast"
#encode_folder = "E:\\NewsEncode"
encode_folder = "F:\\Shows"

# File patterns for Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, and Sunday
monday_files = ["WHSV5A1MON.mxf", "WHSV5A2MON.mxf", "12PMMON.mxf", "WHSV11PMON.mxf", "WHSV6PMON.mxf", "5PMMON.mxf", "FOXNEWSMON.mxf"]
tuesday_files = ["WHSV5A1TUE.mxf", "WHSV5A2TUE.mxf", "12PMTHU.mxf", "WHSV11PTUE.mxf", "WHSV6PTUE.mxf", "5PMTUE.mxf", "FOXNEWSTUE.mxf"]
wednesday_files = ["WHSV5A1WED.mxf", "WHSV5A2WED.mxf", "12PMWED.mxf", "WHSV11PWED.mxf", "WHSV6PWED.mxf", "5PMWED.mxf", "FOXNEWSWED.mxf"]
thursday_files = ["WHSV5A1THU.mxf", "WHSV5A2THU.mxf", "12PMTHU.mxf", "WHSV11PTHU.mxf", "WHSV6PTHU.mxf", "5PMTHU.mxf", "FOXNEWSTHU.mxf"]
friday_files = ["WHSV5A1FRI.mxf", "WHSV5A2FRI.mxf", "12PMFRI.mxf", "WHSV11PFRI.mxf", "WHSV6PFRI.mxf", "5PMFRI.mxf", "FOXNEWSFRI.mxf"]
saturday_files = ["WHSV6P1WE.mxf", "WHSV11P1WE.mxf","WHSV6P2WE.mxf", "WHSV11P2WE.mxf"]
sunday_files = ["WHSV6P2WE.mxf", "WHSV11P2WE.mxf"]
#sunday_files = ["1300mxf"]

# Function to download files from FTP
# Function to download files from FTP


def download_files(ftp, files, pancakes,days3):
    #global day2
    os.chdir("E:\\PReNewsCast")
    downloaded_files = []
    for file in files:
        ftp.cwd("/fs0/clip.dir")  # Change directory to the specified folder
        local_filename = os.path.join(download_folder, file)
        try:
            ftp.retrbinary("RETR " + file, open(local_filename, 'wb').write)
            downloaded_files.append(file)
            print(f"Downloaded: {file}")
        except Exception as e:
            print(f"Error downloading {file}: {e}")

    # Rename downloaded files based on their original download start time
    print("the downloaded_files list", downloaded_files)
    for file in downloaded_files:
        base_name, ext = os.path.splitext(file)
        #new_filename = os.path.join(download_folder, f"{base_name}_{datetime.date.today().strftime('%Y%m%d')}{ext}")
        new_filename = os.path.join(download_folder, f"{base_name}_{day3}{ext}")
        try:
            print("file name ",file, "new_filename ", new_filename)
            os.rename(file, new_filename)
            #os.rename(local_filename, new_filename)
            print(f"Renamed: {file}")
        except Exception as e:
            print(f"Error renaming {file}: {e}")
'''
    # Rename downloaded files based on their original download start time
    for file in downloaded_files:
		#global day2
        global day2
        base_name, ext = os.path.splitext(file)
        #new_filename = os.path.join(download_folder, f"{base_name}_{datetime.date.today().strftime('%Y%m%d')}{ext}")
        new_filename = os.path.join(download_folder, f"{base_name}_{day2}{ext}")
        os.rename(local_filename, new_filename)
'''

# Function to encode files using ffmpeg
# Function to encode files using ffmpeg
def encode_files(files):
    os.chdir(download_folder)  # Change working directory to download_folder
    for file in files:
        if not os.path.exists(file):
            print(f"Error: File {file} not found.")
            continue
        output_file = os.path.join(encode_folder, os.path.basename(file).replace('.mxf', '.mp4'))
        ffmpeg_cmd = f"ffmpeg -i {file} -preset veryfast -codec:a aac -b:a 128k -codec:v libx264 -pix_fmt yuv420p -b:v 8000k -minrate 1500k -maxrate 4000k -bufsize 5000k -vf scale=-1:720 {output_file}"
        subprocess.run(ffmpeg_cmd, shell=True)
        # Remove original MXF file
        os.remove(file)
# Main function
def main():
    # Debugging information
    print("Starting the main function")

    try:
        # Debugging FTP connection
        print("Connecting to FTP server...")
        ftp = ftplib.FTP(server_ip, username, password)
        print("Successfully connected to the FTP server.")
        ftp.cwd("/")
        print("Changed directory to root.")

        # Check current day and download appropriate files
        today1 = datetime.date.today()
        print(f"Today's date: {today1}")

        today = today1 - datetime.timedelta(days=1)
        print(f"Date for processing (yesterday): {today}")

        # Determine the day of the week
        # Calculate the previous day
        previous_day = today - datetime.timedelta(days=0)

# Determine the weekday of the previous day
        weekday = previous_day.weekday()
        print(f"Weekday index (0=Monday, 6=Sunday): {weekday}")

        if weekday == 0:  # Monday
            print("Processing files for Monday...")
            download_files(ftp, monday_files, "Monday",day3)
        elif weekday == 1:  # Tuesday
            print("Processing files for Tuesday...")
            download_files(ftp, tuesday_files, "Tuesday",day3)
        elif weekday == 2:  # Wednesday
            print("Processing files for Wednesday...")
            download_files(ftp, wednesday_files, "Wednesday",day3)
        elif weekday == 3:  # Thursday
            print("Processing files for Thursday...")
            download_files(ftp, thursday_files, "Thursday",day3)
        elif weekday == 4:  # Friday
            print("Processing files for Friday...")
            download_files(ftp, friday_files, "Friday",day3)
        elif weekday == 5:  # Saturday
            print("Processing files for Saturday...")
            download_files(ftp, saturday_files, "Saturday",day3)
        elif weekday == 6:  # Sunday
            print("Processing files for Sunday...")
            download_files(ftp, sunday_files, "Sunday",day3)
        else:
            print("It's not a valid weekday. No files downloaded.")

        # Debugging encoding of files
        print("Listing files in the download folder...")
        files_to_encode = [f for f in os.listdir(download_folder) if f.endswith('.mxf')]
        print(f"Files to encode: {files_to_encode}")

        encode_files(files_to_encode)
        print("Files have been encoded.")

    except Exception as e:
        print(f"Error: {e}")

    finally:
        if ftp:
            ftp.quit()

if __name__ == "__main__":
    main()
