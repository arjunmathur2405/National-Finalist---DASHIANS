import os
import shutil
from datetime import datetime
import sys

# Add the 'history' folder to the system path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../history/data')))

def save_history():
    # Get the current date and time for the directory name
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../history/data', f"backup_{timestamp}"))

    # Directories to create and their corresponding source directories
    directories = {
        "question_paper": "upload_item/question_paper",
        "answer_sheets": "upload_item/answer_sheet",
        "evaluated_sheets": "datasets/Evaluated",
    }

    # Create the base directory and subdirectories
    try:
        os.makedirs(base_dir, exist_ok=True)
        for sub_dir in directories.keys():
            os.makedirs(os.path.join(base_dir, sub_dir), exist_ok=True)
        print(f"Created directories under: {base_dir}")
    except Exception as e:
        print(f"Error creating directories: {e}")

    # Function to move files from source to destination
    def move_files(source, destination):
        try:
            files = os.listdir(source)
            for file_name in files:
                src_path = os.path.join(source, file_name)
                dst_path = os.path.join(destination, file_name)
                shutil.move(src_path, dst_path)
                print(f"Moved file: {src_path} to {dst_path}")
        except Exception as e:
            print(f"Error moving files from {source} to {destination}: {e}")

    # Move files for each directory
    move_files(directories["question_paper"], os.path.join(base_dir, "question_paper"))
    move_files(directories["answer_sheets"], os.path.join(base_dir, "answer_sheets"))

    # Move the files for evaluated_sheets
    try:
        eval_files_src = os.listdir(directories["evaluated_sheets"])
        for file_name in eval_files_src:
            src_path = os.path.join(directories["evaluated_sheets"], file_name)
            dst_path = os.path.join(base_dir, "evaluated_sheets", file_name)
            shutil.move(src_path, dst_path)
            print(f"Moved file: {src_path} to {dst_path}")
    except Exception as e:
        print(f"Error moving files from {directories['evaluated_sheets']} to {os.path.join(base_dir, 'evaluated_sheets')}: {e}")



