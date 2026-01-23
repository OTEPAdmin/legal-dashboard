import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from utils.styles import render_header

def show_view():
    render_header("สำนักการคลัง กลุ่มการเงิน ", border_color="#009688")
    
    if 'df_treasury' not in st.session_state or st.session_state['df_treasury'].empty:
        st.error("⚠️ ไม่พบข้อมูล Treasury_Data ใน Excel")
        return

    df = st.session_state['df_treasury'].copy()

    # --- FILTER LOGIC ---
    thai_month_map = {
        "มกราคม": 1, "กุมภาพันธ์": 2, "มีนาคม": 3, "เมษายน": 4, "พฤษภาคม": 5, "มิถุนายน": 6,
        "กรกฎาคม": 7, "สิงหาคม": 8, "กันยายน": 9, "ตุลาคม": 10, "พฤศจิกายน": 11, "ธันวาคม": 12
    }
    
    df['YearNum'] = pd.to_numeric(df['Year'], errors='coerce').fillna(0).astype(int)
    df['MonthNum'] = df['Month'].map(thai_month_map).fillna(0).astype(int)
    df['SortKey'] = (df['YearNum'] * 100) + df['MonthNum']

    available_years = sorted(df['Year'].unique(), reverse=True)
    if not available_years: available_years = ["2568"]
    months_list = list(thai_month_map.keys())

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

    start_key = (int(y_start) * 100) + thai_month_map[m_start]
    end_key = (int(y_end) * 100) + thai_month_map[m_end]
    
    mask = (df['SortKey'] >= start_key) & (df['SortKey'] <= end_key)
    df_filtered = df[mask]
    
    if df_filtered.empty:
        st.warning(f"ไม่พบข้อมูลในช่วงเวลา: {m_start} {y_start} - {m_end} {y_end}")
        return

    # --- AGGREGATION LOGIC ---
    # 1. Flow Data (Rev/Exp): SUM over the period
    flow_mask = df_filtered['Category'] == 'KPI'
    rev_sum = df_filtered[flow_mask & (df_filtered['Item'] == 'Rev_Month')]['Value_1'].sum()
    exp_sum = df_filtered[flow_mask & (df_filtered['Item'] == 'Exp_Month')]['Value_1'].sum()

    # 2. Snapshot Data (Deposit/Loan/Budget): Take the LATEST month in selection
    latest_df = df_filtered.sort_values('SortKey', ascending=False)
    # Get unique categories for latest month only
    latest_key = latest_df.iloc[0]['SortKey']
    df_snapshot = latest_df[latest_df['SortKey'] == latest_key]

    def get_val(cat, item, col='Value_1'):
        val = df_snapshot[(df_snapshot['Category'] == cat) & (df_snapshot['Item'] == item)][col].sum()
        return val

    # KPI Snapshot
    dep_amt = get_val('KPI', 'Deposit', 'Value_1')
    dep_count = get_val('KPI', 'Deposit', 'Value_2')
    loan_amt = get_val('KPI', 'Loan', 'Value_1')
    loan_users = get_val('KPI', 'Loan', 'Value_2')

    # Budget Snapshot
    bud_total = get_val('Budget_Overview', 'Total')
    bud_disb = get_val('Budget_Overview', 'Disbursed')
    bud_commit = get_val('Budget_Overview', 'Committed')
    bud_remain = bud_total - bud_disb - bud_commit
    
    disb_rate = (bud_disb / bud_total * 100) if bud_total > 0 else 0

    # --- UI ROW 1: KPI CARDS ---
    c1, c2, c3, c4 = st.columns(4)
    
    def kpi_card(title, val, unit, subtext, color, border_color):
        st.markdown(f"""
        <div style="background:white; padding:15px; border-radius:10px; border-left: 5px solid {border_color}; box-shadow: 0 2px 5px rgba(0,0,0,0.1);">
            <div style="font-size:14px; color:#555;">{title}</div>
            <div style="font-size:30px; font-weight:bold; color:#333;">{val} <span style="font-size:16px; color:#777;">{unit}</span></div>
            <div style="font-size:12px; color:#999; margin-top:5px;">{subtext}</div>
        </div>
        """, unsafe_allow_html=True)

    with c1: kpi_card("รายรับช่วงเวลานี้", f"{rev_sum:,.2f}", "ล.", "", "#333", "#2ecc71") # Green
    with c2: kpi_card("รายจ่ายช่วงเวลานี้", f"{exp_sum:,.2f}", "ล.", "", "#333", "#f1c40f") # Yellow
    with c3: kpi_card("เงินฝากธนาคาร", f"{dep_amt:,.2f}", "ล.", f"{int(dep_count)} ธนาคาร", "#333", "#3498db") # Blue
    with c4: kpi_card("เงินกู้คงค้าง", f"{loan_amt:,.2f}", "ล.", f"{int(loan_users):,} ราย", "#333", "#9b59b6") # Purple

    st.write("---")

    # --- UI ROW 2: BUDGET & CHART ---
    c_left, c_right = st.columns([1, 2])

    # Left: Budget Summary Card
    with c_left:
        st.markdown(f"##### งบประมาณ ปี {y_end}")
        st.markdown(f"""
        <div style="background:white; padding:20px; border-radius:10px; border: 1px solid #ddd; text-align:center;">
            <div style="font-size:14px; color:#555;">อัตราเบิกจ่าย</div>
            <div style="font-size:50px; font-weight:bold; color:#2ecc71;">{disb_rate:.2f}%</div>
            <hr style="margin:15px 0;">
            <div style="display:flex; justify-content:space-between; margin-bottom:8px; font-size:14px;">
                <span style="font-weight:bold;">งบประมาณทั้งปี</span>
                <span>{bud_total:,.2f} ล.</span>
            </div>
            <div style="display:flex; justify-content:space-between; margin-bottom:8px; font-size:14px; color:#2ecc71;">
                <span style="font-weight:bold;">เบิกจ่ายแล้ว</span>
                <span>{bud_disb:,.2f} ล.</span>
            </div>
             <div style="display:flex; justify-content:space-between; margin-bottom:8px; font-size:14px; color:#f39c12;">
                <span style="font-weight:bold;">ผูกพัน (กันเงิน)</span>
                <span>{bud_commit:,.2f} ล.</span>
            </div>
             <div style="display:flex; justify-content:space-between; font-size:14px; color:#3498db;">
                <span style="font-weight:bold;">คงเหลือ</span>
                <span>{bud_remain:,.2f} ล.</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Right: Disbursement Chart
    with c_right:
        st.markdown("##### เบิกจ่ายตามกลุ่มงาน (10 กลุ่ม)")
        
        # Filter for Department Data (Snapshot)
        df_dept = df_snapshot[df_snapshot['Category'] == 'Dept_Budget'].copy()
        
        if not df_dept.empty:
            # Sort by budget amount
            df_dept = df_dept.sort_values('Value_1', ascending=True)
            
            fig = go.Figure()
            # Budget Bar (Background)
            fig.add_trace(go.Bar(
                y=df_dept['Item'], 
                x=df_dept['Value_1'], 
                orientation='h', 
                name='งบประมาณ',
                marker_color='#29B6F6',
                opacity=0.8
            ))
            # Disbursed Bar (Foreground)
            fig.add_trace(go.Bar(
                y=df_dept['Item'], 
                x=df_dept['Value_2'], 
                orientation='h', 
                name='เบิกจ่าย',
                marker_color='#66BB6A',
                text=df_dept['Value_2'],
                textposition='inside'
            ))
            
            fig.update_layout(
                barmode='overlay', 
                height=400, 
                margin=dict(l=0,r=0,t=20,b=0), 
                font_family="Kanit",
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
            )
            st.plotly_chart(fig, use_container_width=True, key="treasury_chart")
        else:
            st.info("ไม่มีข้อมูลกลุ่มงาน")
