# ==========================================
# 1: Loading and importing all required tools
# ==========================================
import sqlite3
import datetime
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression

# ==========================================
# 2: Creating saved log file
# ==========================================
def setup_database():
    connection = sqlite3.connect("security_logs.db")
    cursor = connection.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS phishing_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            email_content TEXT,
            prediction_result TEXT
        )
    """)
    connection.commit()
    connection.close()

# ==========================================
# 3: Setting up scanner rule
# ==========================================
def train_brain():
    # help program learn basic patterns
    examples = [
        "Hi, are we still having lunch today?",
        "URGENT: Click here to change your bank password now!",
        "Please send me the project report by tomorrow morning.",
        "WINNER! You won a free lottery prize click this link!",
        "Hi  hurry up give bank details"
    ]
    answers = [0, 1, 0, 1, 1] # 0 mean safe, 1 mean scam
    
    # turning words into number so program can read them
    counter = CountVectorizer()
    numbers = counter.fit_transform(examples)
    
    brain = LogisticRegression()
    brain.fit(numbers, answers)

    # check how well it learned the basic examples
    accuracy = brain.score(numbers, answers) * 100
    print(f" Model Training Accuracy: {accuracy:.1f}%")
    
    return counter, brain

# ==========================================
# 4: Scanning the text and saving the log
# ==========================================
def check_new_email(counter, brain):
    print("\n--- Command-Line Analysis Interface ---")
    user_email = input("Paste the email text you want to check: ")


    # process the text anf guess the result
    numerical_data = counter.transform([user_email])
    prediction = brain.predict(numerical_data)[0]
    
    # show final answer on screen
    if prediction == 1:
        print("\n WARNING: This email looks like a PHISHING attempt!")
        result_label = "Phishing"
    else:
        print("\n SAFE: This email appears to be legitimate.")
        result_label = "Safe"

    # save this check into history database
    connection = sqlite3.connect("security_logs.db")
    cursor = connection.cursor()
    
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    cursor.execute(
        "INSERT INTO phishing_logs (email_content, prediction_result, timestamp) VALUES (?, ?, ?)",
        (user_email, result_label, current_time)
    )
    
    connection.commit()
    connection.close()
    print(" Scan result successfully logged to security_logs.db.")

# ==========================================
# 5: Showing past history on screen
# ==========================================
def view_saved_logs():
    print("\n---  Retrieving Secure Database Logs ---")
    connection = sqlite3.connect("security_logs.db")
    cursor = connection.cursor()
    
    cursor.execute("SELECT timestamp, email_content, prediction_result FROM phishing_logs")
    all_rows = cursor.fetchall()
    
    if not all_rows:
        print("The database log is currently empty.")
    else:
        for row in all_rows:
            print(f" Time: {row[0]} |  Content: '{row[1]}' |  Result: {row[2]}")
            
    connection.close()

# ==========================================
# 6: starting the detector
# ==========================================
if __name__ == "__main__":
    print("Setting up database...")
    setup_database()
    
    print(" Setting up scanner data...")
    counter, brain = train_brain()
    print("App is ready to use!")
    
    # run the scanner box
    check_new_email(counter, brain)
    
    # show history log right after
    view_saved_logs()
