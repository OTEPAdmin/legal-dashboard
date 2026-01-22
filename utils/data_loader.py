import streamlit as st
import pandas as pd
import os

DATA_FOLDER = "data"
DATA_FILE = os.path.join(DATA_FOLDER, "otep_data_saved.xlsx")

def save_and_load_excel(uploaded_file):
    try:
        if not os.path.exists(DATA_FOLDER):
            os.makedirs(DATA_FOLDER)
        with open(DATA_FILE, "wb") as f:
            f.write(uploaded_file.getbuffer())
        return load_from_disk()
    except Exception as e:
        st.error(f"Error saving file: {e}")
        return False

def load_from_disk():
    if not os.path.exists(DATA_FILE):
        return False
        
    try:
        # Load Standard Sheets
        df_eis = pd.read_excel(DATA_FILE, sheet_name="EIS_Data")
        df_rev = pd.read_excel(DATA_FILE, sheet_name="Revenue_Data")
        
        # Load Extra Sheets (Try/Except blocks to prevent crashes if tabs miss)
        try:
            st.session_state['df_admin'] = pd.read_excel(DATA_FILE, sheet_name="Admin_Data").assign(Year=lambda x: x['Year'].astype(str))
        except: st.session_state['df_admin'] = pd.DataFrame()

        try:
            st.session_state['df_audit'] = pd.read_excel(DATA_FILE, sheet_name="Audit_Data").assign(Year=lambda x: x['Year'].astype(str))
        except: st.session_state['df_audit'] = pd.DataFrame()

        try:
            st.session_state['df_legal'] = pd.read_excel(DATA_FILE, sheet_name="Legal_Data").assign(Year=lambda x: x['Year'].astype(str))
        except: st.session_state['df_legal'] = pd.DataFrame()

        try:
            st.session_state['df_hospital'] = pd.read_excel(DATA_FILE, sheet_name="Hospital_Data").assign(Year=lambda x: x['Year'].astype(str))
        except: st.session_state['df_hospital'] = pd.DataFrame()

        # NEW: Load EIS Extra
        try:
            st.session_state['df_eis_extra'] = pd.read_excel(DATA_FILE, sheet_name="EIS_Extra").assign(Year=lambda x: x['Year'].astype(str))
        except: st.session_state['df_eis_extra'] = pd.DataFrame()

        df_eis['Year'] = df_eis['Year'].astype(str)
        df_rev['Year'] = df_rev['Year'].astype(str)
        
        st.session_state['df_eis'] = df_eis
        st.session_state['df_rev'] = df_rev
        return True
    except Exception as e:
        st.error(f"Error reading saved data: {e}")
        return False

def get_dashboard_data(year_str, month_str):
    # Standard EIS/Revenue logic (Unchanged from previous versions)
    data = {
        "cpk": {"total": "0", "new": "0", "resign": "0", "apply_vals": [0,0], "resign_vals": [0,0,0,0], "gender": [50,50], "age": [0,0,0,0]},
        "cps": {"total": "0", "new": "0", "resign": "0", "apply_vals": [0,0], "resign_vals": [0,0,0,0], "gender": [50,50], "age": [0,0,0,0]},
        "finance": {"cpk_paid": "0%", "cps_paid": "0%", "cpk_trend": [0]*12, "cps_trend": [0]*12},
        "revenue": {"total": "0", "users": "0", "avg": "0", "checkup_stats": [0,0,0,0], "checkup_rate": 0, "age_dist": [0,0,0,0,0]}
    }
    # (Simplified for brevity as we use df_eis directly in views now, but keeping structure)
    if 'df_eis' in st.session_state:
        # Populate basic logic if needed by other views
        pass 
    return data
