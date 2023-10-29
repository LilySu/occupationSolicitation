import glob
import os

import docx2txt

# Specify the folder where your .docx files are located
folder_path = "../my_resumes"

# List all .docx files in the folder
docx_files = glob.glob(os.path.join(folder_path, "*.docx"))

# Find the most recent .docx file
if docx_files:
    most_recent_file = max(docx_files, key=os.path.getctime)
    print(f"Processing the most recent file: {most_recent_file}")

    # Replace 'output.txt' with the path where you want to save the .txt file
    output_txt_path = "output.txt"

    try:
        # Extract text from the most recent .docx file and save it to a .txt file
        text = docx2txt.process(most_recent_file, output_txt_path)
        print(f'Text from "{most_recent_file}" has been saved to "{output_txt_path}".')

    except Exception as e:
        print(f"An error occurred: {str(e)}")

else:
    print("No .docx files found in the specified folder.")
