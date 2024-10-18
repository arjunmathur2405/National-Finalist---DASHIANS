import os
import sys
import glob
import shutil  # For removing directories

# Add the directory containing the modules to the system path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

# List of files to remove, except the specified file
files_to_remove = [
    "text_data/question.txt",
]

# Directory to clean but preserve a specific file
datasets_directory = "datasets"
file_to_preserve = "english_dataset.txt"

# Directories to clean, including the correct comma in the list
directories_to_clean = [
    "upload_item/answer_sheet",
    "upload_item/question_paper",
    "text_data",
]

def clean_files():
    # Remove specified files
    for file_path in files_to_remove:
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
                print(f"Removed file: {file_path}")
            else:
                print(f"File not found: {file_path}")
        except Exception as e:
            print(f"Error removing file {file_path}: {e}")

    # Remove all files and directories in the datasets directory except the file to preserve
    try:
        for item in os.listdir(datasets_directory):
            item_path = os.path.join(datasets_directory, item)
            if os.path.isfile(item_path):
                if os.path.basename(item_path) != file_to_preserve:
                    os.remove(item_path)
                    print(f"Removed file: {item_path}")
            elif os.path.isdir(item_path):
                shutil.rmtree(item_path)
                print(f"Removed directory: {item_path}")
        print(f"Cleaned directory (except {file_to_preserve}): {datasets_directory}")
    except Exception as e:
        print(f"Error cleaning directory {datasets_directory}: {e}")

def clean_directories():
    for directory in directories_to_clean:
        try:
            # Get a list of all files in the directory
            files = glob.glob(os.path.join(directory, '*'))
            for file_path in files:
                if os.path.isfile(file_path):
                    os.remove(file_path)
                    print(f"Removed file: {file_path}")
            print(f"Cleaned directory: {directory}")
        except Exception as e:
            print(f"Error cleaning directory {directory}: {e}")
