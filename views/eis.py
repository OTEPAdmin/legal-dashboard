# At the top
from utils.config_manager import is_feature_visible

# ... (Inside show_view) ...

    # =================================================================================================
    # SECTION 1: EXECUTIVE SUMMARY
    # =================================================================================================
    if is_feature_visible("EIS_Executive_Summary"):
        st.markdown("#### 📊 บทสรุปผู้บริหาร")
        # ... (Rest of Section 1 code) ...
        # ...
        st.write("---")

    # =================================================================================================
    # SECTION 2: DEMOGRAPHICS
    # =================================================================================================
    if is_feature_visible("EIS_Demographics"):
        st.markdown("#### 👥 ข้อมูลสมาชิก | DEMOGRAPHIC")
        # ... (Rest of Section 2 code) ...
        # ...
        st.write("---")
        
    # =================================================================================================
    # SECTION 3: DEATH STATS
    # =================================================================================================
    if is_feature_visible("EIS_Death_Stats"):
        st.markdown("#### ☠️ สาเหตุการเสียชีวิต | CAUSES OF DEATH")
        # ... (Rest of Section 3 code) ...
        # ...
        st.write("---")

    # =================================================================================================
    # SECTION 4: FINANCIALS
    # =================================================================================================
    if is_feature_visible("EIS_Financials"):
        st.markdown("#### 💸 การนำส่งเงิน & งบการเงิน")
        # ... (Rest of Section 4 code) ...import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import random # For trend simulation
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

    latest_key = df_filtered['SortKey'].max()
    df_snap = df_filtered[df_filtered['SortKey'] == latest_key]
    
    def get_snap(cat, item):
        return df_snap[(df_snap['Category'] == cat) & (df_snap['Item'] == item)]['Value'].sum()

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
    # SECTION 1: EXECUTIVE SUMMARY
    # =================================================================================================
    st.markdown("#### 📊 บทสรุปผู้บริหาร")

    col_cpk, col_cps = st.columns(2)

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
        </div>
        """, unsafe_allow_html=True)

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
        </div>
        """, unsafe_allow_html=True)

    st.write("")

    # BAR CHARTS
    def create_horiz_bar(values, labels, colors, title):
        fig = go.Figure(go.Bar(
            x=values, y=labels, orientation='h', marker_color=colors,
            text=[f"{v:,}" for v in values], textposition='inside', insidetextanchor='middle'
        ))
        fig.update_layout(
            title=dict(text=title, font=dict(size=14, family="Kanit"), x=0),
            height=150, margin=dict(l=0, r=0, t=30, b=0),
            xaxis=dict(showgrid=False, showticklabels=False), yaxis=dict(showgrid=False),
            plot_bgcolor='rgba(0,0,0,0)', font=dict(family="Kanit")
        )
        return fig

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        val_apply = int(cpk_new_total * 0.85)
        fig = create_horiz_bar([cpk_new_total - val_apply, val_apply], ['ขอกลับ', 'สมัคร'], ['#00ACC1', '#4CAF50'], "📈 สมาชิกเพิ่ม ช.พ.ค.")
        st.plotly_chart(fig, use_container_width=True)
    with c2:
        val_dead = int(cpk_dead_val)
        val_wd = int(cpk_resign_val * 0.5)
        val_res = int(cpk_resign_val * 0.3)
        fig = create_horiz_bar([cpk_resign_val-val_wd-val_res, val_dead, val_res, val_wd], ['อื่นๆ', 'ตาย', 'ลาออก', 'ถอนชื่อ'], ['#9E9E9E', '#E53935', '#8E24AA', '#FFB300'], "📉 จำหน่าย ช.พ.ค.")
        st.plotly_chart(fig, use_container_width=True)
    with c3:
        val_apply = int(cps_new_total * 0.82)
        fig = create_horiz_bar([cps_new_total - val_apply, val_apply], ['ขอกลับ', 'สมัคร'], ['#AB47BC', '#66BB6A'], "📈 สมาชิกเพิ่ม ช.พ.ส.")
        st.plotly_chart(fig, use_container_width=True)
    with c4:
        val_dead = int(cps_dead_val)
        val_wd = int(cps_resign_val * 0.5)
        val_res = int(cps_resign_val * 0.3)
        fig = create_horiz_bar([cps_resign_val-val_wd-val_res, val_dead, val_res, val_wd], ['อื่นๆ', 'ตาย', 'ลาออก', 'ถอนชื่อ'], ['#9E9E9E', '#E53935', '#00ACC1', '#FFB300'], "📉 จำหน่าย ช.พ.ส.")
        st.plotly_chart(fig, use_container_width=True)

    st.write("---")

    # =================================================================================================
    # SECTION 2: MEMBER DEMOGRAPHICS
    # =================================================================================================
    st.markdown("#### 👥 ข้อมูลสมาชิก | DEMOGRAPHIC")
    
    cpk_male = int(cpk_total * 0.38)
    cps_male = int(cps_total * 0.42)
    cpk_age_vals = [int(cpk_total*x) for x in [0.08, 0.18, 0.32, 0.28, 0.14]]
    cps_age_vals = [int(cps_total*x) for x in [0.05, 0.12, 0.25, 0.35, 0.23]]
    age_labels = ['<40', '40-49', '50-59', '60-69', '≥70']
    age_colors = ['#29B6F6', '#66BB6A', '#FBC02D', '#AB47BC', '#FF7043']

    col_d1, col_d2, col_d3, col_d4 = st.columns(4)

    def create_donut(male, female, title):
        fig = go.Figure(data=[go.Pie(labels=['ชาย', 'หญิง'], values=[male, female], hole=.5, marker_colors=['#29B6F6', '#EC407A'], sort=False)])
        fig.update_layout(title=dict(text=title, font=dict(family="Kanit", size=14)), height=200, margin=dict(t=40, b=10, l=10, r=10), showlegend=True, legend=dict(orientation="h", y=-0.1))
        return fig

    def create_age_bar(vals, title):
        fig = go.Figure(go.Bar(x=age_labels, y=vals, marker_color=age_colors, text=[f"{v:,}" for v in vals], textposition='auto'))
        fig.update_layout(title=dict(text=title, font=dict(family="Kanit", size=14)), height=200, margin=dict(t=40, b=10, l=10, r=10), plot_bgcolor='white')
        return fig

    with col_d1: st.plotly_chart(create_donut(cpk_male, cpk_total-cpk_male, "👫 สัดส่วนเพศ ช.พ.ค."), use_container_width=True)
    with col_d2: st.plotly_chart(create_age_bar(cpk_age_vals, "📊 กลุ่มอายุ ช.พ.ค."), use_container_width=True)
    with col_d3: st.plotly_chart(create_donut(cps_male, cps_total-cps_male, "👫 สัดส่วนเพศ ช.พ.ส."), use_container_width=True)
    with col_d4: st.plotly_chart(create_age_bar(cps_age_vals, "📊 กลุ่มอายุ ช.พ.ส."), use_container_width=True)

    st.write("---")

    # =================================================================================================
    # SECTION 3: CAUSES OF DEATH
    # =================================================================================================
    st.markdown("#### ☠️ สาเหตุการเสียชีวิต | CAUSES OF DEATH")

    cpk_death_data = {}
    cps_death_data = {}
    
    # Financial data preparation for next section
    cpk_remit_total = 0
    cps_remit_total = 0
    
    if 'df_eis_extra' in st.session_state and not st.session_state['df_eis_extra'].empty:
        df_ex = st.session_state['df_eis_extra'].copy()
        df_ex['YearNum'] = pd.to_numeric(df_ex['Year'], errors='coerce').fillna(0).astype(int)
        df_ex['MonthNum'] = df_ex['Month'].map(thai_month_map).fillna(0).astype(int)
        df_ex['SortKey'] = (df_ex['YearNum'] * 100) + df_ex['MonthNum']
        df_ex_filtered = df_ex[(df_ex['SortKey'] >= start_key) & (df_ex['SortKey'] <= end_key)]

        # Death Data
        death_mapping = [('โรคมะเร็ง', 'โรคมะเร็ง'), ('โรคปอด', 'โรคปอด'), ('โรคหัวใจ/หลอดเลือด', 'โรคหัวใจ'), ('ชราภาพ', 'โรคชรา'), ('ติดเชื้อในกระแสเลือด', 'โรคสมอง')]
        for db_key, label in death_mapping:
            val = df_ex_filtered[(df_ex_filtered['Category'] == 'Death_Cause') & (df_ex_filtered['Item'] == db_key)]['Value'].sum()
            cpk_death_data[label] = int(val * 0.55)
            cps_death_data[label] = int(val * 0.45)
            
        # Financial Data
        cpk_remit_total = df_ex_filtered[(df_ex_filtered['Category'] == 'Remittance') & (df_ex_filtered['Item'] == 'เงินนำส่ง ช.พ.ค.')]['Value'].sum() * 1000000 # Convert M to unit if needed (Mocking scale)
        cps_remit_total = df_ex_filtered[(df_ex_filtered['Category'] == 'Remittance') & (df_ex_filtered['Item'] == 'เงินนำส่ง ช.พ.ส.')]['Value'].sum() * 1000000

    col_death1, col_death2 = st.columns(2)
    death_colors = ['#FF7043', '#29B6F6', '#AB47BC', '#FFCA28', '#66BB6A'] 
    death_labels = ['โรคมะเร็ง', 'โรคปอด', 'โรคหัวใจ', 'โรคชรา', 'โรคสมอง']

    def create_death_bar(data, title):
        vals = [data.get(l, 0) for l in death_labels]
        fig = go.Figure(go.Bar(x=vals, y=death_labels, orientation='h', marker_color=death_colors, text=[f"{v:,} ราย" for v in vals], textposition='outside'))
        fig.update_layout(title=dict(text=title, font=dict(family="Kanit", size=14)), height=300, margin=dict(r=50), yaxis=dict(autorange="reversed"))
        return fig

    with col_death1: st.plotly_chart(create_death_bar(cpk_death_data, "📊 5 อันดับสาเหตุการเสียชีวิต ช.พ.ค."), use_container_width=True)
    with col_death2: st.plotly_chart(create_death_bar(cps_death_data, "📊 5 อันดับสาเหตุการเสียชีวิต ช.พ.ส."), use_container_width=True)

    st.write("---")

    # =================================================================================================
    # SECTION 4: FINANCIAL & REMITTANCE (การนำส่งเงิน & งบการเงิน)
    # =================================================================================================
    st.markdown("#### 💸 การนำส่งเงิน & งบการเงิน | FINANCIAL & REMITTANCE")

    c_fin1, c_fin2 = st.columns(2)

    # Helper for the 3-colored Card
    def render_fin_group(title, dead_count, per_body, total_fam, bg_color):
        st.markdown(f"""
        <div style="background-color:{bg_color}; padding:15px; border-radius:10px; font-family: 'Kanit', sans-serif; margin-bottom: 10px;">
            <div style="font-weight:bold; color:#555; margin-bottom:10px;">💰 {title}</div>
            <div style="display:flex; gap:10px;">
                <div style="flex:1; background:#0288D1; color:white; padding:10px; border-radius:8px; text-align:center;">
                    <div style="font-size:10px;">จำนวนผู้วายชนม์</div>
                    <div style="font-size:20px; font-weight:bold;">{int(dead_count):,} ราย</div>
                </div>
                <div style="flex:1; background:#43A047; color:white; padding:10px; border-radius:8px; text-align:center;">
                    <div style="font-size:10px;">เงินสงเคราะห์รายศพ</div>
                    <div style="font-size:20px; font-weight:bold;">{int(per_body):,}.-</div>
                </div>
                <div style="flex:1.2; background:#FBC02D; color:white; padding:10px; border-radius:8px; text-align:center;">
                    <div style="font-size:10px;">เงินสงเคราะห์ครอบครัว</div>
                    <div style="font-size:20px; font-weight:bold;">{int(total_fam):,}-.</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Helper for Status Row
    def render_status_row(paid_pct, pending_pct, rank):
        paid_count = int(paid_pct * 15000) # Mock scale
        pending_count = int(pending_pct * 15000)
        st.markdown(f"""
        <div style="background:white; border:1px solid #eee; padding:15px; border-radius:10px; font-family: 'Kanit', sans-serif; display:flex; justify-content:space-between; text-align:center;">
            <div style="flex:1;">
                <div style="color:#43A047; font-size:12px; font-weight:bold;">✅ นำส่งภายในกำหนด</div>
                <div style="font-size:24px; font-weight:bold; color:#43A047;">{paid_pct}%</div>
                <div style="font-size:10px; color:#999;">{paid_count:,} ราย</div>
            </div>
            <div style="flex:1; border-left:1px solid #eee; border-right:1px solid #eee;">
                <div style="color:#FBC02D; font-size:12px; font-weight:bold;">⚠️ ค้างชำระ</div>
                <div style="font-size:24px; font-weight:bold; color:#FBC02D;">{pending_pct}%</div>
                <div style="font-size:10px; color:#999;">{pending_count:,} ราย</div>
            </div>
            <div style="flex:1;">
                <div style="color:#AB47BC; font-size:12px; font-weight:bold;">🏆 จังหวัดนำส่งภายในกำหนด</div>
                <div style="font-size:24px; font-weight:bold; color:#AB47BC;">{rank}/77</div>
                <div style="font-size:10px; color:#999;">จังหวัด</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Helper for Line Chart
    def create_trend_chart(color_hex, title):
        # Generate mock trend data based on selected range
        dates = pd.date_range(start=f"2024-{thai_month_map[m_start]:02d}-01", periods=10, freq='M')
        months_label = [f"งวด {i+1}" for i in range(len(dates))]
        values = [random.uniform(88, 95) for _ in range(len(dates))]
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=months_label, y=values, mode='lines+markers', line=dict(color=color_hex, width=3, shape='spline'), marker=dict(size=8)))
        fig.update_layout(
            title=dict(text=title, font=dict(family="Kanit", size=14)),
            height=200, margin=dict(l=20, r=20, t=40, b=20),
            yaxis=dict(range=[85, 100], showgrid=True, gridcolor='#eee'),
            plot_bgcolor='rgba(245, 245, 245, 0.5)'
        )
        return fig

    # --- LEFT COLUMN: CPK ---
    with c_fin1:
        # 1. Cards
        cpk_deceased = int(cpk_dead_val)
        cpk_per_body = 200000 # Mock Rate
        cpk_family = max(0, cpk_remit_total - (cpk_deceased * cpk_per_body)) # Logic: Remit - Funeral = Family
        render_fin_group("เงินสงเคราะห์ ช.พ.ค.", cpk_deceased, cpk_per_body, cpk_family, "#E0F7FA")
        
        # 2. Status
        render_status_row(90.64, 9.36, 66)
        
        # 3. Chart
        st.plotly_chart(create_trend_chart("#00BCD4", "📈 แนวโน้มอัตราการชำระ ช.พ.ค."), use_container_width=True)

    # --- RIGHT COLUMN: CPS ---
    with c_fin2:
        # 1. Cards
        cps_deceased = int(cps_dead_val)
        cps_per_body = 180000 # Mock Rate
        cps_family = max(0, cps_remit_total - (cps_deceased * cps_per_body))
        render_fin_group("เงินสงเคราะห์ ช.พ.ส.", cps_deceased, cps_per_body, cps_family, "#F3E5F5")
        
        # 2. Status
        render_status_row(91.25, 8.75, 71)
        
        # 3. Chart
        st.plotly_chart(create_trend_chart("#AB47BC", "📈 แนวโน้มอัตราการชำระ ช.พ.ส."), use_container_width=True)
