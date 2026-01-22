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
        
        # Helper to load optional sheets
        def load_sheet(name):
            try:
                df = pd.read_excel(DATA_FILE, sheet_name=name)
                if 'Year' in df.columns:
                    df['Year'] = df['Year'].astype(str)
                return df
            except:
                return pd.DataFrame()

        st.session_state['df_admin'] = load_sheet("Admin_Data")
        st.session_state['df_audit'] = load_sheet("Audit_Data")
        st.session_state['df_legal'] = load_sheet("Legal_Data")
        st.session_state['df_hospital'] = load_sheet("Hospital_Data")
        st.session_state['df_eis_extra'] = load_sheet("EIS_Extra")
        st.session_state['df_strategy'] = load_sheet("Strategy_Data")
        st.session_state['df_finance'] = load_sheet("Finance_Data")
        st.session_state['df_treasury'] = load_sheet("Treasury_Data")
        
        # NEW: Welfare Data
        st.session_state['df_welfare'] = load_sheet("Welfare_Data")

        df_eis['Year'] = df_eis['Year'].astype(str)
        df_rev['Year'] = df_rev['Year'].astype(str)
        
        st.session_state['df_eis'] = df_eis
        st.session_state['df_rev'] = df_rev
        return True
    except Exception as e:
        st.error(f"Error reading saved data: {e}")
        return False

def get_dashboard_data(year_str, month_str):
    data = {
        "cpk": {"total": "0", "new": "0", "resign": "0", "apply_vals": [0,0], "resign_vals": [0,0,0,0], "gender": [50,50], "age": [0,0,0,0]},
        "cps": {"total": "0", "new": "0", "resign": "0", "apply_vals": [0,0], "resign_vals": [0,0,0,0], "gender": [50,50], "age": [0,0,0,0]},
        "finance": {"cpk_paid": "0%", "cps_paid": "0%", "cpk_trend": [0]*12, "cps_trend": [0]*12},
        "revenue": {"total": "0", "users": "0", "avg": "0", "checkup_stats": [0,0,0,0], "checkup_rate": 0, "age_dist": [0,0,0,0,0]}
    }
    return data
