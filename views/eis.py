import streamlit as st
import pandas as pd
import plotly.express as px
from utils.styles import render_header

def show_view():
    render_header("สำนัก ช.พ.ค. - ช.พ.ส", border_color="#FF9800")
    
    # 1. CHECK DATA SOURCES
    if 'df_eis' not in st.session_state:
        st.error("⚠️ ไม่พบข้อมูล EIS_Data (กรุณาอัปโหลดไฟล์)")
        return

    # 2. COMBINE DATA (EIS_Data + EIS_Extra)
    df_main = st.session_state['df_eis'].copy() # Members Data
    
    df_extra = pd.DataFrame()
    if 'df_eis_extra' in st.session_state:
        df_extra = st.session_state['df_eis_extra'].copy() # Death/Finance/Remittance
    
    # Merge them into one dataframe for easier filtering
    df = pd.concat([df_main, df_extra], ignore_index=True)

    # 3. FILTER LOGIC
    thai_month_map = {
        "มกราคม": 1, "กุมภาพันธ์": 2, "มีนาคม": 3, "เมษายน": 4, "พฤษภาคม": 5, "มิถุนายน": 6,
        "กรกฎาคม": 7, "สิงหาคม": 8, "กันยายน": 9, "ตุลาคม": 10, "พฤศจิกายน": 11, "ธันวาคม": 12
    }
    
    # Ensure SortKey exists
    if 'SortKey' not in df.columns:
        df['YearNum'] = pd.to_numeric(df['Year'], errors='coerce').fillna(0).astype(int)
        df['MonthNum'] = df['Month'].map(thai_month_map).fillna(0).astype(int)
        df['SortKey'] = (df['YearNum'] * 100) + df['MonthNum']

    available_years = sorted(df['Year'].unique(), reverse=True)
    months_list = list(thai_month_map.keys())

    # Filter UI
    with st.expander("🔎 ตัวเลือกการกรอง (Filter)", expanded=False):
        c1, c2, c3, c4, c5 = st.columns([1,1,1,1,1])
        with c1: m_start = st.selectbox("เดือนเริ่มต้น", months_list, index=0)
        with c2: y_start = st.selectbox("ปีเริ่มต้น", available_years, index=0)
        with c3: m_end = st.selectbox("ถึงเดือน", months_list, index=11)
        with c4: y_end = st.selectbox("ถึงปี", available_years, index=0)
        with c5: 
            st.write("") 
            st.write("") 
            if st.button("🔍 กรองข้อมูล", use_container_width=True):
                st.rerun()

    # Apply Filter
    start_key = (int(y_start) * 100) + thai_month_map[m_start]
    end_key = (int(y_end) * 100) + thai_month_map[m_end]
    mask = (df['SortKey'] >= start_key) & (df['SortKey'] <= end_key)
    df_filtered = df[mask]
    
    if df_filtered.empty:
        st.warning(f"ไม่พบข้อมูลในช่วงเวลา: {m_start} {y_start} - {m_end} {y_end}")
        return

    # --- ROW 1: MEMBER CARDS (Read from EIS_Data) ---
    latest_key = df_filtered['SortKey'].max()
    df_snap = df_filtered[df_filtered['SortKey'] == latest_key]
    
    def get_val(cat, item):
        val = df_snap[(df_snap['Category'] == cat) & (df_snap['Item'] == item)]['Value'].sum()
        return val

    cpk_mem = get_val('CPK', 'Members_Total')
    cps_mem = get_val('CPS', 'Members_Total')

    c1, c2 = st.columns(2)
    with c1:
        st.markdown(f"""<div style="background:#E3F2FD; padding:15px; border-radius:10px; border-left:5px solid #2196F3;">
            <h4 style="margin:0; color:#1565C0;">👥 สมาชิก ช.พ.ค.</h4>
            <h1 style="margin:0; color:#0D47A1;">{int(cpk_mem):,}</h1></div>""", unsafe_allow_html=True)
    with c2:
        st.markdown(f"""<div style="background:#F3E5F5; padding:15px; border-radius:10px; border-left:5px solid #9C27B0;">
            <h4 style="margin:0; color:#6A1B9A;">👥 สมาชิก ช.พ.ส.</h4>
            <h1 style="margin:0; color:#4A148C;">{int(cps_mem):,}</h1></div>""", unsafe_allow_html=True)
    
    st.write("---")

    # --- ROW 2: CAUSE OF DEATH & FINANCIALS (Read from EIS_Extra) ---
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("💀 สาเหตุการเสียชีวิต")
        # Filter Category 'Death_Cause' (from EIS_Extra)
        df_death = df_filtered[df_filtered['Category'] == 'Death_Cause']
        
        if not df_death.empty:
            df_death_agg = df_death.groupby("Item")['Value'].sum().reset_index().sort_values("Value", ascending=True)
            fig_death = px.bar(df_death_agg, x='Value', y='Item', orientation='h', text='Value',
                               color='Item', color_discrete_sequence=px.colors.qualitative.Pastel)
            fig_death.update_layout(showlegend=False, height=350, xaxis_title="จำนวน (คน)", yaxis_title=None)
            st.plotly_chart(fig_death, use_container_width=True)
        else:
            st.info("ไม่พบข้อมูลสาเหตุการเสียชีวิต (ตรวจสอบ Tab: EIS_Extra)")

    with col2:
        st.subheader("💰 งบการเงิน")
        # Filter Category 'Financial' (from EIS_Extra)
        df_fin = df_filtered[df_filtered['Category'] == 'Financial']
        
        if not df_fin.empty:
            fig_fin = px.bar(df_fin, x='Month', y='Value', color='Item', barmode='group',
                             color_discrete_map={'รายรับ': '#4CAF50', 'รายจ่าย': '#F44336'})
            fig_fin.update_layout(height=350, xaxis_title=None, yaxis_title="ล้านบาท")
            st.plotly_chart(fig_fin, use_container_width=True)
        else:
            st.info("ไม่พบข้อมูลเกี่ยวงบการเงิน (ตรวจสอบ Tab: EIS_Extra)")

    st.write("---")

    # --- ROW 3: REMITTANCE (Read from EIS_Extra) ---
    st.subheader("💸 การนำส่งเงิน")
    # Filter Category 'Remittance' (from EIS_Extra)
    df_remit = df_filtered[df_filtered['Category'] == 'Remittance']
    
    if not df_remit.empty:
        df_remit['MonthNum'] = df_remit['Month'].map(thai_month_map)
        df_remit = df_remit.sort_values(['Year', 'MonthNum'])
        
        fig_remit = px.area(df_remit, x='Month', y='Value', color='Item', 
                            color_discrete_map={'เงินนำส่ง ช.พ.ค.': '#2196F3', 'เงินนำส่ง ช.พ.ส.': '#9C27B0'})
        fig_remit.update_layout(height=400, xaxis_title="เดือน", yaxis_title="จำนวนเงิน (ล้านบาท)")
        st.plotly_chart(fig_remit, use_container_width=True)
    else:
        st.info("ไม่พบข้อมูลการนำส่งเงิน (ตรวจสอบ Tab: EIS_Extra)")
