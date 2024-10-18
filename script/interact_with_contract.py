import hashlib
import os
import json
import csv
import requests
from web3 import Web3
from dotenv import load_dotenv
from datetime import datetime
import sys
import random
import string

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

def interact_with_contract():
    load_dotenv()

    # Initialize Web3 with Alchemy URL (use the HTTP URL from your Alchemy dashboard)
    alchemy_url = os.getenv('ALCHEMY_URL')  # Set your Alchemy project URL in .env file
    web3 = Web3(Web3.HTTPProvider(alchemy_url))

    # Check connection
    if not web3.is_connected():
        raise Exception("Failed to connect to the network")

    # Load contract ABI and address
    with open('script/AnswerSheetEvaluation.json') as f:
        abi = json.load(f)

    contract_address = os.getenv('CONTRACT_ADDRESS')
    contract = web3.eth.contract(address=contract_address, abi=abi)

    # Set up account details
    private_key = os.getenv('PRIVATE_KEY')
    account = web3.eth.account.from_key(private_key)

    # Check balance
    balance = web3.eth.get_balance(account.address)
    print(f'Account Balance: {web3.from_wei(balance, "ether")} ETH')

    if balance == 0:
        raise Exception("Insufficient funds in the account. Please fund it and try again.")

    # Function to calculate the hash of a file
    def calculate_file_hash(file_path):
        hash_algorithm = hashlib.sha256()
        with open(file_path, 'rb') as file:
            while chunk := file.read(8192):
                hash_algorithm.update(chunk)
        return hash_algorithm.hexdigest()

    # Function to add the file hash to the blockchain
    def add_file_hash_to_blockchain(file_hash):
        nonce = web3.eth.get_transaction_count(account.address)
        transaction = contract.functions.addFileHash(file_hash).build_transaction({
            'chainId': int(os.getenv('CHAIN_ID')),  # Ensure this is correct
            'gas': 2000000,
            'gasPrice': web3.to_wei('20', 'gwei'),
            'nonce': nonce
        })
        
        signed_tx = web3.eth.account.sign_transaction(transaction, private_key=private_key)
        
        try:
            tx_hash = web3.eth.send_raw_transaction(signed_tx.raw_transaction)
            return web3.to_hex(tx_hash)
        except Exception as e:
            print(f'Error sending transaction: {e}')
            return None

    # Function to tokenize the file using Rairtech API
    def tokenize_file_using_api(file_path, filename):
        api_key = os.getenv('RAIRTECH_API_KEY')  # Your Rairtech API key
        api_url = "https://api.rairtech.com/v1/tokens"  # Adjust to the actual endpoint

        # Prepare file and metadata for the request
        files = {'file': open(file_path, 'rb')}
        metadata = {
            "title": f"Tokenized Answer Sheet - {filename}",
            "description": "Tokenized version of the evaluated answer sheet",
            "author": "Teacher's Name"
        }

        headers = {
            'Authorization': f'Bearer {api_key}',  # Adjust authorization method if different
            'Content-Type': 'multipart/form-data'
        }

        try:
            response = requests.post(api_url, files=files, data=metadata, headers=headers)
            response.raise_for_status()  # Check for HTTP errors
            token_info = response.json()
            print(f"Token created: {token_info['token_id']}")
            return token_info
        except requests.exceptions.RequestException as e:
            print(f"Error tokenizing file: {e}")
            return None

    # Function to process all files in the Evaluated folder
    def process_files_in_evaluated_folder():
        evaluated_folder_path = 'datasets/Evaluated'
        transaction_records = []
        
        for filename in os.listdir(evaluated_folder_path):
            if filename.startswith('Transaction'):
                continue

            file_path = os.path.join(evaluated_folder_path, filename)
            if os.path.isfile(file_path):
                # Calculate file hash
                file_hash = calculate_file_hash(file_path)
                print(f'File: {filename}, Hash: {file_hash}')
                
                # Tokenize the file using Rairtech API
                token = tokenize_file_using_api(file_path, filename)
                if token:
                    print(f"Token ID for {filename}: {token['token_id']}")
                    
                    # Add file hash to blockchain
                    tx_hash = add_file_hash_to_blockchain(file_hash)
                    if tx_hash:
                        print(f'Transaction hash for {filename}: {tx_hash}')
                        transaction_records.append({
                            'Filename': filename, 
                            'Token_ID': token['token_id'], 
                            'Transaction_hash': tx_hash
                        })

        # Save transaction records to CSV file
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        csv_filename = f'{evaluated_folder_path}/Transaction_{timestamp}.csv'
        fieldname_random = lambda length: ''.join(random.choices(string.ascii_letters + string.digits, k=length))

        with open(csv_filename, mode='a+', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=['Filename', fieldname_random(64), 'Token_ID', 'Transaction_hash'])
            writer.writeheader()
            writer.writerows(transaction_records)

    # Run the process
    process_files_in_evaluated_folder()

