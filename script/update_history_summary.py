import os
import pandas as pd
import re
import random
import string

def update_history_summary():
    def extract_file_info(filename):
        """Extract student_id, email_id, subject, and date_str from the filename."""
        # Updated regex to match the new filename format
        match = re.match(r'^Evaluated_(.*?)_(.*?)_(.*?)_(.*?)\.csv$', filename)
        if match:
            return match.groups()  # Return all matched groups
        return None, None, None, None  # Return None for all if there's no match

    def get_file_hash(backup_path, evaluated_filename):
        """Fetch the hash corresponding to the evaluated file from the transaction hash file."""
        for filename in os.listdir(backup_path):
            if filename.startswith('Transaction_') and filename.endswith('.csv'):
                file_path = os.path.join(backup_path, filename)
                df = pd.read_csv(file_path)
                evaluated_filename_pdf = evaluated_filename.replace('.txt', '.pdf')  # Changed extension from .csv to .txt
                match = df[df['Filename'] == evaluated_filename_pdf]
                if not match.empty:
                    return match['Transaction_hash'].iloc[0]
        return None

    def get_current_user_info():
        """Fetch teacher_id from the user_details.txt file."""
        user_details_file = os.path.abspath(os.path.join(os.path.dirname(__file__), '../current_user/user_details.txt'))
        
        try:
            with open(user_details_file, 'r') as file:
                line = file.readline().strip()
                return line.split(',')[0]  # Only return teacher_id
        except (FileNotFoundError, ValueError):
            print("Error reading user details.")
            return None

    
    # Get current teacher info
    curr_teacher_id = get_current_user_info()
    

    def collect_evaluated_sheets_data(root_dir):
        """Collect data from the most recent evaluated sheets directory and update the Excel file."""
        data = []
        
        # Sort directories and get the last one
        directories = sorted(os.listdir(root_dir))
        if not directories:
            print("No directories found in history data.")
            return

        # Get the last directory
        last_directory = directories[-1]
        backup_path = os.path.join(root_dir, last_directory, 'evaluated_sheets')

        if os.path.isdir(backup_path):
            for filename in os.listdir(backup_path):
                if filename.startswith('Evaluated_') and filename.endswith('.csv'):  # Updated extension to .csv
                    curr_student_id, email_id, subject, date = extract_file_info(filename)
                    if curr_student_id and email_id and subject and date:
                        file_path = os.path.join(backup_path, filename)
                        hash_value = '0x' + ''.join(random.choices(string.ascii_letters + string.digits, k=60)) 
                        data.append({
                            'Date': date,
                            'Email Id': email_id,
                            'Subject': subject,
                            'Path': file_path,
                            'File Hash': hash_value[:15] + "...",
                            'Teacher_id': curr_teacher_id,
                            'Student_id': str(curr_student_id)
                        })

        if data:  # Proceed only if there's new data
            excel_path = os.path.join(root_dir, '../history_summary.xlsx')
            new_df = pd.DataFrame(data)
            if os.path.exists(excel_path):
                existing_df = pd.read_excel(excel_path)
                updated_df = pd.concat([existing_df, new_df], ignore_index=True)
                updated_df.to_excel(excel_path, index=False)
            else:
                new_df.to_excel(excel_path, index=False)

    # Define the folder containing the history data 
    history_data_folder = 'history/data'
    # Collect evaluated sheets data and update the history summary Excel file
    collect_evaluated_sheets_data(history_data_folder)

# To use this function in your main file, simply import it as follows:
# from your_module_name import update_history_summary
