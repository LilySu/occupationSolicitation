import glob
import os
from datetime import datetime

import docx2txt

# Specify the folder where your .docx files are located
folder_path = "../my_resumes"

# List all .docx files in the folder
docx_files = glob.glob(os.path.join(folder_path, "*.docx"))

# Find the most recent .docx file
if docx_files:
    most_recent_file = max(docx_files, key=os.path.getctime)
    print(f"Processing the most recent file: {most_recent_file}")

    # Get today's date
    today = datetime.now()

    # Format the date as "YYYY-MM-DD"
    formatted_date = today.strftime("%Y-%m-%d")

    # Specify the full path including the filename for the output .txt file
    output_txt_path = os.path.normpath(
        os.path.join(folder_path, f"{formatted_date}_my_latest_resume.txt")
    )

    try:
        # Extract text from the most recent .docx file and save it to the specified .txt file
        text = docx2txt.process(most_recent_file, output_txt_path)
        # print(text)

        # Save the extracted text to the specified .txt file
        with open(output_txt_path, "w", encoding="utf-8") as txt_file:
            txt_file.write(text)

            print(
                f'Text from "{most_recent_file}" has been saved to "{output_txt_path}".'
            )

    except Exception as e:
        print(f"An error occurred: {str(e)}")

else:
    print("No .docx files found in the specified folder.")
