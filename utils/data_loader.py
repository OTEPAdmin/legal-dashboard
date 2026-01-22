import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# Cache data for 5 minutes (ttl=300) so it doesn't reload on every click
@st.cache_data(ttl=300)
def fetch_all_data():
    conn = st.connection("gsheets", type=GSheetsConnection)
    try:
        # Read the two tabs we created
        df_eis = conn.read(worksheet="EIS_Data", ttl=0)
        df_rev = conn.read(worksheet="Revenue_Data", ttl=0)
        
        # Ensure Year is text so we can match it with dropdowns
        df_eis['Year'] = df_eis['Year'].astype(str)
        df_rev['Year'] = df_rev['Year'].astype(str)
        return df_eis, df_rev
    except Exception as e:
        st.error(f"Connection Error: {e}")
        return pd.DataFrame(), pd.DataFrame()

def get_dashboard_data(year_str, month_str):
    df_eis, df_rev = fetch_all_data()
    
    # 1. Default Defaults (Empty Zeros)
    data = {
        "cpk": {"total": "0", "new": "0", "resign": "0", "apply_vals": [0,0], "resign_vals": [0,0,0,0], "gender": [50,50], "age": [0,0,0,0]},
        "cps": {"total": "0", "new": "0", "resign": "0", "apply_vals": [0,0], "resign_vals": [0,0,0,0], "gender": [50,50], "age": [0,0,0,0]},
        "finance": {"cpk_paid": "0%", "cps_paid": "0%", "cpk_trend": [0]*12, "cps_trend": [0]*12},
        "revenue": {"total": "0", "users": "0", "avg": "0", "checkup_stats": [0,0,0,0], "checkup_rate": 0, "age_dist": [0,0,0,0,0]}
    }

    # 2. MATCH & FILL EIS DATA
    if not df_eis.empty:
        row = df_eis[(df_eis['Year'] == year_str) & (df_eis['Month'] == month_str)]
        if not row.empty:
            r = row.iloc[0]
            # Fill CPK
            data['cpk']['total'] = f"{int(r['CPK_Total']):,}"
            data['cpk']['new'] = f"+{int(r['CPK_New']):,}"
            data['cpk']['resign'] = f"-{int(r['CPK_Resign']):,}"
            data['cpk']['apply_vals'] = [int(r['CPK_New']), int(r['CPK_New']*0.2)]
            data['cpk']['resign_vals'] = [int(r['CPK_Resign']*0.5), int(r['CPK_Resign']*0.3), int(r['CPK_Resign']*0.1), int(r['CPK_Resign']*0.1)]
            
            # Fill CPS
            data['cps']['total'] = f"{int(r['CPS_Total']):,}"
            data['cps']['new'] = f"+{int(r['CPS_New']):,}"
            data['cps']['resign'] = f"-{int(r['CPS_Resign']):,}"
            data['cps']['apply_vals'] = [int(r['CPS_New']), int(r['CPS_New']*0.1)]
            data['cps']['resign_vals'] = [int(r['CPS_Resign']*0.4), int(r['CPS_Resign']*0.4), int(r['CPS_Resign']*0.1), int(r['CPS_Resign']*0.1)]
            
            # Fill Finance (Simulate trend ending at current paid %)
            paid_cpk = float(r['CPK_Paid_Percent'])
            paid_cps = float(r['CPS_Paid_Percent'])
            data['finance']['cpk_paid'] = f"{paid_cpk}%"
            data['finance']['cps_paid'] = f"{paid_cps}%"
            data['finance']['cpk_trend'] = [paid_cpk - 2 + (i*0.2) for i in range(12)]
            data['finance']['cps_trend'] = [paid_cps - 2 + (i*0.2) for i in range(12)]

    # 3. MATCH & FILL REVENUE DATA
    if not df_rev.empty:
        row = df_rev[(df_rev['Year'] == year_str) & (df_rev['Month'] == month_str)]
        if not row.empty:
            r = row.iloc[0]
            data['revenue']['total'] = f"{float(r['Rev_Total_Million']):.2f}"
            data['revenue']['users'] = f"{int(r['Users_Total']):,}"
            data['revenue']['avg'] = f"{int(r['Avg_Rev_Per_Head']):,}"
            
            reg, att = int(r['Registered_Count']), int(r['Attended_Count'])
            data['revenue']['checkup_stats'] = [int(r['Province_Count']), int(r['Unit_Count']), reg, att]
            data['revenue']['checkup_rate'] = att / reg if reg > 0 else 0
            
            # Simulate Age Dist based on attendees
            data['revenue']['age_dist'] = [int(att*0.1), int(att*0.25), int(att*0.35), int(att*0.2), int(att*0.1)]

    return data
