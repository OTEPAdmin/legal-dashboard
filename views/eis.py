import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from utils.styles import render_header

def show_view():
    render_header("สำนัก ช.พ.ค. - ช.พ.ส", border_color="#00BCD4")
    
    if 'df_eis' not in st.session_state or st.session_state['df_eis'].empty:
        st.error("⚠️ ไม่พบข้อมูล EIS_Data ใน Excel")
        return

    # --- 1. PREPARE MAIN DATA (MEMBERS) ---
    df = st.session_state['df_eis'].copy()

    thai_month_map = {
        "มกราคม": 1, "กุมภาพันธ์": 2, "มีนาคม": 3, "เมษายน": 4, "พฤษภาคม": 5, "มิถุนายน": 6,
        "กรกฎาคม": 7, "สิงหาคม": 8, "กันยายน": 9, "ตุลาคม": 10, "พฤศจิกายน": 11, "ธันวาคม": 12
    }
    
    # Ensure SortKey
    if 'SortKey' not in df.columns:
        df['YearNum'] = pd.to_numeric(df['Year'], errors='coerce').fillna(0).astype(int)
        df['MonthNum'] = df['Month'].map(thai_month_map).fillna(0).astype(int)
        df['SortKey'] = (df['YearNum'] * 100) + df['MonthNum']

    available_years = sorted(df['Year'].unique(), reverse=True)
    if not available_years: available_years = ["2568"]
    months_list = list(thai_month_map.keys())

    # --- FILTER UI ---
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

    # Aggregate Member Data
    # Note: Using Item/Category structure from generated data
    def get_main_sum(cat, item):
        return df_filtered[(df_filtered['Category'] == cat) & (df_filtered['Item'] == item)]['Value'].sum()

    # Get latest total count (Snapshot)
    latest_row_key = df_filtered['SortKey'].max()
    df_snap = df_filtered[df_filtered['SortKey'] == latest_row_key]
    
    def get_snap_val(cat, item):
        val = df_snap[(df_snap['Category'] == cat) & (df_snap['Item'] == item)]['Value'].sum()
        return val

    cpk_total = get_snap_val('CPK', 'Members_Total')
    cps_total = get_snap_val('CPS', 'Members_Total')
    
    cpk_new = get_main_sum('CPK', 'Members_New')
    cpk_resign = get_main_sum('CPK', 'Members_Resign')
    cps_new = get_main_sum('CPS', 'Members_New')
    cps_resign = get_main_sum('CPS', 'Members_Resign')

    # --- 2. PREPARE EXTRA DATA (DEATH/FINANCE) ---
    # We bridge the gap between "Long Format" data and "Wide Format" code expectations
    cpk_ex = {}
    cps_ex = {}
    
    if 'df_eis_extra' in st.session_state and not st.session_state['df_eis_extra'].empty:
        df_ex = st.session_state['df_eis_extra'].copy()
        
        # Prepare Filter
        df_ex['YearNum'] = pd.to_numeric(df_ex['Year'], errors='coerce').fillna(0).astype(int)
        df_ex['MonthNum'] = df_ex['Month'].map(thai_month_map).fillna(0).astype(int)
        df_ex['SortKey'] = (df_ex['YearNum'] * 100) + df_ex['MonthNum']
        mask_ex = (df_ex['SortKey'] >= start_key) & (df_ex['SortKey'] <= end_key)
        df_ex_filtered = df_ex[mask_ex]

        # --- DATA MAPPING LOGIC ---
        # 1. Death Causes (Map Thai Items to Code Keys)
        # Since data isn't split by Type, we split 50/50 for demo visualization
        death_map = {
            'โรคมะเร็ง': 'Cause_Cancer',
            'โรคปอด': 'Cause_Lung',
            'โรคหัวใจ/หลอดเลือด': 'Cause_Heart',
            'ชราภาพ': 'Cause_Old',
            'ติดเชื้อในกระแสเลือด': 'Cause_Brain' # Mapping to 5th category
        }
        for item_name, key in death_map.items():
            val = df_ex_filtered[(df_ex_filtered['Category'] == 'Death_Cause') & (df_ex_filtered['Item'] == item_name)]['Value'].sum()
            cpk_ex[key] = int(val * 0.55) # Mock: CPK has slightly more
            cps_ex[key] = int(val * 0.45)

        # 2. Financials (Map Items to Code Keys)
        # Remittance
        remit_cpk = df_ex_filtered[(df_ex_filtered['Category'] == 'Remittance') & (df_ex_filtered['Item'] == 'เงินนำส่ง ช.พ.ค.')]['Value'].sum()
        remit_cps = df_ex_filtered[(df_ex_filtered['Category'] == 'Remittance') & (df_ex_filtered['Item'] == 'เงินนำส่ง ช.พ.ส.')]['Value'].sum()
        
        # Financial Aid (Mocking logic based on Revenue data if specific items missing)
        fin_rev = df_ex_filtered[(df_ex_filtered['Category'] == 'Financial') & (df_ex_filtered['Item'] == 'รายรับ')]['Value'].sum()
        
        # Assign to dictionary keys expected by UI
        cpk_ex['Fin_Family'] = remit_cpk * 1000 # Scaling for demo amount
        cpk_ex['Fin_Deceased'] = get_main_sum('CPK', 'Members_Dead') # Use actual dead count
        cpk_ex['Fin_Per_Body'] = 200000 # Static rate

        cps_ex['Fin_Family'] = remit_cps * 1000
        cps_ex['Fin_Deceased'] = get_main_sum('CPS', 'Members_Dead')
        cps_ex['Fin_Per_Body'] = 180000

    # --- UI SECTION 1: MEMBERS ---
    st.markdown("##### 👥 ภาพรวมสมาชิก")
    c1, c2 = st.columns(2)

    with c1:
        st.markdown(f"""
        <div style="background:#E0F7FA; padding:20px; border-radius:10px; border-top: 5px solid #00BCD4; box-shadow: 0 2px 5px rgba(0,0,0,0.1);">
            <div style="display:flex; justify-content:space-between; align-items:center;">
                <h4 style="margin:0; color:#006064;">👥 ภาพรวมสมาชิก ช.พ.ค.</h4>
                <span style="background:white; padding:2px 8px; border-radius:10px; font-size:12px; color:#00838F;">ปี {y_end}</span>
            </div>
            <div style="display:flex; justify-content:space-between; align-items:flex-end; margin-top:15px;">
                <div style="text-align:center;">
                    <div style="font-size:38px; font-weight:bold; color:#00BCD4;">{int(cpk_total):,}</div>
                    <div style="font-size:12px; color:#555;">จำนวนสมาชิก</div>
                </div>
                <div style="text-align:center;">
                    <div style="font-size:24px; font-weight:bold; color:#4CAF50;">+{int(cpk_new):,}</div>
                    <div style="font-size:12px; color:#555;">สมาชิกเพิ่ม</div>
                </div>
                <div style="text-align:center;">
                    <div style="font-size:24px; font-weight:bold; color:#F44336;">-{int(cpk_resign):,}</div>
                    <div style="font-size:12px; color:#555;">จำหน่าย</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown(f"""
        <div style="background:#F3E5F5; padding:20px; border-radius:10px; border-top: 5px solid #AB47BC; box-shadow: 0 2px 5px rgba(0,0,0,0.1);">
            <div style="display:flex; justify-content:space-between; align-items:center;">
                <h4 style="margin:0; color:#4A148C;">👥 ภาพรวมสมาชิก ช.พ.ส.</h4>
                <span style="background:white; padding:2px 8px; border-radius:10px; font-size:12px; color:#6A1B9A;">ปี {y_end}</span>
            </div>
             <div style="display:flex; justify-content:space-between; align-items:flex-end; margin-top:15px;">
                <div style="text-align:center;">
                    <div style="font-size:38px; font-weight:bold; color:#AB47BC;">{int(cps_total):,}</div>
                    <div style="font-size:12px; color:#555;">จำนวนสมาชิก</div>
                </div>
                <div style="text-align:center;">
                    <div style="font-size:24px; font-weight:bold; color:#4CAF50;">+{int(cps_new):,}</div>
                    <div style="font-size:12px; color:#555;">สมาชิกเพิ่ม</div>
                </div>
                <div style="text-align:center;">
                    <div style="font-size:24px; font-weight:bold; color:#F44336;">-{int(cps_resign):,}</div>
                    <div style="font-size:12px; color:#555;">จำหน่าย</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.write("---")

    # --- UI SECTION 2: CHARTS & DEMO ---
    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown("###### 📉 สมาชิกเพิ่ม ช.พ.ค.")
        # Mocking sub-categories for bar chart since we only have total new
        val_total = int(cpk_new)
        val_reg = int(val_total * 0.8)
        val_rejoin = val_total - val_reg
        fig = go.Figure(go.Bar(x=[val_reg, val_rejoin], y=['สมัครใหม่', 'ขอกลับ'], orientation='h', marker_color=['#4CAF50', '#00ACC1'], text=[val_reg, val_rejoin], textposition='auto'))
        fig.update_layout(height=120, margin=dict(l=0,r=0,t=0,b=0), font_family="Kanit")
        st.plotly_chart(fig, use_container_width=True)
    with col_b:
        st.markdown("###### 📉 จำหน่าย ช.พ.ค.")
        fig = go.Figure(go.Bar(x=[int(cpk_resign)], y=['จำหน่าย'], orientation='h', marker_color=['#F44336'], text=[int(cpk_resign)], textposition='auto'))
        fig.update_layout(height=120, margin=dict(l=0,r=0,t=0,b=0), font_family="Kanit")
        st.plotly_chart(fig, use_container_width=True)

    st.write("---")
    
    # --- UI SECTION 3: CAUSES OF DEATH ---
    st.markdown("##### ☠️ สาเหตุการเสียชีวิต")
    
    d1, d2 = st.columns(2)
    
    death_labels = ["โรคมะเร็ง", "โรคปอด", "โรคหัวใจ", "โรคชรา", "ติดเชื้อฯ"]
    death_colors = ['#FF7043', '#29B6F6', '#AB47BC', '#FFCA28', '#66BB6A'] 

    # CPK Death
    with d1:
        st.markdown("###### 📉 5 อันดับสาเหตุการเสียชีวิต ช.พ.ค.")
        cpk_vals = [cpk_ex.get('Cause_Cancer',0), cpk_ex.get('Cause_Lung',0), cpk_ex.get('Cause_Heart',0), cpk_ex.get('Cause_Old',0), cpk_ex.get('Cause_Brain',0)]
        if sum(cpk_vals) == 0: st.info("ไม่มีข้อมูล")
        else:
            fig = go.Figure(go.Bar(
                x=cpk_vals, y=death_labels, orientation='h', 
                marker_color=death_colors, text=cpk_vals, textposition='auto'
            ))
            fig.update_layout(height=250, margin=dict(l=0,r=0,t=0,b=0), font_family="Kanit", yaxis=dict(autorange="reversed"))
            st.plotly_chart(fig, use_container_width=True, key="cpk_death")

    # CPS Death
    with d2:
        st.markdown("###### 📉 5 อันดับสาเหตุการเสียชีวิต ช.พ.ส.")
        cps_vals = [cps_ex.get('Cause_Cancer',0), cps_ex.get('Cause_Lung',0), cps_ex.get('Cause_Heart',0), cps_ex.get('Cause_Old',0), cps_ex.get('Cause_Brain',0)]
        if sum(cps_vals) == 0: st.info("ไม่มีข้อมูล")
        else:
            fig = go.Figure(go.Bar(
                x=cps_vals, y=death_labels, orientation='h', 
                marker_color=death_colors, text=cps_vals, textposition='auto'
            ))
            fig.update_layout(height=250, margin=dict(l=0,r=0,t=0,b=0), font_family="Kanit", yaxis=dict(autorange="reversed"))
            st.plotly_chart(fig, use_container_width=True, key="cps_death")

    st.write("---")

    # --- UI SECTION 4: FINANCIAL CONTRIBUTION ---
    st.markdown("##### 💳 การนำส่งเงิน & งบการเงิน")

    f1, f2 = st.columns(2)

    def fin_card(title, count, per_body, total_fam, bg_color="#E0F7FA"):
        st.markdown(f"""
        <div style="background:{bg_color}; padding:15px; border-radius:10px; margin-bottom:20px;">
            <h5 style="margin-bottom:15px; color:#555;">💰 {title}</h5>
            <div style="display:flex; gap:10px;">
                <div style="flex:1; background:#00ACC1; padding:10px; border-radius:8px; text-align:center; color:white;">
                    <div style="font-size:11px;">จำนวนผู้วายชนม์</div>
                    <div style="font-size:22px; font-weight:bold;">{int(count):,} <span style="font-size:12px;">ราย</span></div>
                </div>
                <div style="flex:1; background:#66BB6A; padding:10px; border-radius:8px; text-align:center; color:white;">
                    <div style="font-size:11px;">เงินสงเคราะห์รายศพ</div>
                    <div style="font-size:22px; font-weight:bold;">{int(per_body):,}.-</div>
                </div>
                <div style="flex:1.2; background:#FBC02D; padding:10px; border-radius:8px; text-align:center; color:white;">
                    <div style="font-size:11px;">เงินสงเคราะห์ครอบครัว</div>
                    <div style="font-size:22px; font-weight:bold;">{int(total_fam):,}-.</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with f1:
        fin_card("เงินสงเคราะห์ ช.พ.ค.", cpk_ex.get('Fin_Deceased',0), cpk_ex.get('Fin_Per_Body',0), cpk_ex.get('Fin_Family',0), "#E0F7FA")

    with f2:
        fin_card("เงินสงเคราะห์ ช.พ.ส.", cps_ex.get('Fin_Deceased',0), cps_ex.get('Fin_Per_Body',0), cps_ex.get('Fin_Family',0), "#F3E5F5")
