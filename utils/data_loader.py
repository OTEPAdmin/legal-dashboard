import streamlit as st
import pandas as pd
import os

DATA_PATH = "data/otep_data_saved.xlsx"

def load_from_disk():
    """Loads the Excel file from disk into session state on app startup."""
    if os.path.exists(DATA_PATH):
        try:
            # Load all sheets
            excel_file = pd.ExcelFile(DATA_PATH)
            
            # 1. EIS Data
            if 'EIS_Data' in excel_file.sheet_names:
                st.session_state['df_eis'] = pd.read_excel(excel_file, 'EIS_Data')
            
            # 2. EIS Extra (New)
            if 'EIS_Extra' in excel_file.sheet_names:
                st.session_state['df_eis_extra'] = pd.read_excel(excel_file, 'EIS_Extra')
                
            # 3. Procurement
            if 'Procure_Data' in excel_file.sheet_names:
                st.session_state['df_procure'] = pd.read_excel(excel_file, 'Procure_Data')
                
            # 4. Strategy
            if 'Strategy_Data' in excel_file.sheet_names:
                st.session_state['df_strategy'] = pd.read_excel(excel_file, 'Strategy_Data')

            # 5. Finance/Treasury (If added later)
            if 'Finance_Data' in excel_file.sheet_names:
                st.session_state['df_finance'] = pd.read_excel(excel_file, 'Finance_Data')
                
            st.session_state['data_loaded'] = True
            return True
        except Exception as e:
            st.error(f"Error loading data: {e}")
            return False
    return False

def save_and_load_excel(uploaded_file):
    """Saves uploaded file to disk and loads it."""
    try:
        # Ensure directory exists
        if not os.path.exists("data"):
            os.makedirs("data")
            
        # Save file
        with open(DATA_PATH, "wb") as f:
            f.write(uploaded_file.getbuffer())
            
        # Load immediately
        return load_from_disk()
    except Exception as e:
        st.error(f"Error saving file: {e}")
        return False
