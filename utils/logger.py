import pandas as pd
import datetime
import os
import streamlit as st
from streamlit.web.server.websocket_headers import _get_websocket_headers

LOG_FILE = "data/system_logs.csv"
BANGKOK_TZ = datetime.timezone(datetime.timedelta(hours=7))

def get_remote_ip():
    """Attempts to get the client IP address from headers."""
    try:
        headers = _get_websocket_headers()
        if headers:
            # Check standard headers for IP forwarding
            if "X-Forwarded-For" in headers:
                return headers["X-Forwarded-For"].split(",")[0].strip()
            if "X-Real-Ip" in headers:
                return headers["X-Real-Ip"]
    except Exception:
        pass
    return "Unknown"

def log_action(user, action, details):
    """Records an action to the CSV log file with IP and Timestamp."""
    now_bangkok = datetime.datetime.now(BANGKOK_TZ)
    timestamp = now_bangkok.strftime("%Y-%m-%d %H:%M:%S")
    
    # Get IP Address
    user_ip = get_remote_ip()
    
    new_entry = {
        "Timestamp": timestamp, 
        "User": user, 
        "IP Address": user_ip, # <--- NEW COLUMN
        "Action": action, 
        "Details": details
    }
    
    # Ensure directory exists
    if not os.path.exists("data"):
        os.makedirs("data")
        
    # Load existing or create new
    if os.path.exists(LOG_FILE):
        df = pd.read_csv(LOG_FILE)
        
        # Schema Check: If old logs don't have "IP Address", add it
        if "IP Address" not in df.columns:
            df["IP Address"] = "N/A"
            
        df = pd.concat([df, pd.DataFrame([new_entry])], ignore_index=True)
    else:
        df = pd.DataFrame([new_entry])
        
    df.to_csv(LOG_FILE, index=False)

def get_logs():
    """Returns the log dataframe sorted by newest first."""
    if os.path.exists(LOG_FILE):
        df = pd.read_csv(LOG_FILE)
        
        # Ensure 'IP Address' column exists for display safety
        if "IP Address" not in df.columns:
            df["IP Address"] = "N/A"
            
        # Reorder columns for better readability
        cols = ["Timestamp", "User", "IP Address", "Action", "Details"]
        # Only select columns that actually exist (in case of weird file states)
        existing_cols = [c for c in cols if c in df.columns]
        df = df[existing_cols]
        
        return df.sort_values("Timestamp", ascending=False)
        
    return pd.DataFrame(columns=["Timestamp", "User", "IP Address", "Action", "Details"])

def clear_logs():
    """Clears all logs by removing the file."""
    if os.path.exists(LOG_FILE):
        os.remove(LOG_FILE)
