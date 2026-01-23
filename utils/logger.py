import pandas as pd
import datetime
import os

LOG_FILE = "data/system_logs.csv"

# Define Bangkok Timezone (GMT+7)
BANGKOK_TZ = datetime.timezone(datetime.timedelta(hours=7))

def log_action(user, action, details):
    """Records an action to the CSV log file with Bangkok Time (GMT+7)."""
    # Get current time in Bangkok timezone
    now_bangkok = datetime.datetime.now(BANGKOK_TZ)
    timestamp = now_bangkok.strftime("%Y-%m-%d %H:%M:%S")
    
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

def clear_logs():
    """Clears all logs by removing the file."""
    if os.path.exists(LOG_FILE):
        os.remove(LOG_FILE)
