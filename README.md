BLOCKCHAIN TRANSACTION VALIDATOR

This project is a simple web-based Blockchain Transaction Validator built using Flask.
It demonstrates how transactions can be added, hashed, validated, and tampered with to show blockchain data integrity.

FEATURES

Add new transactions to the blockchain.

Generate SHA-256 hash for each transaction.

Validate blockchain integrity.

Simulate tampering of data.

Reset blockchain data.

Simple and user-friendly web interface.

TECHNOLOGIES USED

Python 3

Flask Web Framework

HTML, CSS, and JavaScript

Hashlib for SHA-256 hashing

HOW TO RUN

Install Python 3 on your system.

Open Command Prompt or Terminal in your project folder.

Install Flask using the command:

pip install flask


Run the application using:

python app.py


Open your browser and visit:

http://127.0.0.1:5000/

HOW IT WORKS

Each transaction entered is hashed using SHA-256.

The transaction data and hash are stored in a stack (LIFO).

The blockchain is validated by recalculating all stored hashes.

If any transaction is tampered with, validation shows INVALID.

You can reset blockchain data anytime to clear all transactions.
