'''
import pandas as pd
import os
import sys
import google.generativeai as genai
from dotenv import load_dotenv


load_dotenv()
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
model = genai.GenerativeModel("gemini-1.5-flash")


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

def answer_generator():
    # File paths
    predicted_folder_path = "datasets/Predicted/"
    
    # Create the Predicted directory if it doesn't exist
    os.makedirs(predicted_folder_path, exist_ok=True)

    
    # List all files in the datasets folder except the training file
    dataset_files = [f for f in os.listdir('datasets') if f.endswith('.csv') and f != 'english_dataset.txt']
    
    # Ensure there is at least one file to process
    if not dataset_files:
        print("No dataset files found for evaluation.")
        return
    
    # Use only the first file in the list
    file_name = dataset_files[0]
    student_file_path = os.path.join('datasets', file_name)
    output_file_path = os.path.join(predicted_folder_path, file_name)
    
    # Load the student written questions and answers
    use_columns = ['questions']
    student_df = pd.read_csv(student_file_path , usecols=use_columns)
    student_df['questions'].fillna('', inplace=True)
    
    

    # Function to predict an answer for a new question
    def predict_answer(question):
        return model.generate_content
        # return model.predict([question])[0]
    
    # Add a new column for model predicted answers
    student_df['model_predicted_answers'] = student_df['questions'].apply(predict_answer)
    
    # Save the updated DataFrame to a CSV file
    student_df.to_csv(output_file_path, index=False)
    print(f"Student questions with model answers saved to '{output_file_path}'")

'''