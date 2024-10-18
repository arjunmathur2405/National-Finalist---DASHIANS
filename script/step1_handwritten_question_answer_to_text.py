import os
import boto3
from datetime import datetime
import sys
import openai
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Loading OpenAI API Key
openai.api_key = os.getenv('OPENAI_API_KEY')

# AWS configuration
aws_access_key = os.getenv('AWS_ACCESS_KEY')
aws_secret_key = os.getenv('AWS_SECRET_KEY')
aws_region = os.getenv('AWS_REGION')

# Initialize Textract client
textract_client = boto3.client('textract',
                               aws_access_key_id=aws_access_key,
                               aws_secret_access_key=aws_secret_key,
                               region_name=aws_region)

# Add the 'history' folder to the system path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

# Paths
question_path = "upload_item/question_paper/"
answer_path = "upload_item/answer_sheet/"
text_data_path = "text_data/"

# Ensure text_data directory exists
os.makedirs(text_data_path, exist_ok=True)
subject = ""


def recognize_handwritten_text_question():
    global subject
    question_paper_path = question_path + os.listdir(question_path)[0]

    # Open the PDF file
    with open(question_paper_path, 'rb') as pdf_file:
        pdf_content = pdf_file.read()

    # Call AWS Textract to analyze the document
    response = textract_client.analyze_document(
        Document={'Bytes': pdf_content},
        FeatureTypes=['FORMS', 'TABLES']
    )

    # Extract the detected text
    text = ""
    for block in response['Blocks']:
        if block['BlockType'] == 'LINE':
            text += block['Text'] + "\n"

    # Save the text to a file
    with open('text_data/question.txt', 'w') as f:
        f.write(text)

    # Use ChatGPT API to get the subject name
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are an assistant."},
            {"role": "user", "content": text + "\n Write the Subject name only and nothing else."}
        ]
    )
    subject = response['choices'][0]['message']['content'].strip()


def recognize_handwritten_text_answer():
    # Process each file in the answer sheet folder
    for answer_file in os.listdir(answer_path):
        answer_sheet_path = os.path.join(answer_path, answer_file)

        # Open the PDF file
        with open(answer_sheet_path, 'rb') as pdf_file:
            pdf_content = pdf_file.read()

        # Call AWS Textract to analyze the document
        response = textract_client.analyze_document(
            Document={'Bytes': pdf_content},
            FeatureTypes=['FORMS', 'TABLES']
        )

        # Extract the detected text
        text = ""
        for block in response['Blocks']:
            if block['BlockType'] == 'LINE':
                text += block['Text'] + "\n"

        # Fetch the email ID from the text using ChatGPT API
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an assistant."},
                {"role": "user", "content": text + "\n Write student data only in comma separated form (first email id then student Id) and nothing else."}
            ]
        )
        email_id_and_student_id = response['choices'][0]['message']['content'].split(",")

        email_id_and_student_id = [i.strip() for i in email_id_and_student_id]

        if len(email_id_and_student_id) == 1:
            if ("@" not in email_id_and_student_id[0]):
                student_id = email_id_and_student_id[0]
                email_id = "priyanshuautocad@gmail.com"
            else:
                student_id = "stu_2"
                email_id = email_id_and_student_id[0]
            
        else:
            student_id = email_id_and_student_id[1]
            email_id = email_id_and_student_id[0]

        if len(email_id) < 5:
            email_id = "priyanshuautocad@gmail.com"

        # Create the filename using the email ID, subject (from the answer file name), and the current date
        date_str = datetime.now().strftime("%Y-%m-%d")
        filename = f"{student_id}_{email_id}_{subject}_{date_str}.txt"

        # Save the text to the file
        with open(os.path.join(text_data_path, filename), 'w') as f:
            f.write(text)
        print(f"Saved OCR result to {filename}")


