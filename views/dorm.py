import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from utils.styles import render_header

def show_view():
    render_header("🏢 หอพัก สกสค. (OTEP Dormitory)", border_color="#8BC34A")
    
    if 'df_dorm' not in st.session_state or st.session_state['df_dorm'].empty:
        st.error("⚠️ ไม่พบข้อมูล Dorm_Data ใน Excel")
        return

    df = st.session_state['df_dorm'].copy()

    # --- FILTER LOGIC ---
    thai_month_map = {
        "มกราคม": 1, "กุมภาพันธ์": 2, "มีนาคม": 3, "เมษายน": 4, "พฤษภาคม": 5, "มิถุนายน": 6,
        "กรกฎาคม": 7, "สิงหาคม": 8, "กันยายน": 9, "ตุลาคม": 10, "พฤศจิกายน": 11, "ธันวาคม": 12
    }
    
    df['YearNum'] = pd.to_numeric(df['Year'], errors='coerce').fillna(0).astype(int)
    df['MonthNum'] = df['Month'].map(thai_month_map).fillna(0).astype(int)
    # Sort for charts
    df['SortKey'] = (df['YearNum'] * 100) + df['MonthNum']

    available_years = sorted(df['Year'].unique(), reverse=True)
    months_list = list(thai_month_map.keys())

    # Create Filter UI
    # Note: Image shows "Date: 08/12/2568" and "Room Type". 
    # We will simulate the date selection using Month/Year for the snapshot.
    c1, c2, c3, c4 = st.columns([1.5, 1.5, 1.5, 3])
    with c1: 
        sel_month = st.selectbox("เดือน (Month)", months_list, index=6) # Default July (has good data in mock)
    with c2: 
        sel_year = st.selectbox("ปี (Year)", available_years, index=0)
    with c3:
        room_type = st.selectbox("ประเภทห้อง (Room Type)", ["ทั้งหมด", "เตียงเดี่ยว", "เตียงคู่", "VIP"])
    with c4:
        st.write("") 
        if st.button("🔍 กรองข้อมูล (Filter)", type="primary"):
            st.rerun()

    # Filter Data
    # 1. Snapshot Data (for Top Cards & Donut Charts)
    snapshot_data = df[(df['Year'] == str(sel_year)) & (df['Month'] == sel_month)]
    
    # 2. Trend Data (for Bottom Charts - Whole Year)
    trend_data = df[df['Year'] == str(sel_year)].sort_values('SortKey')

    if snapshot_data.empty:
        st.warning(f"ไม่พบข้อมูลสำหรับ {sel_month} {sel_year}")
        return

    row = snapshot_data.iloc[0]

    # --- ROW 1: KPI CARDS ---
    st.markdown("##### 🏛️ บทสรุปผู้บริหาร")
    
    # Extract Values
    total_mem = row['Members_Total']
    total_rev = trend_data['Revenue'].sum() # Revenue is usually YTD or Annual sum shown in top? 
    # Image says "Revenue 8.5 M", mock data monthly is ~0.7. Annual sum matches ~8.5.
    # Let's show ANNUAL Revenue for the selected year in the card, as per image likely context.
    
    total_guests = trend_data['Guests'].sum() # Annual Guests
    occupancy_rate = row['Room_Occupied'] # This is % in logic usually, or count. Let's assume % from mock 80
    satisfaction = row['Satisfaction']

    k1, k2, k3, k4, k5 = st.columns(5)

    def kpi(val, label, sub="", color="#333"):
        st.markdown(f"""
        <div style="background:white; padding:15px; border-radius:8px; border:1px solid #eee; text-align:center; box-shadow:0 2px 4px rgba(0,0,0,0.05);">
            <div style="font-size:26px; font-weight:bold; color:{color};">{val}</div>
            <div style="font-size:12px; color:#555; margin-top:5px;">{label}</div>
            <div style="font-size:10px; color:#999;">{sub}</div>
        </div>
        """, unsafe_allow_html=True)

    with k1: kpi(f"{int(total_mem):,} คน", "จำนวนสมาชิก", "ทั้งหมด", "#9C27B0")
    with k2: kpi(f"{total_rev:,.1f} ล้านบาท", "รายรับรวม", f"ปี {sel_year}", "#4CAF50")
    with k3: kpi(f"{int(total_guests):,} ราย", "ผู้เข้าพัก", f"ปี {sel_year}", "#03A9F4")
    with k4: kpi(f"{int(occupancy_rate)}%", "ลูกค้าประจำ", "Occupancy Rate", "#FF9800")
    with k5: kpi(f"{satisfaction}⭐", "ความพึงพอใจ", "เฉลี่ย", "#FFC107")

    st.write("---")

    # --- ROW 2: DONUT CHARTS ---
    c_left, c_right = st.columns(2)

    # Chart 1: Members Breakdown
    with c_left:
        st.markdown(f"**👥 สมาชิกทั้งหมด | {int(total_mem):,} คน**")
        
        labels = ['ครู', 'ขรก.อื่น', 'ทั่วไป']
        values = [row['Mem_Teacher'], row['Mem_Other'], row['Mem_General']]
        colors = ['#00ACC1', '#4CAF50', '#FFC107']
        
        fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.6, marker_colors=colors)])
        fig.update_layout(height=250, margin=dict(l=20,r=20,t=0,b=20), showlegend=True, 
                          legend=dict(orientation="h", yanchor="top", y=-0.1))
        # Add text in center
        # fig.add_annotation(text=f"{int(total_mem):,}", x=0.5, y=0.5, font_size=20, showarrow=False)
        st.plotly_chart(fig, use_container_width=True, key="dorm_donut_1")

    # Chart 2: Room Status (Snapshot)
    with c_right:
        st.markdown(f"**📊 อัตราการใช้ห้องพัก @ {sel_month} {sel_year}**")
        
        labels = ['ใช้งาน', 'ว่าง', 'ปิดซ่อม']
        values = [row['Room_Occupied'], row['Room_Vacant'], row['Room_Maint']]
        colors = ['#00ACC1', '#B2DFDB', '#F44336'] # Blue, Light Blue, Red
        
        fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.6, marker_colors=colors)])
        fig.update_layout(height=250, margin=dict(l=20,r=20,t=0,b=20), showlegend=True,
                          legend=dict(orientation="h", yanchor="top", y=-0.1))
        st.plotly_chart(fig, use_container_width=True, key="dorm_donut_2")

    st.write("---")
    st.markdown(f"##### 📈 ข้อมูลหอพัก (ปี {sel_year})")

    # --- ROW 3: BAR CHARTS (TRENDS) ---
    b1, b2 = st.columns(2)

    # Chart 3: Revenue Trend
    with b1:
        st.markdown("**💰 รายรับแนวโน้มรายเดือน**")
        if not trend_data.empty:
            fig = px.bar(trend_data, x='Month', y='Revenue', 
                         color_discrete_sequence=['#66BB6A'])
            fig.update_layout(height=300, margin=dict(l=0,r=0,t=10,b=0), xaxis_title=None, yaxis_title="ล้านบาท", font_family="Kanit")
            st.plotly_chart(fig, use_container_width=True, key="dorm_trend_rev")

    # Chart 4: Guest Trend
    with b2:
        st.markdown("**👥 ผู้เข้าพักแนวโน้มรายเดือน**")
        if not trend_data.empty:
            fig = px.bar(trend_data, x='Month', y='Guests', 
                         color_discrete_sequence=['#039BE5'])
            fig.update_layout(height=300, margin=dict(l=0,r=0,t=10,b=0), xaxis_title=None, yaxis_title="ราย", font_family="Kanit")
            st.plotly_chart(fig, use_container_width=True, key="dorm_trend_guest")
