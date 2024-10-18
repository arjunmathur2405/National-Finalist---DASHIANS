import time
from flask import Flask, render_template, request, redirect, url_for, jsonify, flash
import os
import pandas as pd
import sys
import pdfkit
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import subprocess


app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Database configuration
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
db_folder = os.path.join(os.getcwd(), 'database')
if not os.path.exists(db_folder):
    os.makedirs(db_folder)
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(db_folder, "users.db")}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# User model
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    designation = db.Column(db.String(50), nullable=False)  # Designation field

# Create the database and tables
with app.app_context():
    db.create_all()

# Load user for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Allowed file extensions
ALLOWED_EXTENSIONS = {'pdf', 'jpg', 'jpeg', 'png', 'gif', 'txt'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def index():
    if current_user.is_authenticated:
        logout_user()
    return render_template('index.html')

# Signup Route
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        designation = request.form['designation']

        # Check if the user already exists
        if User.query.filter_by(username=username).first():
            flash('Username already exists. Please choose another.')
            return redirect(url_for('signup'))

        # Create new user and add to the database
        new_user = User(username=username, password=password, designation=designation)
        db.session.add(new_user)
        db.session.commit()

        flash('Signup successful! You can now log in.')
        return redirect(url_for('login'))

    return render_template('signup.html')

# Login Route
@app.route('/login', methods=['GET', 'POST'])
def login():
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Find the user in the database
        user = User.query.filter_by(username=username).first()

        if user and user.password == password:
            login_user(user)
            flash('Login successful!')

            # Save Current User Details in the current_user directory
            user_details = f"{current_user.username},{current_user.designation}\n"
            file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../current_user/'))
            filename = file_path + "/user_details.txt"

            with open(filename, 'w') as f:  # Append mode to add multiple entries
                f.write(user_details)

        
            # Redirect based on user designation
            if user.designation == 'teacher':
                return redirect(url_for('teacher_dashboard'))
            elif user.designation == 'student':
                return redirect(url_for('student_dashboard'))
            else:
                return redirect(url_for('portal'))
        else:
            flash('Invalid username or password')

    return render_template('login.html')

# Logout Route
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('index'))

# Student Panel
@app.route('/student_dashboard')
@login_required
def student_dashboard():
    return render_template('student_dashboard.html')

@app.route('/student_result_history')
@login_required
def student_result_history():
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
    excel_file_path = os.path.join('history', 'history_summary.xlsx')
    df = pd.read_excel(excel_file_path)

    # Assuming 'current_user.username' is the username of the logged-in user
    current_username = str(current_user.username)  # Adjust if needed
    # Filter the DataFrame for the current user's username
    user_results = df[df['Student_id'] == current_username]

    results = user_results.to_dict(orient='records')
    return render_template('student_result_history.html',results=results)

@app.route('/view_result_details')
@login_required
def view_result_details():
    return None


# Teacher Dashboard
@app.route('/teacher_dashboard')
@login_required
def teacher_dashboard():
    return render_template('teacher_dashboard.html')


@app.route('/teacher_panel')
@login_required
def teacher_panel():
    return render_template('teacher_panel.html')


@app.route('/teacher_results')
@login_required
def teacher_results():
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
    excel_file_path = os.path.join('history', 'history_summary.xlsx')
    df = pd.read_excel(excel_file_path)

    # Assuming 'current_user.username' is the username of the logged-in user
    current_username = current_user.username  # Adjust if needed

    # Filter the DataFrame for the current user's username
    user_results = df[df['Teacher_id'] == current_username]

    results = user_results.to_dict(orient='records')
    return render_template('teacher_results.html', results=results)



