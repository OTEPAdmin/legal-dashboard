import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# --- 1. CONFIG & SETTINGS ---
st.set_page_config(page_title="Legal EIS Platform (Mockup)", layout="wide")

# --- 2. THEME & FONTS (Sarabun) ---
st.markdown("""
    <link href="https://fonts.googleapis.com/css2?family=Sarabun:wght@300;400;700&display=swap" rel="stylesheet">
    <style>
        html, body, [class*="css"] { font-family: 'Sarabun', sans-serif !important; }
        .stMetric { background-color: #ffffff; padding: 15px; border-radius: 10px; border-left: 5px solid #45B1CD; box-shadow: 2px 2px 5px rgba(0,0,0,0.05); }
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
                st.error("ข้อมูลไม่ถูกต้อง (ลอง: user / user123)")
        st.markdown('</div>', unsafe_allow_html=True)

# --- 5. PAGE: GENERAL DASHBOARD (Using Mock Data) ---
def show_general_dashboard():
    st.title(f"📊 ภาพรวมนิติการ (Mock Data)")
    st.write(f"ยินดีต้อนรับคุณ **{st.session_state.name}** | สิทธิ์การใช้งาน: **{st.session_state.role}**")
    
    # Mock Data: Summary
    m_total, m_pending, m_done, m_damage = 45, 28, 17, 1250000

    # Row 1: KPI Metrics
    k1, k2, k3, k4 = st.columns(4)
    k1.metric("ทั้งหมด", f"{m_total} เรื่อง")
    k2.metric("กำลังดำเนินการ", f"{m_pending} เรื่อง")
    k3.metric("เสร็จสิ้น", f"{m_done} เรื่อง")
    k4.metric("มูลค่าความเสียหาย", f"{m_damage:,} บาท")

    # Mock Data: Workload Chart
    df_work = pd.DataFrame({
        "กลุ่มงาน": ["สืบสวน-วินัย", "อุทธรณ์-ร้องทุกข์", "ร้องเรียน", "ละเมิด", "คดี"],
        "อยู่ระหว่างดำเนินการ": [9, 5, 6, 2, 6],
        "ดำเนินการเสร็จสิ้น": [3, 5, 4, 2, 4]
    })

    # Row 2: Charts
    st.write("<br>", unsafe_allow_html=True)
    c1, c2 = st.columns([2, 1])
    with c1:
        st.subheader("ภาระงานแยกตามกลุ่มงาน")
        fig = px.bar(df_work, y="กลุ่มงาน", x=["อยู่ระหว่างดำเนินการ", "ดำเนินการเสร็จสิ้น"], 
                     orientation='h', barmode='stack', 
                     color_discrete_map={"อยู่ระหว่างดำเนินการ": "#45B1CD", "ดำเนินการเสร็จสิ้น": "#6ECB93"})
        fig.update_layout(font_family="Sarabun", height=350, margin=dict(l=0, r=0, t=30, b=0))
        st.plotly_chart(fig, use_container_width=True)
    with c2:
        st.subheader("สัดส่วนงานสะสม")
        fig_pie = px.pie(values=[24, 22, 22, 9, 22], names=["สืบสวน", "อุทธรณ์", "ร้องเรียน", "ละเมิด", "คดี"], hole=0.5,
                         color_discrete_sequence=px.colors.qualitative.Pastel)
        fig_pie.update_layout(font_family="Sarabun", showlegend=False, height=350)
        st.plotly_chart(fig_pie, use_container_width=True)

    # Mock Data: Main Table
    st.subheader("📋 รายการคดีล่าสุด")
    df_main = pd.DataFrame({
        "ลำดับ": [1, 2, 3, 4],
        "เรื่อง": ["คดีบรรจุแต่งตั้งตำแหน่ง", "คดีเลิกจ้างไม่เป็นธรรม", "คดียักยอกทรัพย์", "คดีฟ้องเพิกถอนคำสั่ง"],
        "ประเภทคดี": ["ปกครอง", "แพ่ง", "อาญา", "ปกครอง"],
        "สถานะคดี": ["ศาลชั้นต้น", "ศาลอุทธรณ์", "เสร็จสิ้น", "ศาลฎีกา"]
    })
    st.dataframe(df_main, use_container_width=True, hide_index=True)

# --- 6. PAGE: ANALYTICS (Super User & Admin) ---
def show_analytics():
    st.title("🧪 Advanced Analytics (Mock Data)")
    st.info("หน้านี้จำลองการแสดงกราฟแนวโน้มคดีรายเดือน")
    
    # Mock Time Series Data
    df_time = pd.DataFrame({
        "เดือน": ["ม.ค.", "ก.พ.", "มี.ค.", "เม.ย.", "พ.ค."],
        "คดีรับใหม่": [5, 8, 12, 7, 10],
        "คดีที่ปิดได้": [3, 4, 8, 9, 6]
    })
    fig_line = px.line(df_time, x="เดือน", y=["คดีรับใหม่", "คดีที่ปิดได้"], markers=True)
    fig_line.update_layout(font_family="Sarabun")
    st.plotly_chart(fig_line, use_container_width=True)

# --- 7. PAGE: ADMIN PANEL (Admin Only) ---
def show_admin():
    st.title("⚙️ ระบบจัดการ Admin")
    st.success("Admin เข้าถึงหน้านี้ได้เพื่อจัดการ Log และระบบหลังบ้าน")
    st.write("ตารางจำลองรายชื่อผู้ใช้:")
    st.table(pd.DataFrame({
        "Username": ["admin", "super", "user"],
        "Role": ["Admin", "Super User", "User"],
        "Last Login": ["2026-01-20", "2026-01-19", "2026-01-21"]
    }))

# --- 8. MAIN NAVIGATION LOGIC ---
if not st.session_state.logged_in:
    login_page()
else:
    # Sidebar Navigation
    st.sidebar.markdown(f"### 👤 {st.session_state.name}")
    st.sidebar.write(f"ระดับสิทธิ์: **{st.session_state.role}**")
    if st.sidebar.button("ออกจากระบบ"):
        st.session_state.logged_in = False
        st.rerun()
    
    st.sidebar.divider()
    
    # จัดการเมนูตามสิทธิ์
    menu = ["ภาพรวมระบบ (General)"]
    if st.session_state.role in ["Super User", "Admin"]:
        menu.append("วิเคราะห์เชิงลึก (Analytics)")
    if st.session_state.role == "Admin":
        menu.append("จัดการระบบ (Admin)")
    
    choice = st.sidebar.radio("เลือกหน้า Dashboard:", menu)

    # แสดงผลตามหน้า
    if choice == "ภาพรวมระบบ (General)":
        show_general_dashboard()
    elif choice == "วิเคราะห์เชิงลึก (Analytics)":
        show_analytics()
    elif choice == "จัดการระบบ (Admin)":
        show_admin()
