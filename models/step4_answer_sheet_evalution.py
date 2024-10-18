import pandas as pd
from concurrent.futures import ThreadPoolExecutor
import os
import sys
import openai  # Importing OpenAI's library for GPT-3.5
from dotenv import load_dotenv


# Loading environment variables
load_dotenv()
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')  # Use your OpenAI API key
openai.api_key = OPENAI_API_KEY  # Set the API key for OpenAI

# Add the directory containing the modules to the system path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

def answer_sheet_evaluation():
    global question_marks_index

    with open('current_user/question_paper_data.txt', 'r') as f:
        question_marks = f.read().split(',')

    def evaluate_answer(row):
        global question_marks_index
        question_marks_index += 1
        question = row['questions']
        student_answer = row['answers']

        # Prepare the prompt for GPT-3.5
        prompt = f"Evaluate the following answer: {student_answer}. based on this question {question}" \
                 f"Please provide the marks out of {question_marks[question_marks_index]} " \
                 f"(just write the number) and write remarks of 2-3 lines based on correctness, " \
                 f"completeness, length, and accuracy of the answer and weak points." \
                 f"Format your response as 'marks$remarks' without any extra text."

        # Call GPT-3.5 API
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        # Extract the marks and remarks from the response
        marks_obtain, remarks = response.choices[0].message['content'].split('$')

        return {
            'Question': question,
            'Student Answer': student_answer,

            'Mark Obtain': min(int(marks_obtain),int(question_marks[question_marks_index].strip())),
            'Out Of': max(int(marks_obtain),int(question_marks[question_marks_index].strip())),
            'Remarks': remarks.strip()
        }

    # Path to the Evaluated folder
    evaluated_folder_path = 'datasets/Evaluated/'
    os.makedirs(evaluated_folder_path, exist_ok=True)
    
    # List all CSV files in the datasets folder except the training file
    dataset_files = [f for f in os.listdir('datasets') if f.endswith('.csv') and f != 'english_dataset.txt']
    
    for file_name in dataset_files:
        question_marks_index = -1
        input_file_path = os.path.join('datasets', file_name)
        
        # Load the CSV file
        df = pd.read_csv(input_file_path)
        
        # Evaluate each row using ThreadPoolExecutor for parallel processing
        with ThreadPoolExecutor(max_workers=4) as executor:
            results = list(executor.map(evaluate_answer, [row for index, row in df.iterrows()]))
        
        # Create a new DataFrame with results
        results_df = pd.DataFrame(results)
        
        # Define the output file path for the evaluated results
        output_file_name = f"Evaluated_{file_name}"
        output_file_path = os.path.join(evaluated_folder_path, output_file_name)
        
        # Save the results to a CSV file
        results_df.to_csv(output_file_path, index=False)
        
        print(f"Evaluation results for '{file_name}' saved to '{output_file_path}'")


