import re
import os
from PIL import Image
import pytesseract

# Set the Tesseract OCR executable file pathway
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def extract_info_from_image(img_path):
    try:
        # Open image using PIL
        with Image.open(img_path) as img:
            # Use pytesseract to extract text from the image
            text = pytesseract.image_to_string(img)
            
            # Search for a six-digit number
            six_digit_number = re.search(r'(\b\d{6}\b)', text)
            six_digit_number = six_digit_number.group(1) if six_digit_number else None
            
            # Search for a date in the format MM/DD/YYYY, MM-DD-YYYY, etc.
            date_pattern = re.search(r'(\d{1,2}[\/\-]\d{1,2}[\/\-]\d{4})', text)
            date = date_pattern.group(1).replace('/', '.').replace('-', '.').replace(' ', '') if date_pattern else None

            return six_digit_number, date
    except Exception as e:
        print(f"Error processing {img_path}: {e}")
        return None, None

def process_files_in_directory(directory):
    for filename in os.listdir(directory):
        # Check if the file has the required extension
        if filename.endswith((".pdf", ".jpeg", ".png")):
            filepath = os.path.join(directory, filename)
            
            six_digit_number, date = extract_info_from_image(filepath)
            
            # If both the six-digit number and date are found, rename the file
            if six_digit_number and date:
                new_filename = six_digit_number + '_' + date + os.path.splitext(filename)[1]
                new_filepath = os.path.join(directory, new_filename)
                os.rename(filepath, new_filepath)
                print(f'Renamed {filename} to {new_filename}')
            else:
                print(f'Could not find required info in {filename}')

if __name__ == '__main__':
    # Process all files in the current directory
    process_files_in_directory('.')
