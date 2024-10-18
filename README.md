# Answer Sheet Checker Platform

This project is a secure, web-based platform that allows teachers to upload and evaluate answer sheets, while providing students with access to their evaluated sheets. To ensure the integrity of these evaluations, blockchain technology is integrated, which prevents tampering and guarantees that once an answer sheet is evaluated, it remains unchanged.

## Key Features

### 1. **Student Dashboard**
- Students can log in to view their evaluated answer sheets.
- Answer sheets are stored securely and can be accessed anytime.
  
### 2. **Teacher Dashboard**
- Teachers can upload answer sheets in PDF or image format (images are automatically converted to PDFs).
- Built-in tools allow teachers to evaluate sheets online.
- After evaluation, a hash is generated and stored on the blockchain to ensure data integrity.

### 3. **Blockchain Security**
- Each evaluated answer sheet generates a unique hash using the SHA-256 algorithm.
- This hash is stored on the blockchain using smart contracts, ensuring that any tampering with the answer sheet is easily detectable.
- The blockchain integration uses **Alchemy** and **Rairtech** for secure hash storage.

### 4. **Backup and Recovery**
- The platform provides automatic backups of all evaluated answer sheets.
- Backups ensure that even in the event of data loss, the sheets are recoverable.

### 5. **Plans for Users**
- Free and paid plans are available for students and teachers, offering varying levels of access and features.
- Free plan users can upload and access sheets but have limited storage and features.
- Paid plan users have access to enhanced features, additional storage, and priority support.

### 6. **Admin Control Panel**
- Admins can manage user accounts, monitor system performance, and view blockchain transaction logs.
- Full control over adding, editing, and removing teachers and students.
  
## Technology Stack

The platform is built using modern web technologies and blockchain tools:

- **Backend**: Flask (Python-based web framework)
- **Blockchain**: 
  - **Web3** for interacting with Ethereum-based blockchains.
  - **Alchemy** for blockchain infrastructure and managing transactions.
  - **Rairtech** for storing answer sheet hashes securely on the blockchain.
- **AWS Textract**: Used for extracting text from uploaded PDFs and images.
- **Frontend**: HTML5, CSS3, and JavaScript for responsive and dynamic interfaces.
- **Database**: SQLite (development) and PostgreSQL (production).
- **File Storage**: AWS S3 for storing uploaded answer sheets and backups.
- **Hashing Algorithm**: SHA-256 for generating secure hashes for evaluated answer sheets.

## How It Works

### 1. **Uploading & Evaluating Answer Sheets**
- Teachers can upload PDFs or images of answer sheets via their dashboard.
- If images are uploaded, the platform converts them into PDFs using AWS Textract.
- Teachers can then evaluate the uploaded sheets and add comments or annotations directly on the platform.

### 2. **Blockchain Hashing Process**
- After the evaluation is complete, the system generates a unique hash for the evaluated sheet using the SHA-256 algorithm.
- This hash is then recorded on the blockchain using **Web3**, **Alchemy**, and **Rairtech** to ensure that it cannot be modified without detection.

### 3. **Verification of Answer Sheets**
- Students can view their evaluated sheets along with the blockchain-verified hash.
- Any attempt to tamper with the evaluated sheet will change the hash, alerting students, teachers, and administrators of potential tampering.

### 4. **Backup & Recovery**
- All evaluated sheets are backed up automatically on **AWS S3**.
- In the event of data loss, sheets can be recovered from these backups.

## Future Features
- **AI-Assisted Grading**: Implementing machine learning models to assist teachers in grading.
- **Analytics Dashboard**: Provide detailed analytics for teachers and admins on student performance.


