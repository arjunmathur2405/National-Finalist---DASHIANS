import os
import requests
import sys
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

def send_report():
    # Add the directory containing the modules to the system path
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

    # Read API key and domain from environment variables
    api_key = os.getenv('EMAIL_API_KEY')
    domain = os.getenv('EMAIL_DOMAIN_KEY')

    # Path to the Evaluated folder
    evaluated_folder = 'datasets/Evaluated'
    sender_email = "v67904413@gmail.com"  # Replace with your sender email

    # Traverse the Evaluated folder and process each CSV file that starts with "Evaluated"
    for filename in os.listdir(evaluated_folder):
        if not filename.startswith('Evaluated') or not filename.endswith('.csv'):
            continue  # Skip files that don't start with "Evaluated" or are not CSV files

        # Extract components from the filename
        parts = filename.split('_')
        if parts[1].count('.') > 1:
            email_id = parts[1][:-1]
        else:
            email_id = parts[1]
        subject = parts[2]
        date_str = parts[3].split('.')[0]

        # Ensure it's a valid email format
        if not email_id or '@' not in email_id:
            print(f'Skipping file {filename}: Invalid email ID extracted.')
            continue

        # Call the Flask function to generate the PDF
        csv_path = os.path.join(evaluated_folder, filename)
        response = requests.get(f"http://localhost:5000/generate-pdf?csv_path={csv_path}")

        if response.status_code != 200:
            print(f"Failed to generate PDF for {filename}: {response.text}")
            continue

        # PDF file name will be the same as the CSV file but with a .pdf extension
        pdf_filename = filename.replace('.csv', '.pdf')
        pdf_path = os.path.join(evaluated_folder, pdf_filename)

        # Prepare the email details
        email_subject = f"Result of Your {subject} Exam on {datetime.strptime(date_str, '%Y-%m-%d').strftime('%d %B %Y')}"
        body = f"Dear {email_id},\n\nPlease find your evaluated answer sheet for the {subject} exam held on {datetime.strptime(date_str, '%Y-%m-%d').strftime('%d %B %Y')} attached.\n\nBest regards,\nD.A.S.H"

        # Send the email with the PDF attachment
        response = requests.post(
            f"https://api.mailgun.net/v3/{domain}/messages",
            auth=("api", api_key),
            files={"attachment": open(pdf_path, "rb")},
            data={"from": sender_email,
                  "to": email_id,
                  "subject": email_subject,
                  "text": body}
        )

        # Print the detailed response for debugging
        print(f'Sending email to {email_id}')
        print(f'Status code: {response.status_code}')
        print(f'Response headers: {response.headers}')
        print(f'Response body: {response.text}')

