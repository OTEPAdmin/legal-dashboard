import streamlit as st
import pandas as pd
import plotly.express as px
from utils.styles import render_header

def show_view():
    render_header("📊 ภาพรวมสำนักอำนวยการ (Director's Office)", border_color="#3F51B5")

    # --- FILTERS (Matching the image design) ---
    months = ["มกราคม", "กุมภาพันธ์", "มีนาคม", "เมษายน", "พฤษภาคม", "มิถุนายน", 
              "กรกฎาคม", "สิงหาคม", "กันยายน", "ตุลาคม", "พฤศจิกายน", "ธันวาคม"]
    years = ["2568", "2567"]
    
    # Check if data exists
    if 'df_admin' not in st.session_state or st.session_state['df_admin'].empty:
        st.error("⚠️ ไม่พบข้อมูล Admin_Data ใน Excel (Please add 'Admin_Data' tab to your file)")
        return

    df = st.session_state['df_admin']

    # Filter UI
    c1, c2, c3, c4, c5 = st.columns([1,1,1,1,1])
    with c1: m_start = st.selectbox("เดือนเริ่มต้น", months, index=0)
    with c2: y_start = st.selectbox("ปีเริ่มต้น", years, index=0)
    with c3: m_end = st.selectbox("ถึงเดือน", months, index=11)
    with c4: y_end = st.selectbox("ถึงปี", years, index=0)
    with c5: 
        st.write("") 
        st.write("") 
        if st.button("🔍 กรองข้อมูล", use_container_width=True):
            st.rerun()

    # --- GET DATA FOR SELECTED MONTH (Currently showing specific month data for Cards) ---
    # For simplicity, we grab the "End Month" data to show on cards, 
    # but the Chart will show the trend.
    current_data = df[(df['Year'] == str(y_end)) & (df['Month'] == m_end)]
    
    if current_data.empty:
        st.warning(f"ไม่พบข้อมูลสำหรับ {m_end} {y_end}")
        # Use zeros if no data
        d = {col: 0 for col in df.columns if col not in ['Year', 'Month']}
    else:
        d = current_data.iloc[0].to_dict()

    st.write("---")

    # --- ROW 1: KPI CARDS ---
    col1, col2, col3, col4, col5 = st.columns(5)

    # Card 1: Complaints (Blue)
    with col1:
        st.markdown(f"""
        <div style="background:white; padding:15px; border-radius:10px; border-top: 5px solid #3F51B5; box-shadow: 0 2px 5px rgba(0,0,0,0.1);">
            <h5 style='margin:0; color:#555;'>📝 เรื่องร้องเรียนทั้งหมด</h5>
            <h2 style='margin:10px 0; font-size: 32px; color:#333;'>{d.get('Complain_Total', 0)} <span style='font-size:14px; color:grey;'>เรื่อง</span></h2>
            <div style="display:flex; justify-content:space-between; font-size:12px;">
                <span style="color:green;">เสร็จสิ้น <b>{d.get('Complain_Done', 0)}</b></span>
                <span style="color:orange;">ระหว่างดำเนินการ <b>{d.get('Complain_Pending', 0)}</b></span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Card 2: Vehicles (Red/Orange)
    with col2:
        st.markdown(f"""
        <div style="background:white; padding:15px; border-radius:10px; border-top: 5px solid #F44336; box-shadow: 0 2px 5px rgba(0,0,0,0.1);">
            <h5 style='margin:0; color:#555;'>🚗 ข้อมูลรถส่วนกลาง</h5>
            <h2 style='margin:10px 0; font-size: 32px; color:#333;'>{d.get('Car_Total', 0)} <span style='font-size:14px; color:grey;'>คัน</span></h2>
             <div style="display:flex; justify-content:space-between; font-size:12px;">
                <span style="color:green;">ใช้งานได้ <b>{d.get('Car_Active', 0)}</b></span>
                <span style="color:red;">ชำรุด <b>{d.get('Car_Repair', 0)}</b></span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Card 3: Website (Purple)
    with col3:
        st.markdown(f"""
        <div style="background:white; padding:15px; border-radius:10px; border-top: 5px solid #9C27B0; box-shadow: 0 2px 5px rgba(0,0,0,0.1);">
            <h5 style='margin:0; color:#555;'>🌐 การเข้าชมเว็บไซต์</h5>
            <h2 style='margin:10px 0; font-size: 32px; color:#333;'>{d.get('Web_Visits', 0):,} <span style='font-size:14px; color:grey;'>ครั้ง</span></h2>
             <div style="display:flex; justify-content:space-between; font-size:10px; color:#777;">
                <span>มือถือ {d.get('Web_Mobile', 0)}%</span>
                <span>PC {d.get('Web_PC', 0)}%</span>
                <span>แท็บเล็ต {d.get('Web_Tablet', 0)}%</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Card 4: Facebook (Blue)
    with col4:
        st.markdown(f"""
        <div style="background:white; padding:15px; border-radius:10px; border-top: 5px solid #2196F3; box-shadow: 0 2px 5px rgba(0,0,0,0.1);">
            <h5 style='margin:0; color:#555;'>📘 Facebook Followers</h5>
            <h2 style='margin:10px 0; font-size: 32px; color:#333;'>{d.get('FB_Followers', 0):,} <span style='font-size:14px; color:grey;'>คน</span></h2>
            <div style="height:18px;"></div>
        </div>
        """, unsafe_allow_html=True)
        
    # Card 5: LINE (Green)
    with col5:
        st.markdown(f"""
        <div style="background:white; padding:15px; border-radius:10px; border-top: 5px solid #4CAF50; box-shadow: 0 2px 5px rgba(0,0,0,0.1);">
            <h5 style='margin:0; color:#555;'>💬 LINE OA</h5>
            <h2 style='margin:10px 0; font-size: 32px; color:#333;'>{d.get('Line_Followers', 0):,} <span style='font-size:14px; color:grey;'>คน</span></h2>
            <div style="height:18px;"></div>
        </div>
        """, unsafe_allow_html=True)

    st.write("---")
    st.markdown("### 📈 ข้อมูลช่องทางดิจิทัล (Phase 1)")

    # --- ROW 2: CHARTS ---
    gc1, gc2 = st.columns([2, 1]) # 2/3 width for chart, 1/3 for summary

    # Left: Line Chart (Trend)
    with gc1:
        st.markdown("##### 📉 LINE Official - แนวโน้มการเพิ่มเพื่อน (รายเดือน)")
        
        # Prepare data for chart (Filter by selected year)
        df_chart = df[df['Year'] == str(y_end)].copy()
        
        # Sort by month index to ensure correct order
        month_order = {m: i for i, m in enumerate(months)}
        df_chart['month_num'] = df_chart['Month'].map(month_order)
        df_chart = df_chart.sort_values('month_num')
        
        if not df_chart.empty:
            fig = px.line(df_chart, x='Month', y='Line_New', markers=True, 
                          labels={'Line_New': 'จำนวนเพิ่มเพื่อน', 'Month': 'เดือน'})
            fig.update_traces(line_color='#00C853', line_width=3, marker_size=8)
            fig.update_layout(height=350, xaxis_title=None, yaxis_title=None, 
                              margin=dict(l=20, r=20, t=20, b=20), font_family="Kanit")
            st.plotly_chart(fig, use_container_width=True, key="line_chart_admin")
        else:
            st.info("ไม่มีข้อมูลกราฟสำหรับปีที่เลือก")

    # Right: Summary Grid
    with gc2:
        st.markdown("##### 📊 สรุปช่องทางดิจิทัล")
        
        # Helper function for mini cards
        def mini_card(icon, label, value, unit, color="#eee"):
            st.markdown(f"""
            <div style="display:flex; align-items:center; background:#F8F9FA; padding:10px; border-radius:8px; margin-bottom:10px;">
                <div style="font-size:24px; margin-right:15px;">{icon}</div>
                <div>
                    <div style="font-size:12px; color:#666;">{label}</div>
                    <div style="font-size:18px; font-weight:bold; color:#333;">{value:,} <span style="font-size:10px; font-weight:normal;">{unit}</span></div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        r1, r2 = st.columns(2)
        with r1:
            mini_card("🌐", "Website", d.get('Web_Visits', 0), "ครั้ง")
            mini_card("💬", "LINE", d.get('Line_Followers', 0), "ราย")
            mini_card("🎵", "TikTok", d.get('Tiktok_Followers', 0), "ราย")
        with r2:
            mini_card("📘", "FB Page", d.get('FB_Followers', 0), "ราย")
            mini_card("📺", "LINE VOOM", d.get('Line_Voom', 0), "ราย")
            mini_card("▶️", "YouTube", d.get('Youtube_Followers', 0), "ราย")
