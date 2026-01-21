import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# --- 1. CONFIG & SETTINGS ---
st.set_page_config(page_title="Legal EIS Platform", layout="wide")

# ลิงก์ Google Sheets (ต้องแชร์เป็น Anyone with the link)
SHEET_URL = "https://docs.google.com/spreadsheets/d/ใส่_ID_ไฟล์ของคุณที่นี่/edit?usp=sharing"

# ฟังก์ชันดึงข้อมูลภาษาไทยจาก Google Sheets
def load_sheet(url, sheet_name):
    try:
        csv_url = url.split('/edit')[0] + f'/gviz/tq?tqx=out:csv&sheet={sheet_name}'
        return pd.read_csv(csv_url)
    except:
        return None

# --- 2. THEME & FONTS (Sarabun) ---
st.markdown("""
    <link href="https://fonts.googleapis.com/css2?family=Sarabun:wght@300;400;700&display=swap" rel="stylesheet">
    <style>
        html, body, [class*="css"] { font-family: 'Sarabun', sans-serif !important; }
        .stMetric { background-color: #ffffff; padding: 15px; border-radius: 10px; border-left: 5px solid #45B1CD; }
        .login-box { max-width: 400px; margin: auto; padding: 2rem; background: #f8f9fa; border-radius: 15px; border: 1px solid #dee2e6; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. SESSION STATE FOR LOGIN ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.role = None
    st.session_state.name = ""

# --- 4. LOGIN PAGE DESIGN ---
def login_page():
    st.write("<br><br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 1.5, 1])
    with col2:
        st.markdown('<div class="login-box">', unsafe_allow_html=True)
        st.markdown("<h2 style='text-align: center;'>🏛️ Legal EIS Login</h2>", unsafe_allow_html=True)
        user = st.text_input("Username")
        pw = st.text_input("Password", type="password")
        if st.button("เข้าสู่ระบบ", use_container_width=True):
            if user == "admin" and pw == "admin123":
                st.session_state.logged_in, st.session_state.role, st.session_state.name = True, "Admin", "ผู้ดูแลระบบ"
                st.rerun()
            elif user == "super" and pw == "super123":
                st.session_state.logged_in, st.session_state.role, st.session_state.name = True, "Super User", "ฝ่ายยุทธศาสตร์"
                st.rerun()
            elif user == "user" and pw == "user123":
                st.session_state.logged_in, st.session_state.role, st.session_state.name = True, "User", "เจ้าหน้าที่นิติการ"
                st.rerun()
            else:
                st.error("ข้อมูลไม่ถูกต้อง")
        st.markdown('</div>', unsafe_allow_html=True)

# --- 5. PAGE: GENERAL DASHBOARD ---
def show_general_dashboard():
    st.title(f"📊 ภาพรวมนิติการ (สิทธิ์: {st.session_state.role})")
    
    # ดึงข้อมูล
    df_sum = load_sheet(SHEET_URL, "Summary")
    df_work = load_sheet(SHEET_URL, "Workload")
    df_main = load_sheet(SHEET_URL, "MainData")

    if df_sum is not None:
        # Row 1: KPI Metrics
        k1, k2, k3, k4 = st.columns(4)
        k1.metric("ทั้งหมด", f"{df_sum['ทั้งหมด'][0]} เรื่อง")
        k2.metric("กำลังดำเนินการ", f"{df_sum['อยู่ระหว่างดำเนินการ'][0]} เรื่อง")
        k3.metric("เสร็จสิ้น", f"{df_sum['ดำเนินการเสร็จสิ้น'][0]} เรื่อง")
        k4.metric("มูลค่าความเสียหาย", f"{df_sum['มูลค่าความเสียหาย'][0]:,} บาท")

        # Row 2: Charts
        st.write("<br>", unsafe_allow_html=True)
        c1, c2 = st.columns([2, 1])
        with c1:
            st.subheader("ภาระงานแยกตามกลุ่มงาน")
            fig = px.bar(df_work, y="กลุ่มงาน", x=["อยู่ระหว่างดำเนินการ", "ดำเนินการเสร็จสิ้น"], 
                         orientation='h', barmode='stack', color_discrete_map={"อยู่ระหว่างดำเนินการ": "#45B1CD", "ดำเนินการเสร็จสิ้น": "#6ECB93"})
            fig.update_layout(font_family="Sarabun", height=300)
            st.plotly_chart(fig, use_container_width=True)
        with c2:
            st.subheader("สัดส่วนงาน")
            fig_pie = px.pie(values=[24, 22, 22, 9, 22], names=["สืบสวน", "อุทธรณ์", "ร้องเรียน", "ละเมิด", "คดี"], hole=0.5)
            fig_pie.update_layout(font_family="Sarabun", showlegend=False, height=300)
            st.plotly_chart(fig_pie, use_container_width=True)

        # Row 3: Table
        st.subheader("📋 รายการคดีล่าสุด")
        st.dataframe(df_main, use_container_width=True, hide_index=True)

# --- 6. PAGE: ANALYTICS (Super User & Admin) ---
def show_analytics():
    st.title("🧪 Advanced Analytics")
    st.write("การวิเคราะห์เปรียบเทียบเชิงลึกรายเดือนและสถิติสะสม")
    st.image("https://via.placeholder.com/800x400.png?text=Advanced+Analytics+Chart+Placeholder")

# --- 7. PAGE: ADMIN PANEL (Admin Only) ---
def show_admin():
    st.title("⚙️ ระบบจัดการ Admin")
    st.info("คุณสามารถแก้ไขรายชื่อผู้ใช้และสิทธิ์การเข้าถึงได้ที่นี่")

# --- 8. MAIN NAVIGATION LOGIC ---
if not st.session_state.logged_in:
    login_page()
else:
    # Sidebar
    st.sidebar.markdown(f"### 👤 {st.session_state.name}")
    st.sidebar.write(f"ระดับ: {st.session_state.role}")
    if st.sidebar.button("ออกจากระบบ"):
        st.session_state.logged_in = False
        st.rerun()
    
    st.sidebar.divider()
    
    # กำหนดเมนูตามสิทธิ์
    menu = ["ภาพรวมระบบ (General)"]
    if st.session_state.role in ["Super User", "Admin"]:
        menu.append("วิเคราะห์เชิงลึก (Analytics)")
    if st.session_state.role == "Admin":
        menu.append("จัดการระบบ (Admin)")
    
    choice = st.sidebar.radio("เมนูหลัก", menu)

    # แสดงผลตามหน้า
    if choice == "ภาพรวมระบบ (General)":
        show_general_dashboard()
    elif choice == "วิเคราะห์เชิงลึก (Analytics)":
        show_analytics()
    elif choice == "จัดการระบบ (Admin)":
        show_admin()
