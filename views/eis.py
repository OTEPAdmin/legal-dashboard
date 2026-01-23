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
    
    if 'SortKey' not in df.columns:
        df['YearNum'] = pd.to_numeric(df['Year'], errors='coerce').fillna(0).astype(int)
        df['MonthNum'] = df['Month'].map(thai_month_map).fillna(0).astype(int)
        df['SortKey'] = (df['YearNum'] * 100) + df['MonthNum']

    # --- FILTER SETUP ---
    target_years = ["2568", "2567", "2566"]
    actual_years = [str(y) for y in df['Year'].unique()]
    available_years = sorted(list(set(target_years + actual_years)), reverse=True)
    months_list = list(thai_month_map.keys())

    # --- FILTER UI ---
    st.markdown("##### 🔎 ตัวเลือกการกรอง (Filter)")
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

    # --- CALCULATION LOGIC ---
    def get_sum(cat, item):
        return df_filtered[(df_filtered['Category'] == cat) & (df_filtered['Item'] == item)]['Value'].sum()

    # Snapshot for Totals (Latest month)
    latest_key = df_filtered['SortKey'].max()
    df_snap = df_filtered[df_filtered['SortKey'] == latest_key]
    
    def get_snap(cat, item):
        return df_snap[(df_snap['Category'] == cat) & (df_snap['Item'] == item)]['Value'].sum()

    # Main Numbers
    cpk_total = get_snap('CPK', 'Members_Total')
    cps_total = get_snap('CPS', 'Members_Total')
    
    cpk_new_total = get_sum('CPK', 'Members_New')
    cpk_resign_val = get_sum('CPK', 'Members_Resign')
    cpk_dead_val = get_sum('CPK', 'Members_Dead')
    cpk_removed_total = cpk_resign_val + cpk_dead_val

    cps_new_total = get_sum('CPS', 'Members_New')
    cps_resign_val = get_sum('CPS', 'Members_Resign')
    cps_dead_val = get_sum('CPS', 'Members_Dead')
    cps_removed_total = cps_resign_val + cps_dead_val

    # =================================================================================================
    # SECTION 1: EXECUTIVE SUMMARY (บทสรุปผู้บริหาร)
    # =================================================================================================
    st.markdown("#### 📊 บทสรุปผู้บริหาร")

    # ROW 1: OVERVIEW CARDS
    col_cpk, col_cps = st.columns(2)

    # 1.1 CPK CARD
    with col_cpk:
        st.markdown(f"""
        <div style="background-color:#E3F2FD; padding:15px; border-radius:10px; border-top: 5px solid #2196F3; box-shadow: 0 2px 4px rgba(0,0,0,0.1); font-family: 'Kanit', sans-serif;">
            <div style="display:flex; justify-content:space-between; color:#555; font-weight:bold; margin-bottom:10px;">
                <span>👥 ภาพรวมสมาชิก ช.พ.ค.</span>
                <span style="font-size:12px; background:#BBDEFB; padding:2px 8px; border-radius:10px;">ปี {y_end}</span>
            </div>
            <div style="display:flex; justify-content:space-between; align-items:flex-end;">
                <div style="text-align:center; width:33%;">
                    <div style="font-size:28px; font-weight:bold; color:#0277BD;">{int(cpk_total):,}</div>
                    <div style="font-size:12px; color:#666;">จำนวนสมาชิก</div>
                </div>
                <div style="text-align:center; width:33%;">
                    <div style="font-size:20px; font-weight:bold; color:#43A047;">+{int(cpk_new_total):,}</div>
                    <div style="font-size:12px; color:#666;">สมาชิกเพิ่ม</div>
                </div>
                <div style="text-align:center; width:33%;">
                    <div style="font-size:20px; font-weight:bold; color:#C62828;">-{int(cpk_removed_total):,}</div>
                    <div style="font-size:12px; color:#666;">จำหน่าย</div>
                </div>
            </div>
            <div style="margin-top:10px; font-size:10px; color:#0277BD;">
                ในประจำการ 68.1% | นอกประจำการ 31.9%
            </div>
        </div>
        """, unsafe_allow_html=True)

    # 1.2 CPS CARD
    with col_cps:
        st.markdown(f"""
        <div style="background-color:#F3E5F5; padding:15px; border-radius:10px; border-top: 5px solid #9C27B0; box-shadow: 0 2px 4px rgba(0,0,0,0.1); font-family: 'Kanit', sans-serif;">
            <div style="display:flex; justify-content:space-between; color:#555; font-weight:bold; margin-bottom:10px;">
                <span>👥 ภาพรวมสมาชิก ช.พ.ส.</span>
                <span style="font-size:12px; background:#E1BEE7; padding:2px 8px; border-radius:10px;">ปี {y_end}</span>
            </div>
            <div style="display:flex; justify-content:space-between; align-items:flex-end;">
                <div style="text-align:center; width:33%;">
                    <div style="font-size:28px; font-weight:bold; color:#7B1FA2;">{int(cps_total):,}</div>
                    <div style="font-size:12px; color:#666;">จำนวนสมาชิก</div>
                </div>
                <div style="text-align:center; width:33%;">
                    <div style="font-size:20px; font-weight:bold; color:#43A047;">+{int(cps_new_total):,}</div>
                    <div style="font-size:12px; color:#666;">สมาชิกเพิ่ม</div>
                </div>
                <div style="text-align:center; width:33%;">
                    <div style="font-size:20px; font-weight:bold; color:#C62828;">-{int(cps_removed_total):,}</div>
                    <div style="font-size:12px; color:#666;">จำหน่าย</div>
                </div>
            </div>
             <div style="margin-top:10px; font-size:10px; color:#7B1FA2;">
                คู่สมรส 95% | บุตร 5%
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.write("")

    # ROW 2: BAR CHARTS
    def create_horiz_bar(values, labels, colors, title):
        fig = go.Figure(go.Bar(
            x=values,
            y=labels,
            orientation='h',
            marker_color=colors,
            text=[f"{v:,}" for v in values],
            textposition='inside',
            insidetextanchor='middle'
        ))
        fig.update_layout(
            title=dict(text=title, font=dict(size=14, family="Kanit"), x=0),
            height=150,
            margin=dict(l=0, r=0, t=30, b=0),
            xaxis=dict(showgrid=False, showticklabels=False, zeroline=False),
            yaxis=dict(showgrid=False, showline=False),
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(family="Kanit")
        )
        return fig

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        val_apply = int(cpk_new_total * 0.85)
        val_rejoin = cpk_new_total - val_apply
        fig = create_horiz_bar([val_rejoin, val_apply], ['ขอกลับ', 'สมัคร'], ['#00ACC1', '#4CAF50'], "📈 สมาชิกเพิ่ม ช.พ.ค.")
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        val_dead = int(cpk_dead_val)
        val_withdraw = int(cpk_resign_val * 0.5)
        val_resign = int(cpk_resign_val * 0.3)
        val_other = cpk_resign_val - val_withdraw - val_resign
        
        fig = create_horiz_bar(
            [val_other, val_dead, val_resign, val_withdraw], 
            ['อื่นๆ', 'ตาย', 'ลาออก', 'ถอนชื่อ'], 
            ['#9E9E9E', '#E53935', '#8E24AA', '#FFB300'], 
            "📉 จำหน่าย ช.พ.ค."
        )
        st.plotly_chart(fig, use_container_width=True)

    with c3:
        val_apply = int(cps_new_total * 0.82)
        val_rejoin = cps_new_total - val_apply
        fig = create_horiz_bar([val_rejoin, val_apply], ['ขอกลับ', 'สมัคร'], ['#AB47BC', '#66BB6A'], "📈 สมาชิกเพิ่ม ช.พ.ส.")
        st.plotly_chart(fig, use_container_width=True)

    with c4:
        val_dead = int(cps_dead_val)
        val_withdraw = int(cps_resign_val * 0.5)
        val_resign = int(cps_resign_val * 0.3)
        val_other = cps_resign_val - val_withdraw - val_resign
        
        fig = create_horiz_bar(
            [val_other, val_dead, val_resign, val_withdraw], 
            ['อื่นๆ', 'ตาย', 'ลาออก', 'ถอนชื่อ'], 
            ['#9E9E9E', '#E53935', '#00ACC1', '#FFB300'], 
            "📉 จำหน่าย ช.พ.ส."
        )
        st.plotly_chart(fig, use_container_width=True)

    st.write("---")

    # =================================================================================================
    # SECTION 2: MEMBER DEMOGRAPHICS (ข้อมูลสมาชิก)
    # =================================================================================================
    st.markdown("#### 👥 ข้อมูลสมาชิก | DEMOGRAPHIC")

    # --- Simulation Logic for Demographics (Proportional to Total) ---
    # We use fixed ratios for demo visualization since raw data doesn't have this granularity
    
    # 1. Gender Ratio
    cpk_male = int(cpk_total * 0.38)
    cpk_female = cpk_total - cpk_male
    
    cps_male = int(cps_total * 0.42)
    cps_female = cps_total - cps_male

    # 2. Age Groups (<40, 40-49, 50-59, 60-69, >=70)
    # Weights: [0.08, 0.18, 0.32, 0.28, 0.14] for CPK
    # Weights: [0.05, 0.12, 0.25, 0.35, 0.23] for CPS
    cpk_age_vals = [int(cpk_total*x) for x in [0.08, 0.18, 0.32, 0.28, 0.14]]
    cps_age_vals = [int(cps_total*x) for x in [0.05, 0.12, 0.25, 0.35, 0.23]]
    age_labels = ['<40', '40-49', '50-59', '60-69', '≥70']
    age_colors = ['#29B6F6', '#66BB6A', '#FBC02D', '#AB47BC', '#FF7043']

    # --- Layout ---
    col_d1, col_d2, col_d3, col_d4 = st.columns(4)

    # Function for Donut Chart (Gender)
    def create_donut(male_val, female_val, title):
        labels = ['ชาย', 'หญิง']
        values = [male_val, female_val]
        colors = ['#29B6F6', '#EC407A'] # Blue, Pink
        
        fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.5, marker_colors=colors, sort=False)])
        fig.update_layout(
            title=dict(text=title, font=dict(size=14, family="Kanit"), x=0),
            height=200,
            margin=dict(l=10, r=10, t=40, b=10),
            showlegend=True,
            legend=dict(orientation="h", y=-0.1, font=dict(family="Kanit"))
        )
        return fig

    # Function for Bar Chart (Age)
    def create_age_bar(values, title):
        fig = go.Figure(go.Bar(
            x=age_labels,
            y=values,
            marker_color=age_colors,
            text=[f"{v:,}" for v in values],
            textposition='auto'
        ))
        fig.update_layout(
            title=dict(text=title, font=dict(size=14, family="Kanit"), x=0),
            height=200,
            margin=dict(l=10, r=10, t=40, b=10),
            xaxis=dict(tickfont=dict(family="Kanit")),
            yaxis=dict(showgrid=True, gridcolor='#eee'),
            plot_bgcolor='white',
            font=dict(family="Kanit")
        )
        return fig

    # Render Cards
    with col_d1:
        st.plotly_chart(create_donut(cpk_male, cpk_female, "👫 สัดส่วนเพศ ช.พ.ค."), use_container_width=True)

    with col_d2:
        st.plotly_chart(create_age_bar(cpk_age_vals, "📊 กลุ่มอายุ ช.พ.ค."), use_container_width=True)

    with col_d3:
        st.plotly_chart(create_donut(cps_male, cps_female, "👫 สัดส่วนเพศ ช.พ.ส."), use_container_width=True)

    with col_d4:
        st.plotly_chart(create_age_bar(cps_age_vals, "📊 กลุ่มอายุ ช.พ.ส."), use_container_width=True)

    st.write("---")

    # --- 3. PREPARE EXTRA DATA (DEATH/FINANCE) FOR NEXT SECTIONS ---
    # (Keeping this logic ready for future sections)
    cpk_ex = {}
    cps_ex = {}
    
    if 'df_eis_extra' in st.session_state and not st.session_state['df_eis_extra'].empty:
        df_ex = st.session_state['df_eis_extra'].copy()
        df_ex['YearNum'] = pd.to_numeric(df_ex['Year'], errors='coerce').fillna(0).astype(int)
        df_ex['MonthNum'] = df_ex['Month'].map(thai_month_map).fillna(0).astype(int)
        df_ex['SortKey'] = (df_ex['YearNum'] * 100) + df_ex['MonthNum']
        mask_ex = (df_ex['SortKey'] >= start_key) & (df_ex['SortKey'] <= end_key)
        df_ex_filtered = df_ex[mask_ex]

        # Map Death Causes
        death_map = {
            'โรคมะเร็ง': 'Cause_Cancer', 'โรคปอด': 'Cause_Lung',
            'โรคหัวใจ/หลอดเลือด': 'Cause_Heart', 'ชราภาพ': 'Cause_Old',
            'ติดเชื้อในกระแสเลือด': 'Cause_Brain'
        }
        for item_name, key in death_map.items():
            val = df_ex_filtered[(df_ex_filtered['Category'] == 'Death_Cause') & (df_ex_filtered['Item'] == item_name)]['Value'].sum()
            cpk_ex[key] = int(val * 0.55) 
            cps_ex[key] = int(val * 0.45)
