import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from utils.styles import render_header

def show_view():
    render_header("📊 บทสรุปผู้บริหาร (Executive Summary)", border_color="#00BCD4")
    
    # 1. LOAD DATA
    if 'df_eis' not in st.session_state or st.session_state['df_eis'].empty:
        st.error("⚠️ ไม่พบข้อมูล EIS_Data ใน Excel")
        return

    df = st.session_state['df_eis'].copy()

    # 2. FILTER LOGIC
    thai_month_map = {
        "มกราคม": 1, "กุมภาพันธ์": 2, "มีนาคม": 3, "เมษายน": 4, "พฤษภาคม": 5, "มิถุนายน": 6,
        "กรกฎาคม": 7, "สิงหาคม": 8, "กันยายน": 9, "ตุลาคม": 10, "พฤศจิกายน": 11, "ธันวาคม": 12
    }
    
    # Create sortable keys
    df['YearNum'] = pd.to_numeric(df['Year'], errors='coerce').fillna(0).astype(int)
    df['MonthNum'] = df['Month'].map(thai_month_map).fillna(0).astype(int)
    df['SortKey'] = (df['YearNum'] * 100) + df['MonthNum']

    available_years = sorted(df['Year'].unique(), reverse=True)
    if not available_years: available_years = ["2568"]
    months_list = list(thai_month_map.keys())

    # Filter UI
    c1, c2, c3, c4, c5 = st.columns([1,1,1,1,1])
    with c1: m_start = st.selectbox("เดือนเริ่มต้น", months_list, index=0)
    with c2: y_start = st.selectbox("ปีเริ่มต้น", available_years, index=0)
    with c3: m_end = st.selectbox("ถึงเดือน", months_list, index=11) # Default to Dec
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
    
    # 3. CALCULATE AGGREGATES
    if df_filtered.empty:
        st.warning(f"ไม่พบข้อมูลในช่วงเวลา: {m_start} {y_start} - {m_end} {y_end}")
        return

    # For "Flow" data (New, Resign), we SUM over the period
    sum_cols = ['CPK_New', 'CPK_Resign', 'CPS_New', 'CPS_Resign']
    sums = df_filtered[sum_cols].sum()

    # For "Stock" data (Total Members), we take the LATEST month in the selection
    latest_row = df_filtered.sort_values('SortKey', ascending=False).iloc[0]
    
    cpk_total = latest_row['CPK_Total']
    cps_total = latest_row['CPS_Total']
    
    # --- ROW 1: KPI CARDS ---
    st.markdown("##### 👥 ภาพรวมสมาชิก")
    
    c1, c2 = st.columns(2)

    # Left: CPK (Cyan/Blue Theme)
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
            <div style="margin-top:10px; font-size:11px; color:#00838F;">
                ในประจำการ 68.1% | นอกประจำการ 31.9%
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Right: CPS (Purple/Pink Theme)
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
            <div style="margin-top:10px; font-size:11px; color:transparent;">.</div>
        </div>
        """, unsafe_allow_html=True)

    st.write("---")

    # --- ROW 2: DETAILED MOVEMENT CHARTS ---
    # Breakdown Data Generation (Simulated based on totals)
    cpk_new_total = int(sums['CPK_New'])
    cpk_resign_total = int(sums['CPK_Resign'])
    cps_new_total = int(sums['CPS_New'])
    cps_resign_total = int(sums['CPS_Resign'])

    # Chart 1: CPK New
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown("###### 📉 สมาชิกเพิ่ม ช.พ.ค.")
        fig = go.Figure(go.Bar(
            x=[cpk_new_total * 0.8, cpk_new_total * 0.2],
            y=['สมัคร', 'ขอกลับ'],
            orientation='h',
            marker_color=['#4CAF50', '#00ACC1'],
            text=[f"{int(cpk_new_total*0.8):,}", f"{int(cpk_new_total*0.2):,}"],
            textposition='auto'
        ))
        fig.update_layout(height=150, margin=dict(l=0,r=0,t=0,b=0), font_family="Kanit")
        st.plotly_chart(fig, use_container_width=True, key="cpk_new_bar")

    # Chart 2: CPK Resign
    with c2:
        st.markdown("###### 📉 จำหน่าย ช.พ.ค.")
        labels = ['ถอนชื่อ', 'ลาออก', 'ตาย', 'อื่นๆ']
        values = [cpk_resign_total*0.3, cpk_resign_total*0.1, cpk_resign_total*0.5, cpk_resign_total*0.1]
        colors = ['#FFC107', '#AB47BC', '#F44336', '#9E9E9E']
        
        fig = go.Figure(go.Bar(
            x=values, y=labels, orientation='h', marker_color=colors,
            text=[f"{int(v):,}" for v in values], textposition='auto'
        ))
        fig.update_layout(height=150, margin=dict(l=0,r=0,t=0,b=0), font_family="Kanit")
        st.plotly_chart(fig, use_container_width=True, key="cpk_res_bar")

    # Chart 3: CPS New
    with c3:
        st.markdown("###### 📉 สมาชิกเพิ่ม ช.พ.ส.")
        fig = go.Figure(go.Bar(
            x=[cps_new_total * 0.9, cps_new_total * 0.1],
            y=['สมัคร', 'ขอกลับ'],
            orientation='h',
            marker_color=['#4CAF50', '#8E24AA'],
            text=[f"{int(cps_new_total*0.9):,}", f"{int(cps_new_total*0.1):,}"],
            textposition='auto'
        ))
        fig.update_layout(height=150, margin=dict(l=0,r=0,t=0,b=0), font_family="Kanit")
        st.plotly_chart(fig, use_container_width=True, key="cps_new_bar")

    # Chart 4: CPS Resign
    with c4:
        st.markdown("###### 📉 จำหน่าย ช.พ.ส.")
        labels = ['ถอนชื่อ', 'ลาออก', 'ตาย', 'อื่นๆ']
        values = [cps_resign_total*0.2, cps_resign_total*0.1, cps_resign_total*0.65, cps_resign_total*0.05]
        colors = ['#FFC107', '#00ACC1', '#E91E63', '#9E9E9E']
        
        fig = go.Figure(go.Bar(
            x=values, y=labels, orientation='h', marker_color=colors,
            text=[f"{int(v):,}" for v in values], textposition='auto'
        ))
        fig.update_layout(height=150, margin=dict(l=0,r=0,t=0,b=0), font_family="Kanit")
        st.plotly_chart(fig, use_container_width=True, key="cps_res_bar")

    st.write("---")
    st.markdown("##### 👥 ข้อมูลสมาชิก | DEMOGRAPHIC")

    # --- ROW 3: DEMOGRAPHICS ---
    d1, d2, d3, d4 = st.columns(4)

    # CPK Gender
    with d1:
        st.markdown("###### 🚻 สัดส่วนเพศ ช.พ.ค.")
        # Simulated Gender Data
        fig = go.Figure(data=[go.Pie(labels=['ชาย', 'หญิง'], values=[38, 62], hole=.6, 
                                     marker_colors=['#039BE5', '#E91E63'])])
        fig.update_layout(height=200, margin=dict(t=0, b=0, l=0, r=0), showlegend=True, 
                          legend=dict(orientation="h", yanchor="bottom", y=-0.2))
        st.plotly_chart(fig, use_container_width=True, key="cpk_gender")

    # CPK Age
    with d2:
        st.markdown("###### 📊 กลุ่มอายุ ช.พ.ค.")
        age_labels = ['<40', '40-49', '50-59', '60-69', '≥70']
        age_vals = [8, 18, 32, 28, 14]
        colors = ['#00ACC1', '#4CAF50', '#FFC107', '#9C27B0', '#FF5722']
        
        fig = px.bar(x=age_labels, y=age_vals, color=age_labels, color_discrete_sequence=colors)
        fig.update_layout(height=200, margin=dict(t=10, b=0, l=0, r=0), showlegend=False, 
                          xaxis_title=None, yaxis_title="%")
        st.plotly_chart(fig, use_container_width=True, key="cpk_age")

    # CPS Gender
    with d3:
        st.markdown("###### 🚻 สัดส่วนเพศ ช.พ.ส.")
        fig = go.Figure(data=[go.Pie(labels=['ชาย', 'หญิง'], values=[42, 58], hole=.6, 
                                     marker_colors=['#039BE5', '#E91E63'])])
        fig.update_layout(height=200, margin=dict(t=0, b=0, l=0, r=0), showlegend=True,
                          legend=dict(orientation="h", yanchor="bottom", y=-0.2))
        st.plotly_chart(fig, use_container_width=True, key="cps_gender")

    # CPS Age
    with d4:
        st.markdown("###### 📊 กลุ่มอายุ ช.พ.ส.")
        age_labels = ['<40', '40-49', '50-59', '60-69', '≥70']
        age_vals = [5, 12, 25, 35, 23]
        colors = ['#00ACC1', '#4CAF50', '#FFC107', '#9C27B0', '#FF5722']
        
        fig = px.bar(x=age_labels, y=age_vals, color=age_labels, color_discrete_sequence=colors)
        fig.update_layout(height=200, margin=dict(t=10, b=0, l=0, r=0), showlegend=False,
                          xaxis_title=None, yaxis_title="%")
        st.plotly_chart(fig, use_container_width=True, key="cps_age")
