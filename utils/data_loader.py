import streamlit as st
import pandas as pd

def load_data_from_excel(uploaded_file):
    """Reads the uploaded Excel file and saves it to Session State."""
    try:
        # Read both sheets
        df_eis = pd.read_excel(uploaded_file, sheet_name="EIS_Data")
        df_rev = pd.read_excel(uploaded_file, sheet_name="Revenue_Data")
        
        # Ensure 'Year' is treated as text for matching
        df_eis['Year'] = df_eis['Year'].astype(str)
        df_rev['Year'] = df_rev['Year'].astype(str)
        
        # Save to Session State so we can access it everywhere
        st.session_state['df_eis'] = df_eis
        st.session_state['df_rev'] = df_rev
        return True
    except Exception as e:
        st.error(f"Error reading Excel file: {e}")
        return False

def get_dashboard_data(year_str, month_str):
    """
    Retrieves data from Session State and filters it.
    """
    # 1. Default Defaults (Empty Zeros)
    data = {
        "cpk": {"total": "0", "new": "0", "resign": "0", "apply_vals": [0,0], "resign_vals": [0,0,0,0], "gender": [50,50], "age": [0,0,0,0]},
        "cps": {"total": "0", "new": "0", "resign": "0", "apply_vals": [0,0], "resign_vals": [0,0,0,0], "gender": [50,50], "age": [0,0,0,0]},
        "finance": {"cpk_paid": "0%", "cps_paid": "0%", "cpk_trend": [0]*12, "cps_trend": [0]*12},
        "revenue": {"total": "0", "users": "0", "avg": "0", "checkup_stats": [0,0,0,0], "checkup_rate": 0, "age_dist": [0,0,0,0,0]}
    }

    # 2. Check if data is loaded
    if 'df_eis' not in st.session_state or 'df_rev' not in st.session_state:
        return data  # Return zeros if no file uploaded yet

    df_eis = st.session_state['df_eis']
    df_rev = st.session_state['df_rev']

    # 3. MATCH & FILL EIS DATA
    if not df_eis.empty:
        # Filter safely
        row = df_eis[(df_eis['Year'] == str(year_str)) & (df_eis['Month'] == month_str)]
        
        if not row.empty:
            r = row.iloc[0]
            data['cpk']['total'] = f"{int(r['CPK_Total']):,}"
            data['cpk']['new'] = f"+{int(r['CPK_New']):,}"
            data['cpk']['resign'] = f"-{int(r['CPK_Resign']):,}"
            data['cpk']['apply_vals'] = [int(r['CPK_New']), int(r['CPK_New']*0.2)]
            data['cpk']['resign_vals'] = [int(r['CPK_Resign']*0.5), int(r['CPK_Resign']*0.3), int(r['CPK_Resign']*0.1), int(r['CPK_Resign']*0.1)]
            
            data['cps']['total'] = f"{int(r['CPS_Total']):,}"
            data['cps']['new'] = f"+{int(r['CPS_New']):,}"
            data['cps']['resign'] = f"-{int(r['CPS_Resign']):,}"
            data['cps']['apply_vals'] = [int(r['CPS_New']), int(r['CPS_New']*0.1)]
            data['cps']['resign_vals'] = [int(r['CPS_Resign']*0.4), int(r['CPS_Resign']*0.4), int(r['CPS_Resign']*0.1), int(r['CPS_Resign']*0.1)]
            
            paid_cpk = float(r['CPK_Paid_Percent'])
            paid_cps = float(r['CPS_Paid_Percent'])
            data['finance']['cpk_paid'] = f"{paid_cpk}%"
            data['finance']['cps_paid'] = f"{paid_cps}%"
            data['finance']['cpk_trend'] = [paid_cpk - 2 + (i*0.2) for i in range(12)]
            data['finance']['cps_trend'] = [paid_cps - 2 + (i*0.2) for i in range(12)]

    # 4. MATCH & FILL REVENUE DATA
    if not df_rev.empty:
        row = df_rev[(df_rev['Year'] == str(year_str)) & (df_rev['Month'] == month_str)]
        if not row.empty:
            r = row.iloc[0]
            data['revenue']['total'] = f"{float(r['Rev_Total_Million']):.2f}"
            data['revenue']['users'] = f"{int(r['Users_Total']):,}"
            data['revenue']['avg'] = f"{int(r['Avg_Rev_Per_Head']):,}"
            
            reg, att = int(r['Registered_Count']), int(r['Attended_Count'])
            data['revenue']['checkup_stats'] = [int(r['Province_Count']), int(r['Unit_Count']), reg, att]
            data['revenue']['checkup_rate'] = att / reg if reg > 0 else 0
            data['revenue']['age_dist'] = [int(att*0.1), int(att*0.25), int(att*0.35), int(att*0.2), int(att*0.1)]

    return data