# File upload routes
@app.route('/upload', methods=['POST'])
@login_required
def upload_answer_sheets():
    if 'answer-sheets[]' not in request.files:
        return jsonify(success=False, message="No file part"), 400
    
    files = request.files.getlist('answer-sheets[]')
    
    if not files:
        return jsonify(success=False, message="No selected files"), 400
    
    upload_folder = app.config.get('UPLOAD_FOLDER_ANSWER_SHEETS', 'upload_item/answer_sheet/')
    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)
    for file in files:
        if file.filename == '':
            return jsonify(success=False, message="One or more files are missing a filename"), 400
        
        if not allowed_file(file.filename):
            return jsonify(success=False, message=f"File type not allowed: {file.filename}"), 400
        
        filename = f"{int(time.time())}_{file.filename}"
        file_path = os.path.join(upload_folder, filename)
        
        try:
            file.save(file_path)
        except Exception as e:
            return jsonify(success=False, message=f"Error saving file {filename}: {str(e)}"), 500
    
    return jsonify(success=True, message="Files successfully uploaded!")

@app.route('/upload-question-paper', methods=['POST'])
@login_required
def upload_question_paper():
    if 'question-paper' not in request.files:
        return jsonify(success=False, message="No file part"), 400
    
    file = request.files['question-paper']
    
    if file.filename == '':
        return jsonify(success=False, message="No selected file"), 400
        
    if not allowed_file(file.filename):
        return jsonify(success=False, message=f"File type not allowed: {file.filename}"), 400
        
    filename = f"{int(time.time())}_{file.filename}"
    upload_folder = app.config.get('UPLOAD_FOLDER_QUESTION_PAPER', 'upload_item/question_paper/')
    
    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)
    
    file_path = os.path.join(upload_folder, filename)
    
    try:
        file.save(file_path)
    except Exception as e:
        return jsonify(success=False, message=f"Error saving file {filename}: {str(e)}"), 500
    
    return jsonify(success=True, message="Question paper successfully uploaded!")

# PDF generation routes
@app.route('/generate-report')
@login_required
def generate_report():
    csv_file = request.args.get('report_path')
    if not os.path.exists(csv_file):
        return render_template('report.html', data=[], total_marks_obtained=0, total_marks=0, percentage=0, comments="No data available.")

    df = pd.read_csv(csv_file)
    total_marks_obtained = df['Mark Obtain'].sum()
    total_marks = 20
    percentage = (total_marks_obtained / total_marks) * 100 if total_marks > 0 else 0
    comments = "Your performance is good overall but there are some areas that need improvement."

    return render_template('report.html', data=df.to_dict(orient='records'), total_marks_obtained=total_marks_obtained, total_marks=total_marks, percentage=percentage, comments=comments)


@app.route('/generate-pdf')
@login_required
def generate_pdf():
    csv_file = request.args.get('csv_path')
    
    if not csv_file or not os.path.exists(csv_file):
        return "CSV file path is invalid or not provided", 400

    filename = os.path.basename(csv_file)

    df = pd.read_csv(csv_file)
    total_marks_obtained = df['Mark Obtain'].sum()
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
    with open('current_user/question_paper_data.txt','r') as f:
        total_marks = sum([int(i.strip()) for i in f.read().split(',')])

    percentage = (total_marks_obtained / total_marks) * 100 if total_marks > 0 else 0
    comments = "Your performance is good overall but there are some areas that need improvement."

    rendered_html = render_template('report.html', data=df.to_dict(orient='records'),
                                    total_marks_obtained=total_marks_obtained,
                                    total_marks=total_marks,
                                    percentage=percentage,
                                    comments=comments)

    pdf_filename = f"{filename.replace('.csv', '.pdf')}"
    pdf_path = os.path.join('datasets/Evaluated', pdf_filename)
    pdfkit.from_string(rendered_html, pdf_path)

    return f"PDF saved at {pdf_path}", 200


@app.route('/start-checking-sheets', methods=['POST','GET'])
@login_required
def start_checking_sheets():
    
    if request.method == 'POST':
        # Path to the main.py script outside the UI folder
        script_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'main', 'main.py')

        try:
            # Run the script and capture output
            result = subprocess.run(['python3', script_path], capture_output=True, text=True, check=True)
            print(result.stdout)  # For debugging purposes
        except subprocess.CalledProcessError as e:
            print(f"Script execution failed: {e.stderr}")  # Log the error output
            return jsonify(success=False, message="An Error Occurred"), 500
        return jsonify(success=True, message="Successfully Evaluated Answer Sheets")


if __name__ == '__main__':
    app.run(debug=True,port=5000)
