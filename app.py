import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# --- 1. CONFIG & SETTINGS ---
st.set_page_config(page_title="EIS Executive Platform", layout="wide")

# --- 2. THEME & CUSTOM CSS ---
st.markdown("""
    <link href="https://fonts.googleapis.com/css2?family=Sarabun:wght@300;400;700&display=swap" rel="stylesheet">
    <style>
        html, body, [class*="css"] { font-family: 'Sarabun', sans-serif !important; }
        .executive-header { background-color: #f1f3f4; padding: 10px 20px; border-radius: 5px; margin-bottom: 20px; border-left: 8px solid #5f6368; }
        .finance-card { padding: 15px; border-radius: 10px; color: white; text-align: center; margin-bottom: 10px; }
        .sub-header { background-color: #e8f0fe; padding: 5px 15px; border-radius: 5px; margin: 15px 0; border-left: 5px solid #1a73e8; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. SESSION STATE ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.role = None

# --- 4. PAGE: EIS DASHBOARD (หน้าสมบูรณ์) ---
def show_eis_dashboard():
    # Header & Filters
    st.markdown('<div class="executive-header"><h2>📊 บทสรุปผู้บริหาร (Executive Summary)</h2></div>', unsafe_allow_html=True)
    
    with st.container():
        f1, f2, f3, f4 = st.columns(4)
        f1.selectbox("ช่วงเวลา", ["พฤศจิกายน", "ธันวาคม"], index=0)
        f2.selectbox("ปี", ["2568", "2567"], index=0)
        st.write("<br>", unsafe_allow_html=True)
    
    # --- ส่วนที่ 1: ภาพรวมสมาชิก (จากไฟล์ image_10ab00.png) ---
    st.markdown("### 👥 ข้อมูลสมาชิก | DEMOGRAPHIC")
    # (โค้ดส่วนสถิติสมาชิกเดิมที่เคยทำไว้...)
    st.info("ส่วนแสดงสถิติสมาชิก ช.พ.ค. / ช.พ.ส. (ข้ามโค้ดส่วนนี้เพื่อความกระชับ)")

    # --- ส่วนที่ 2: การนำส่งเงิน & งบการเงิน (ใหม่จากไฟล์ image_10c166.png) ---
    st.markdown('<div class="sub-header">💳 การนำส่งเงิน & งบการเงิน (ประจำงวด พฤศจิกายน 2568)</div>', unsafe_allow_html=True)
    
    # --- เงินสงเคราะห์ Section ---
    col_fin1, col_fin2 = st.columns(2)
    
    with col_fin1:
        st.caption("💰 เงินสงเคราะห์ ช.พ.ค.")
        c1, c2, c3 = st.columns(3)
        c1.markdown('<div class="finance-card" style="background-color:#0097a7;"><h4>879 ราย</h4><p>จำนวนผู้ตาย</p></div>', unsafe_allow_html=True)
        c2.markdown('<div class="finance-card" style="background-color:#43a047;"><h4>879.-</h4><p>เงินสงเคราะห์รายศพ</p></div>', unsafe_allow_html=True)
        c3.markdown('<div class="finance-card" style="background-color:#fbc02d; color:black;"><h4>900,000.-</h4><p>เงินสงเคราะห์ครอบครัว</p></div>', unsafe_allow_html=True)
        
        st.write("**สถานะการนำส่งเงิน ช.พ.ค.**")
        sc1, sc2, sc3 = st.columns(3)
        sc1.metric("นำส่งภายในกำหนด", "90.64%", "834,394 ราย")
        sc2.metric("ค้างชำระ", "9.36%", "-84,478 ราย", delta_color="inverse")
        sc3.metric("จังหวัดนำส่งครบ", "66/77", "จังหวัด")

    with col_fin2:
        st.caption("💰 เงินสงเคราะห์ ช.พ.ส.")
        c1, c2, c3 = st.columns(3)
        c1.markdown('<div class="finance-card" style="background-color:#0097a7;"><h4>383 ราย</h4><p>จำนวนผู้ตาย</p></div>', unsafe_allow_html=True)
        c2.markdown('<div class="finance-card" style="background-color:#43a047;"><h4>383.-</h4><p>เงินสงเคราะห์รายศพ</p></div>', unsafe_allow_html=True)
        c3.markdown('<div class="finance-card" style="background-color:#fbc02d; color:black;"><h4>368,311.-</h4><p>เงินสงเคราะห์ครอบครัว</p></div>', unsafe_allow_html=True)

        st.write("**สถานะการนำส่งเงิน ช.พ.ส.**")
        sc1, sc2, sc3 = st.columns(3)
        sc1.metric("นำส่งภายในกำหนด", "91.25%", "357,178 ราย")
        sc2.metric("ค้างชำระ", "8.75%", "-35,565 ราย", delta_color="inverse")
        sc3.metric("จังหวัดนำส่งครบ", "71/77", "จังหวัด")

    # --- แนวโน้มอัตราการชำระ (Line Charts) ---
    st.write("<br>", unsafe_allow_html=True)
    col_graph1, col_graph2 = st.columns(2)
    
    # Mock Data สำหรับกราฟเส้น
    months = [f"งวด {i}" for i in range(1, 11)]
    pay_rate_chk = [87.5, 87.8, 89.5, 89.1, 90, 90.5, 90.2, 90.8, 90.5, 90.9]
    pay_rate_chs = [88.2, 89.3, 92.8, 94.2, 94, 90.8, 89.5, 93.5, 92.1, 92.8]

    with col_graph1:
        st.write("**📈 แนวโน้มอัตราการชำระ ช.พ.ค. ปี 2568**")
        fig1 = px.line(x=months, y=pay_rate_chk, markers=True)
        fig1.update_traces(line_color='#0097a7', fill='tozeroy')
        fig1.update_layout(height=300, yaxis_range=[85, 95], font_family="Sarabun", xaxis_title=None, yaxis_title="เปอร์เซ็นต์")
        st.plotly_chart(fig1, use_container_width=True)

    with col_graph2:
        st.write("**📈 แนวโน้มอัตราการชำระ ช.พ.ส. ปี 2568**")
        fig2 = px.line(x=months, y=pay_rate_chs, markers=True)
        fig2.update_traces(line_color='#8e24aa', fill='tozeroy')
        fig2.update_layout(height=300, yaxis_range=[85, 98], font_family="Sarabun", xaxis_title=None, yaxis_title="เปอร์เซ็นต์")
        st.plotly_chart(fig2, use_container_width=True)

# --- 5. MAIN LOGIC (เหมือนเดิม) ---
if not st.session_state.get('logged_in'):
    # แสดงหน้า Login (จากโค้ดเดิม)
    st.title("🏛️ EIS Platform Login")
    if st.button("คลิกเพื่อเข้าสู่ระบบ (Demo Mode)"):
        st.session_state.logged_in = True
        st.session_state.role = "Admin"
        st.rerun()
else:
    show_eis_dashboard()
