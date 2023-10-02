import os
import shutil
import re
from datetime import datetime

def extract_date_from_filename(filename):
    # Attempt to match MM.DD.YYYY, MM-DD-YYYY, etc.
    date_pattern = re.search(r'(\d{1,2}[.\-]\d{1,2}[.\-]\d{4})', filename)
    if date_pattern:
        date_str = date_pattern.group(1).replace('.', '-')
        try:
            return datetime.strptime(date_str, "%m-%d-%Y")
        except ValueError:
            print(f"Error parsing date from {filename}. Skipping.")
            return None
    return None

def move_files_based_on_filename(directory):
    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)

        # Check if it's a file and has the required extension
        if os.path.isfile(filepath) and filename.endswith(('.jpeg', '.png', '.pdf')):
            file_date = extract_date_from_filename(filename)
            
            if file_date:
                # Define the folder name based on the date in the filename
                folder_name = file_date.strftime("%B-%Y")  # Format: Month-Year
                folder_path = os.path.join(directory, folder_name)

                # Create the folder if it doesn't exist
                if not os.path.exists(folder_path):
                    os.makedirs(folder_path)

                # Move the file to the appropriate folder
                shutil.move(filepath, os.path.join(folder_path, filename))
                print(f"Moved {filename} to {folder_name}")

if __name__ == '__main__':
    # Process all files in the current directory
    move_files_based_on_filename('.')
    
