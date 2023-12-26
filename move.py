import os
import shutil
from datetime import datetime, timezone
import pytz

def backup_files(source_folder, destination_folder):
    # Create a backup folder with the current date
    os.makedirs(destination_folder, exist_ok=True)

    # List of files to back up
    files_to_backup = ["keeper.txt", "main.txt", "match_summary.txt", "shots.txt", "teamdefence.txt","teamdefencefooter.txt","teammisc.txt","teammiscfooter.txt","teampassing.txt","teampassingfooter.txt","teampasstype.txt","teamsummary_footer.txt","teampasstypefooter.txt","teamposession.txt","teamposessionfooter.txt","teamsummary.txt"]

    for filename in files_to_backup:
        source_file_path = os.path.join(source_folder, filename)
        if os.path.exists(source_file_path):
            # Create the backup file name
            move_file_path = os.path.join(destination_folder, filename)
            # Copy the file to the backup folder
            shutil.copy(source_file_path, move_file_path)
            print(f"file {filename} have moved to {destination_folder} ")

        else:
            print(f"File {filename} does not exist in the source folder.")
    
# Example usage
source_folder_path = "C:/Users/User/Desktop/Code/scraping/data/"
destination_folder_path = "//192.168.0.3/Public/Data/RawData/FBREF_v2/"
backup_files(source_folder_path, destination_folder_path)