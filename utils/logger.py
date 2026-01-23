import pandas as pd
import datetime
import os

LOG_FILE = "data/system_logs.csv"

def log_action(user, action, details):
    """Records an action to the CSV log file."""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    new_entry = {"Timestamp": timestamp, "User": user, "Action": action, "Details": details}
    
    # Ensure directory exists
    if not os.path.exists("data"):
        os.makedirs("data")
        
    # Load existing or create new
    if os.path.exists(LOG_FILE):
        df = pd.read_csv(LOG_FILE)
        df = pd.concat([df, pd.DataFrame([new_entry])], ignore_index=True)
    else:
        df = pd.DataFrame([new_entry])
        
    df.to_csv(LOG_FILE, index=False)

def get_logs():
    """Returns the log dataframe sorted by newest first."""
    if os.path.exists(LOG_FILE):
        df = pd.read_csv(LOG_FILE)
        return df.sort_values("Timestamp", ascending=False)
    return pd.DataFrame(columns=["Timestamp", "User", "Action", "Details"])
