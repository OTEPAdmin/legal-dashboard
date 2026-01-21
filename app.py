import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# --- 1. CONFIG & SETTINGS ---
st.set_page_config(page_title="Legal & EIS Platform", layout="wide")

# --- 2. THEME & FONTS (Sarabun) ---
st.markdown("""
    <link href="https://fonts.googleapis.com/css2?family=Sarabun:wght@300;400;700&display=swap" rel="stylesheet">
    <style>
        html, body, [class*="css"] { font-family: 'Sarabun', sans-serif !important; }
        .stMetric { background-color: #ffffff; padding: 15px; border-radius: 10px; border-left: 5px solid #45B1CD; box-shadow: 2px 2px 5px rgba(0,0,0,0.05); }
        .login-box { max-width: 400px; margin: auto; padding: 2rem; background: #f8f9fa; border-radius: 15px; border: 1px solid #dee2e6; }
        .eis-card { background-color:#f8f9fa; padding:15px; border-radius:10px; border-top:5px solid #00acc1; margin-bottom:10px; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. SESSION STATE FOR LOGIN ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.role = None
    st.session_state.name = ""

# --- 4. LOGIN PAGE ---
def login_page():
    st.write("<br><br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 1.5, 1])
    with col2:
        st.markdown('<div class="login-box">', unsafe_allow_html=True)
        st.markdown("<h2 style='text-align: center;'>🏛️ Platform Login</h2>", unsafe_allow_html=True)
        user = st.text_input("Username")
        pw = st.text_input("Password", type="password")
        if st.button("เข้าสู่ระบบ", use_container_width=True):
            if user == "admin" and pw == "admin123":
                st.session_state.logged_in, st.session_state.role, st.session_state.name = True, "Admin", "ผู้ดูแลระบบ"
                st.rerun()
            elif user == "user" and pw == "user123":
                st.session_state.logged_in, st.session_state.role, st.session_state.name = True, "User", "เจ้าหน้าที่ทั่วไป"
                st.rerun()
            else:
                st.error("ข้อมูลไม่ถูกต้อง (ลอง: admin / admin123 หรือ user / user123)")
        st.markdown('</div>', unsafe_allow_html=True)

# --- 5. PAGE: EIS DASHBOARD (หน้าใหม่ตามดีไซน์ล่าสุด) ---
def show_eis_dashboard():
    st.title("📊 EIS Dashboard - ข้อมูลสมาชิกเชิงลึก")
    st.write(f"สวัสดีคุณ {st.session_state.name} | ข้อมูลสมาชิก ช.พ.ค. และ ช.พ.ส. ประจำปี 2568")

    # Row 1: KPI Summary
    c1, c2 = st.columns(2)
    with c1:
        st.markdown('<div class="eis-card"><h4>👥 ช.พ.ค.</h4><h2>933,962</h2><p>สมาชิกทั้งหมด</p></div>', unsafe_allow_html=True)
    with c2:
        st.markdown('<div class="eis-card" style="border-top-color:#8e24aa"><h4>👥 ช.พ.ส.</h4><h2>287,654</h2><p>สมาชิกทั้งหมด</p></div>', unsafe_allow_html=True)

    # Row 2: Demographic Analysis
    st.subheader("👥 ข้อมูลประชากร (Demographic)")
    d1, d2, d3, d4 = st.columns(4)
    with d1:
        fig_p1 = px.pie(values=[38, 62], names=["ชาย", "หญิง"], hole=0.7, title="เพศ ช.พ.ค.", color_discrete_sequence=['#03A9F4', '#E91E63'])
        st.plotly_chart(fig_p1, use_container_width=True)
    with d2:
        fig_a1 = px.bar(x=["<40", "40-70", ">70"], y=[15, 60, 25], title="อายุ ช.พ.ค.", color_discrete_sequence=['#FF9800'])
        st.plotly_chart(fig_a1, use_container_width=True)
    with d3:
        fig_p2 = px.pie(values=[42, 58], names=["ชาย", "หญิง"], hole=0.7, title="เพศ ช.พ.ส.", color_discrete_sequence=['#03A9F4', '#E91E63'])
        st.plotly_chart(fig_p2, use_container_width=True)
    with d4:
        fig_a2 = px.bar(x=["<40", "40-70", ">70"], y=[10, 55, 35], title="อายุ ช.พ.ส.", color_discrete_sequence=['#9C27B0'])
        st.plotly_chart(fig_a2, use_container_width=True)

    # Row 3: Death Causes
    st.subheader("⚰️ 5 อันดับสาเหตุการเสียชีวิต")
    death_data = pd.DataFrame({"สาเหตุ": ["มะเร็ง", "ปอด", "หัวใจ", "ชรา", "สมอง"], "จำนวน": [198, 125, 90, 70, 65]})
    fig_death = px.bar(death_data, x="จำนวน", y="สาเหตุ", orientation='h', color="สาเหตุ")
    st.plotly_chart(fig_death, use_container_width=True)

# --- 6. PAGE: LEGAL DASHBOARD (หน้าเดิม) ---
def show_legal_dashboard():
    st.title("⚖️ Legal Dashboard - ภาพรวมคดีความ")
    k1, k2, k3, k4 = st.columns(4)
    k1.metric("คดีทั้งหมด", "45 เรื่อง")
    k2.metric("อยู่ระหว่างดำเนินการ", "28 เรื่อง")
    k3.metric("เสร็จสิ้น", "17 เรื่อง")
    k4.metric("ทุนทรัพย์ (ล้านบาท)", "1.25")
    
    # Mock Bar Chart
    df_work = pd.DataFrame({"กลุ่ม": ["สืบสวน", "อุทธรณ์", "คดี"], "จำนวน": [12, 10, 23]})
    fig = px.bar(df_work, x="กลุ่ม", y="จำนวน", color="กลุ่ม", title="ภาระงานตามกลุ่มงาน")
    st.plotly_chart(fig, use_container_width=True)

# --- 7. PAGE: ADMIN PANEL ---
def show_admin_panel():
    st.title("⚙️ Admin Control Panel")
    st.write("จัดการสิทธิ์และตรวจสอบ Log การใช้งาน")
    st.table(pd.DataFrame({"User": ["admin", "user"], "Status": ["Online", "Offline"]}))

# --- 8. MAIN NAVIGATION ---
if not st.session_state.logged_in:
    login_page()
else:
    # Sidebar
    st.sidebar.markdown(f"### 👤 {st.session_state.name}")
    if st.sidebar.button("Log out"):
        st.session_state.logged_in = False
        st.rerun()
    
    st.sidebar.divider()
    
    # เมนูที่ทั้ง User และ Admin เห็นได้
    menu = ["EIS Dashboard", "Legal Dashboard"]
    
    # เมนูเฉพาะ Admin
    if st.session_state.role == "Admin":
        menu.append("ระบบจัดการ Admin")
    
    choice = st.sidebar.radio("เลือกหน้าแดชบอร์ด:", menu)

    if choice == "EIS Dashboard":
        show_eis_dashboard()
    elif choice == "Legal Dashboard":
        show_legal_dashboard()
    elif choice == "ระบบจัดการ Admin":
        show_admin_panel()
