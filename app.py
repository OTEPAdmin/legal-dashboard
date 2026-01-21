import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# --- 1. CONFIG & STYLE ---
st.set_page_config(page_title="Legal & EIS Platform", layout="wide")

st.markdown("""
    <link href="https://fonts.googleapis.com/css2?family=Sarabun:wght@300;400;700&display=swap" rel="stylesheet">
    <style>
        html, body, [class*="css"] { font-family: 'Sarabun', sans-serif !important; }
        .executive-header { background-color: #f1f3f4; padding: 15px; border-radius: 5px; border-left: 8px solid #5f6368; margin-bottom: 20px; }
        .kpi-card { background-color: white; padding: 20px; border-radius: 10px; border: 1px solid #e0e0e0; text-align: center; }
        .finance-card { padding: 15px; border-radius: 10px; color: white; text-align: center; font-weight: bold; }
        .login-box { max-width: 400px; margin: auto; padding: 2rem; background: #f8f9fa; border-radius: 15px; border: 1px solid #dee2e6; }
        .sub-section { background-color: #e8f0fe; padding: 8px 15px; border-radius: 5px; border-left: 5px solid #1a73e8; font-weight: bold; margin: 20px 0 10px 0; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. SESSION STATE ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.role = None
    st.session_state.name = ""

# --- 3. LOGIN PAGE ---
def login_page():
    st.write("<br><br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 1.5, 1])
    with col2:
        st.markdown('<div class="login-box">', unsafe_allow_html=True)
        st.markdown("<h2 style='text-align: center;'>🏛️ EIS Platform Login</h2>", unsafe_allow_html=True)
        user = st.text_input("Username")
        pw = st.text_input("Password", type="password")
        if st.button("เข้าสู่ระบบ", use_container_width=True):
            if user == "admin" and pw == "admin123":
                st.session_state.logged_in, st.session_state.role, st.session_state.name = True, "Admin", "ผู้ดูแลระบบ"
                st.rerun()
            elif user == "user" and pw == "user123":
                st.session_state.logged_in, st.session_state.role, st.session_state.name = True, "User", "เจ้าหน้าที่"
                st.rerun()
            else:
                st.error("Username หรือ Password ไม่ถูกต้อง")
        st.markdown('</div>', unsafe_allow_html=True)

# --- 4. PAGE: EIS DASHBOARD (Member Stats + Finance) ---
def show_eis_dashboard():
    st.markdown('<div class="executive-header"><h2>📊 บทสรุปผู้บริหาร (Executive Summary)</h2></div>', unsafe_allow_html=True)
    
    # Filter Section
    with st.container():
        f1, f2, f3, f4 = st.columns([1.5, 1, 1.5, 1])
        f1.selectbox("ช่วงเวลา", ["พฤศจิกายน", "ธันวาคม"], index=0)
        f2.selectbox("ปี", ["2568", "2567"], index=0)
    
    # --- PART 1: MEMBER STATISTICS ---
    st.markdown('<div class="sub-section">👥 ข้อมูลสมาชิก | DEMOGRAPHIC</div>', unsafe_allow_html=True)
    
    kpi_col1, kpi_col2 = st.columns(2)
    with kpi_col1:
        st.markdown('<div class="kpi-card" style="border-top: 5px solid #00acc1;"><h4>ช.พ.ค.</h4><h2>933,962</h2><p style="color:green;">+12,456 เพิ่ม | <span style="color:red;">-8,967 จำหน่าย</span></p></div>', unsafe_allow_html=True)
    with kpi_col2:
        st.markdown('<div class="kpi-card" style="border-top: 5px solid #e91e63;"><h4>ช.พ.ส.</h4><h2>287,654</h2><p style="color:green;">+4,532 เพิ่ม | <span style="color:red;">-5,234 จำหน่าย</span></p></div>', unsafe_allow_html=True)

    # Demographic Charts
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.plotly_chart(px.pie(values=[38, 62], names=["ชาย", "หญิง"], hole=0.7, title="เพศ ช.พ.ค.").update_layout(height=250, showlegend=False), use_container_width=True)
    with c2:
        st.plotly_chart(px.bar(x=["<40", "40-59", "60-69", ">70"], y=[10, 35, 30, 25], title="อายุ ช.พ.ค.").update_layout(height=250), use_container_width=True)
    with c3:
        st.plotly_chart(px.pie(values=[42, 58], names=["ชาย", "หญิง"], hole=0.7, title="เพศ ช.พ.ส.").update_layout(height=250, showlegend=False), use_container_width=True)
    with c4:
        st.plotly_chart(px.bar(x=["<40", "40-59", "60-69", ">70"], y=[8, 28, 40, 24], title="อายุ ช.พ.ส.").update_layout(height=250), use_container_width=True)

    # --- PART 2: FINANCE ---
    st.markdown('<div class="sub-section">💰 การนำส่งเงิน & งบการเงิน</div>', unsafe_allow_html=True)
    
    fin_col1, fin_col2 = st.columns(2)
    with fin_col1:
        st.write("**💰 เงินสงเคราะห์ ช.พ.ค.**")
        fc1, fc2, fc3 = st.columns(3)
        fc1.markdown('<div class="finance-card" style="background-color:#0097a7;">879 ราย<br><small>จำนวนผู้ตาย</small></div>', unsafe_allow_html=True)
        fc2.markdown('<div class="finance-card" style="background-color:#43a047;">879.-<br><small>รายศพ</small></div>', unsafe_allow_html=True)
        fc3.markdown('<div class="finance-card" style="background-color:#fbc02d; color:black;">900,000.-<br><small>ครอบครัว</small></div>', unsafe_allow_html=True)
        st.metric("นำส่งภายในกำหนด", "90.64%", "834,394 ราย")
    
    with fin_col2:
        st.write("**💰 เงินสงเคราะห์ ช.พ.ส.**")
        fc1, fc2, fc3 = st.columns(3)
        fc1.markdown('<div class="finance-card" style="background-color:#0097a7;">383 ราย<br><small>จำนวนผู้ตาย</small></div>', unsafe_allow_html=True)
        fc2.markdown('<div class="finance-card" style="background-color:#43a047;">383.-<br><small>รายศพ</small></div>', unsafe_allow_html=True)
        fc3.markdown('<div class="finance-card" style="background-color:#fbc02d; color:black;">368,311.-<br><small>ครอบครัว</small></div>', unsafe_allow_html=True)
        st.metric("นำส่งภายในกำหนด", "91.25%", "357,178 ราย")

    # Payment Trend Charts
    st.write("<br>", unsafe_allow_html=True)
    g1, g2 = st.columns(2)
    months = [f"งวด {i}" for i in range(1, 11)]
    with g1:
        fig1 = px.line(x=months, y=[87, 88, 89, 89, 90, 91, 91, 92, 91, 92], title="แนวโน้มการชำระ ช.พ.ค.").update_layout(height=280)
        st.plotly_chart(fig1, use_container_width=True)
    with g2:
        fig2 = px.line(x=months, y=[88, 89, 93, 94, 94, 91, 90, 93, 92, 93], title="แนวโน้มการชำระ ช.พ.ส.").update_layout(height=280)
        st.plotly_chart(fig2, use_container_width=True)

# --- 5. PAGE: LEGAL DASHBOARD ---
def show_legal_dashboard():
    st.title("⚖️ Dashboard นิติการ")
    
    # KPI
    k1, k2, k3, k4 = st.columns(4)
    k1.metric("ทั้งหมด", "45 เรื่อง")
    k2.metric("อยู่ระหว่างดำเนินการ", "28 เรื่อง")
    k3.metric("เสร็จสิ้น", "17 เรื่อง")
    k4.metric("มูลค่าความเสียหาย", "1.25 ล้านบาท")

    # Charts
    st.write("<br>", unsafe_allow_html=True)
    c_l, c_r = st.columns([2, 1])
    with c_l:
        st.write("**ภาระงานตามกลุ่ม**")
        fig = px.bar(x=[9, 5, 6, 2, 6], y=["สืบสวน", "อุทธรณ์", "ร้องเรียน", "ละเมิด", "คดี"], orientation='h', barmode='stack')
        st.plotly_chart(fig, use_container_width=True)
    with c_r:
        st.write("**อัตราเสร็จสิ้น**")
        fig_pie = px.pie(values=[37.8, 62.2], names=["เสร็จสิ้น", "ค้าง"], hole=0.6)
        st.plotly_chart(fig_pie, use_container_width=True)

# --- 6. MAIN LOGIC & NAVIGATION ---
if not st.session_state.logged_in:
    login_page()
else:
    # Sidebar Profile
    st.sidebar.markdown(f"### 👤 {st.session_state.name}")
    st.sidebar.caption(f"สิทธิ์การใช้งาน: {st.session_state.role}")
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()
    
    st.sidebar.divider()
    
    # NAVIGATION BASED ON PRIVILEGE
    menu = ["EIS Dashboard", "Legal Dashboard"]
    if st.session_state.role == "Admin":
        menu.append("Admin Control Panel")
    
    choice = st.sidebar.radio("เลือกแดชบอร์ด:", menu)

    if choice == "EIS Dashboard":
        show_eis_dashboard()
    elif choice == "Legal Dashboard":
        show_legal_dashboard()
    else:
        st.title("⚙️ Admin Control Panel")
        st.write("เฉพาะผู้ดูแลระบบเท่านั้นที่เข้าถึงหน้านี้ได้")
