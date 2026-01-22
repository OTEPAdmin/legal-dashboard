import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from utils.styles import render_header

def show_view():
    render_header("🎁 สวัสดิการ (Welfare)", border_color="#8BC34A")
    
    if 'df_welfare' not in st.session_state or st.session_state['df_welfare'].empty:
        st.error("⚠️ ไม่พบข้อมูล Welfare_Data ใน Excel")
        return

    df = st.session_state['df_welfare'].copy()

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

    # --- KPI DATA (Snapshot Logic) ---
    # For these KPIs (Counts), we take the value from the LATEST month selected.
    start_key = (int(y_start) * 100) + thai_month_map[m_start]
    end_key = (int(y_end) * 100) + thai_month_map[m_end]
    
    mask = (df['SortKey'] >= start_key) & (df['SortKey'] <= end_key)
    df_filtered = df[mask]
    
    if df_filtered.empty:
        st.warning(f"ไม่พบข้อมูลในช่วงเวลา: {m_start} {y_start} - {m_end} {y_end}")
        return

    # Get latest snapshot
    latest_key = df_filtered['SortKey'].max()
    df_snap = df_filtered[df_filtered['SortKey'] == latest_key]

    def get_val(cat, item, col='Value_1'):
        val = df_snap[(df_snap['Category'] == cat) & (df_snap['Item'] == item)][col].sum()
        return int(val)

    shop_cnt = get_val('Shop', 'Count')
    shop_prov = get_val('Shop', 'Count', 'Value_2')
    scholar_cnt = get_val('Scholarship', 'Count')
    scholar_avg = get_val('Scholarship', 'Count', 'Value_2')
    club_mem = get_val('Club', 'Members')
    award_pra = get_val('Award_Prawa', 'Count')
    award_good = get_val('Award_Good', 'Count')

    # --- UI ROW 1: CARDS ---
    c1, c2, c3, c4, c5 = st.columns(5)
    
    def w_card(icon, title, val, unit, subtext, color="#333"):
        st.markdown(f"""
        <div style="background:white; padding:15px; border-radius:10px; border:1px solid #eee; box-shadow: 0 2px 5px rgba(0,0,0,0.05); text-align:center; height:140px;">
            <div style="font-size:14px; font-weight:bold; color:#555; margin-bottom:10px;">{icon} {title}</div>
            <div style="font-size:28px; font-weight:bold; color:{color};">{val:,}</div>
            <div style="font-size:12px; color:#777;">{unit}</div>
            <div style="font-size:11px; color:#999; margin-top:5px;">{subtext}</div>
        </div>
        """, unsafe_allow_html=True)

    with c1: w_card("🏪", "ร้านค้าสวัสดิการ", shop_cnt, "ร้านค้าทั่วประเทศ", f"{shop_prov} จังหวัด", "#0288D1") # Blue
    with c2: w_card("🎓", "ทุนการศึกษา", scholar_cnt, "ทุน", f"เฉลี่ย {scholar_avg:,} บาท/ทุน", "#43A047") # Green
    with c3: w_card("👥", "สมาชิกชมรม", club_mem, "ราย", "2 ชมรม ทั่วประเทศ", "#8E24AA") # Purple
    with c4: w_card("🏆", "รางวัลพระพฤหัสบดี", award_pra, "รางวัล", "3 ระดับ", "#FBC02D") # Yellow
    with c5: w_card("⭐", "คนดีศรีสกสค.", award_good, "ราย", "ผู้ได้รับการยกย่อง", "#E53935") # Red

    st.write("---")
    st.markdown("##### 🎁 สวัสดิการครู (ส่วนลด + ทุน + รางวัล)")

    # --- CHART DATA PREP (Yearly Trends) ---
    # We aggregate data by Year from the FULL dataset (df) to show trends (2566, 2567, 2568)
    # We take the MAX value of each year (assuming it grows or is a cumulative count for that year)
    df_trend = df.groupby(['Year', 'Category', 'Item'])['Value_1'].max().reset_index()
    
    # Filter only relevant years for cleaner chart
    years_to_show = ['2566', '2567', '2568']
    df_trend = df_trend[df_trend['Year'].isin(years_to_show)]

    # Helper to get year values list
    def get_trend_vals(cat, item):
        data = df_trend[(df_trend['Category'] == cat) & (df_trend['Item'] == item)].sort_values('Year')
        return data['Year'].tolist(), data['Value_1'].tolist()

    # --- UI ROW 2: CHARTS ---
    col1, col2, col3 = st.columns(3)

    # Chart 1: Shops (Blue)
    with col1:
        st.markdown("**🏪 ร้านค้าสวัสดิการ**")
        x_shop, y_shop = get_trend_vals('Shop', 'Count')
        if x_shop:
            fig = go.Figure(go.Bar(x=x_shop, y=y_shop, marker_color='#0288D1'))
            fig.update_layout(height=250, margin=dict(l=20,r=20,t=10,b=20), font_family="Kanit")
            st.plotly_chart(fig, use_container_width=True, key="w_chart_shop")

    # Chart 2: Scholarships (Green)
    with col2:
        st.markdown("**🎓 ทุนการศึกษา**")
        x_sch, y_sch = get_trend_vals('Scholarship', 'Count')
        if x_sch:
            fig = go.Figure(go.Bar(x=x_sch, y=y_sch, marker_color='#43A047')) # Green
            fig.update_layout(height=250, margin=dict(l=20,r=20,t=10,b=20), font_family="Kanit")
            st.plotly_chart(fig, use_container_width=True, key="w_chart_sch")

    # Chart 3: Awards (Yellow)
    with col3:
        st.markdown("**🏆 รางวัลพระพฤหัสบดี**")
        x_aw, y_aw = get_trend_vals('Award_Prawa', 'Count')
        if x_aw:
            fig = go.Figure(go.Bar(x=x_aw, y=y_aw, marker_color='#FBC02D')) # Yellow
            fig.update_layout(height=250, margin=dict(l=20,r=20,t=10,b=20), font_family="Kanit")
            st.plotly_chart(fig, use_container_width=True, key="w_chart_aw")
