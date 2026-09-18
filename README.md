 Phishing Email Detection System

Project Overview

This project is a Python-based phishing email detection system that uses machine learning to classify emails as either Phishing or Safe. The application stores every scan in an SQLite database, allowing users to keep a history of analysed emails.

 Requirements

 Python 3.x
 scikit-learn

 

1.Install and import the required libraries by running:

pip install scikit-learn

import sqlite3
import datetime
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression


 2.run the application


python updated detector.py


3.Use the application

 Enter or paste an email when prompted.

 Press Enter
 
 The application will analyse the email and display whether it is Phishing or Safe.

 The result is automatically saved in the SQLite database.


4.Project Files
updated detector.py – Main Python application.

README.md – Project documentation and instructions.

 .gitignore – Prevents unnecessary files, such as the database file, from being uploaded to GitHub.

 
