import streamlit as st
import pandas as pd
import os

DATA_FOLDER = "data"
DATA_FILE = os.path.join(DATA_FOLDER, "otep_data_saved.xlsx")

def save_and_load_excel(uploaded_file):
    try:
        # 1. Save the new file to disk (Overwriting the old one)
        if not os.path.exists(DATA_FOLDER):
            os.makedirs(DATA_FOLDER)
        with open(DATA_FILE, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        # 2. Immediately load the new data
        return load_from_disk()
    except Exception as e:
        st.error(f"Error saving file: {e}")
        return False

def load_from_disk():
    if not os.path.exists(DATA_FILE):
        return False
        
    try:
        def load_sheet(name):
            try:
                df = pd.read_excel(DATA_FILE, sheet_name=name)
                # Force Year to be string to prevent formatting errors (e.g. 2,568)
                if 'Year' in df.columns:
                    df['Year'] = df['Year'].astype(str)
                return df
            except:
                return pd.DataFrame()

        # Load ALL dashboards
        st.session_state['df_eis'] = load_sheet("EIS_Data")
        st.session_state['df_rev'] = load_sheet("Revenue_Data")
        st.session_state['df_admin'] = load_sheet("Admin_Data")
        st.session_state['df_audit'] = load_sheet("Audit_Data")
        st.session_state['df_legal'] = load_sheet("Legal_Data")
        st.session_state['df_hospital'] = load_sheet("Hospital_Data")
        st.session_state['df_eis_extra'] = load_sheet("EIS_Extra")
        st.session_state['df_strategy'] = load_sheet("Strategy_Data")
        st.session_state['df_finance'] = load_sheet("Finance_Data")
        st.session_state['df_treasury'] = load_sheet("Treasury_Data")
        st.session_state['df_welfare'] = load_sheet("Welfare_Data")
        st.session_state['df_dorm'] = load_sheet("Dorm_Data")
        
        # ✅ THIS LINE IS CRITICAL FOR PROCUREMENT DASHBOARD
        st.session_state['df_procure'] = load_sheet("Procure_Data")

        return True
    except Exception as e:
        st.error(f"Error reading saved data: {e}")
        return False

def get_dashboard_data(year_str, month_str):
    # (Placeholder function for compatibility)
    return {}
