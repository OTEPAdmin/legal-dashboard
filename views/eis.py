import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from utils.styles import render_header

def show_view():
    render_header("📊 บทสรุปผู้บริหาร (Executive Summary)", border_color="#00BCD4")
    
    if 'df_eis' not in st.session_state or st.session_state['df_eis'].empty:
        st.error("⚠️ ไม่พบข้อมูล EIS_Data ใน Excel")
        return

    df = st.session_state['df_eis'].copy()

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

    # Aggregate Data
    sum_cols = ['CPK_New', 'CPK_Resign', 'CPS_New', 'CPS_Resign']
    sums = df_filtered[sum_cols].sum()
    latest_row = df_filtered.sort_values('SortKey', ascending=False).iloc[0]
    
    cpk_total = latest_row['CPK_Total']
    cps_total = latest_row['CPS_Total']

    # --- EIS Extra Data (For Death & Finance) ---
    extra_sums = {}
    if 'df_eis_extra' in st.session_state and not st.session_state['df_eis_extra'].empty:
        df_ex = st.session_state['df_eis_extra'].copy()
        df_ex['YearNum'] = pd.to_numeric(df_ex['Year'], errors='coerce').fillna(0).astype(int)
        df_ex['MonthNum'] = df_ex['Month'].map(thai_month_map).fillna(0).astype(int)
        df_ex['SortKey'] = (df_ex['YearNum'] * 100) + df_ex['MonthNum']
        
        mask_ex = (df_ex['SortKey'] >= start_key) & (df_ex['SortKey'] <= end_key)
        df_ex_filtered = df_ex[mask_ex]
        
        # Split by Type
        cpk_ex = df_ex_filtered[df_ex_filtered['Type'] == 'CPK'].sum(numeric_only=True)
        cps_ex = df_ex_filtered[df_ex_filtered['Type'] == 'CPS'].sum(numeric_only=True)
    else:
        # Fallback zeros AND define empty dataframe to prevent crash
        cpk_ex = pd.Series(0, index=['Cause_Cancer','Cause_Lung','Cause_Heart','Cause_Old','Cause_Brain','Fin_Deceased','Fin_Per_Body','Fin_Family'])
        cps_ex = cpk_ex.copy()
        df_ex_filtered = pd.DataFrame(columns=['Type', 'Fin_Per_Body']) # <--- FIX ADDED HERE

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
                    <div style="font-size:24px; font-weight:bold; color:#4CAF50;">+{int(sums['CPK_New']):,}</div>
                    <div style="font-size:12px; color:#555;">สมาชิกเพิ่ม</div>
                </div>
                <div style="text-align:center;">
                    <div style="font-size:24px; font-weight:bold; color:#F44336;">-{int(sums['CPK_Resign']):,}</div>
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
                    <div style="font-size:24px; font-weight:bold; color:#4CAF50;">+{int(sums['CPS_New']):,}</div>
                    <div style="font-size:12px; color:#555;">สมาชิกเพิ่ม</div>
                </div>
                <div style="text-align:center;">
                    <div style="font-size:24px; font-weight:bold; color:#F44336;">-{int(sums['CPS_Resign']):,}</div>
                    <div style="font-size:12px; color:#555;">จำหน่าย</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.write("---")

    # --- UI SECTION 2: CHARTS & DEMO ---
    cpk_new_total = int(sums['CPK_New'])
    cpk_resign_total = int(sums['CPK_Resign'])
    
    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown("###### 📉 สมาชิกเพิ่ม ช.พ.ค.")
        fig = go.Figure(go.Bar(x=[cpk_new_total*0.8, cpk_new_total*0.2], y=['สมัคร', 'ขอกลับ'], orientation='h', marker_color=['#4CAF50', '#00ACC1']))
        fig.update_layout(height=120, margin=dict(l=0,r=0,t=0,b=0), font_family="Kanit")
        st.plotly_chart(fig, use_container_width=True)
    with col_b:
        st.markdown("###### 📉 จำหน่าย ช.พ.ค.")
        fig = go.Figure(go.Bar(x=[cpk_resign_total], y=['จำหน่าย'], orientation='h', marker_color=['#F44336']))
        fig.update_layout(height=120, margin=dict(l=0,r=0,t=0,b=0), font_family="Kanit")
        st.plotly_chart(fig, use_container_width=True)

    st.write("---")
    
    # --- UI SECTION 3: CAUSES OF DEATH ---
    st.markdown("##### ☠️ สาเหตุการเสียชีวิต")
    
    d1, d2 = st.columns(2)
    
    death_labels = ["โรคมะเร็ง", "โรคปอด", "โรคหัวใจ", "โรคชรา", "โรคสมอง"]
    death_colors = ['#FF7043', '#29B6F6', '#AB47BC', '#FFCA28', '#66BB6A'] 

    # CPK Death
    with d1:
        st.markdown("###### 📉 5 อันดับสาเหตุการเสียชีวิต ช.พ.ค.")
        cpk_vals = [cpk_ex.get('Cause_Cancer',0), cpk_ex.get('Cause_Lung',0), cpk_ex.get('Cause_Heart',0), cpk_ex.get('Cause_Old',0), cpk_ex.get('Cause_Brain',0)]
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
        # Check if filtered dataframe exists and has 'Type' column before filtering
        rate = 0
        if not df_ex_filtered.empty and 'Type' in df_ex_filtered.columns:
             subset = df_ex_filtered[df_ex_filtered['Type'] == 'CPK']
             if not subset.empty:
                 rate = subset['Fin_Per_Body'].max()
        
        fin_card("เงินสงเคราะห์ ช.พ.ค.", cpk_ex.get('Fin_Deceased',0), rate, cpk_ex.get('Fin_Family',0), "#E0F7FA")

    with f2:
        rate = 0
        if not df_ex_filtered.empty and 'Type' in df_ex_filtered.columns:
             subset = df_ex_filtered[df_ex_filtered['Type'] == 'CPS']
             if not subset.empty:
                 rate = subset['Fin_Per_Body'].max()

        fin_card("เงินสงเคราะห์ ช.พ.ส.", cps_ex.get('Fin_Deceased',0), rate, cps_ex.get('Fin_Family',0), "#F3E5F5")
