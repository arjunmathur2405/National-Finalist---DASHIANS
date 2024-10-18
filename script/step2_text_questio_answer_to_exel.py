import os
import pandas as pd
import sys
from dotenv import load_dotenv
import openai

# Load environment variables from .env file
load_dotenv()
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
openai.api_key = OPENAI_API_KEY

# Add the directory containing the modules to the system path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))


def chatgpt_generate(content, prompt):
    """Helper function to call OpenAI API for content generation"""
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are an assistant."},
            {"role": "user", "content": content + prompt}
        ]
    )
    return response['choices'][0]['message']['content']


def extract_questions_from_question_file():
    # File path for question.txt
    question_file_path = 'text_data/question.txt'
    
    # Read the content of the question file
    with open(question_file_path, 'r') as file:
        question_content = file.read()

    # Extract questions from the question file using ChatGPT
    questions = chatgpt_generate(
        question_content,
        "\n Extract the questions from this file and write them into python list form. don't write anything else not even question number. just write the list , don't assign it to a variable. write in such a way that i can use python function eval to convert this into a list directly"
    )
    questions = eval(questions)
    # Extract marks for each question using ChatGPT
    with open('current_user/question_paper_data.txt', 'w') as f:
        marks = chatgpt_generate(
            question_content,
            "Write the marks of each question comma separated. If marks are not given against the question, then take the value 3. Don't write anything else, just write the number."
        )
        f.write(marks)


    return questions


def process_answer_files(questions):
    # Path to the folder containing text files
    text_data_folder = 'text_data/'
    output_folder = 'datasets/'

    # List all files in the folder except question.txt
    files = [f for f in os.listdir(text_data_folder) if f.endswith('.txt') and f != 'question.txt']

    for file_name in files:
        answer_file_path = os.path.join(text_data_folder, file_name)
        output_file_path = os.path.join(output_folder, file_name.replace('.txt', '.csv'))

        # Read the content of the answer file
        with open(answer_file_path, 'r') as file:
            answer_content = file.read()

        # Extract answers from the answer file using ChatGPT
        answers = chatgpt_generate(
        answer_content,
        "\n Extract the Complete answers from this file and write them into python list form. don't write anything else. just write the list , don't assign it to a variable. write in such a way that i can use python function eval to convert this into a list directly.")

        answers = eval(answers)
        # Ensure both lists have the same length
        min_length = min(len(questions), len(answers))
        questions_truncated = questions[:min_length]
        answers = answers[:min_length]

        # Create a DataFrame to hold the questions and answers
        df = pd.DataFrame({
            'questions': questions_truncated,
            'answers': answers
        })

        # Save the DataFrame to a CSV file
        df.to_csv(output_file_path, index=False)

        print(f"Questions and answers extracted and saved to '{output_file_path}'")


def txt_to_excel():
    # Extract questions from question.txt
    questions = extract_questions_from_question_file()

    # Process all answer files using the extracted questions
    process_answer_files(questions)





