import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# --- 1. CONFIG & SETTINGS ---
st.set_page_config(page_title="EIS & Legal Platform", layout="wide")

# --- 2. THEME & FONTS (Sarabun) ---
st.markdown("""
    <link href="https://fonts.googleapis.com/css2?family=Sarabun:wght@300;400;700&display=swap" rel="stylesheet">
    <style>
        html, body, [class*="css"] { font-family: 'Sarabun', sans-serif !important; }
        .stMetric { background-color: #ffffff; padding: 15px; border-radius: 10px; border-left: 5px solid #45B1CD; box-shadow: 2px 2px 5px rgba(0,0,0,0.05); }
        .login-box { max-width: 400px; margin: auto; padding: 2rem; background: #f8f9fa; border-radius: 15px; border: 1px solid #dee2e6; }
        .executive-header { background-color: #f1f3f4; padding: 10px 20px; border-radius: 5px; margin-bottom: 20px; border-left: 8px solid #5f6368; }
        .kpi-card { background-color: white; padding: 20px; border-radius: 10px; border: 1px solid #e0e0e0; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. SESSION STATE ---
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
        st.markdown("<h2 style='text-align: center;'>🏛️ EIS Platform Login</h2>", unsafe_allow_html=True)
        user = st.text_input("Username")
        pw = st.text_input("Password", type="password")
        if st.button("เข้าสู่ระบบ", use_container_width=True):
            if user == "admin" and pw == "admin123":
                st.session_state.logged_in, st.session_state.role, st.session_state.name = True, "Admin", "ผู้ดูแลระบบ"
                st.rerun()
            elif user == "user" and pw == "user123":
                st.session_state.logged_in, st.session_state.role, st.session_state.name = True, "User", "เจ้าหน้าที่นิติการ"
                st.rerun()
            else:
                st.error("Username หรือ Password ไม่ถูกต้อง")
        st.markdown('</div>', unsafe_allow_html=True)

# --- 5. PAGE: EIS DASHBOARD (บทสรุปผู้บริหาร) ---
def show_eis_dashboard():
    st.markdown('<div class="executive-header"><h2>📊 บทสรุปผู้บริหาร (Executive Summary)</h2></div>', unsafe_allow_html=True)
    
    # ส่วนตัวเลือกช่วงเวลา (Filters)
    with st.expander("🔍 กรองข้อมูลตามช่วงเวลา", expanded=False):
        c_f1, c_f2, c_f3, c_f4 = st.columns(4)
        c_f1.selectbox("ช่วงเวลาเริ่มต้น", ["กุมภาพันธ์", "มกราคม"], index=0)
        c_f2.selectbox("ปีเริ่มต้น", ["2568", "2567"], index=0)
        c_f3.selectbox("สิ้นสุด", ["กุมภาพันธ์", "มีนาคม"], index=0)
        c_f4.selectbox("ปีสิ้นสุด", ["2568", "2567"], index=0)

    # --- KPI Section ---
    st.markdown("### 👥 ภาพรวมสมาชิก")
    col_k1, col_k2 = st.columns(2)
    with col_k1:
        st.markdown("""
        <div class="kpi-card" style="border-top: 5px solid #0097a7;">
            <h4 style="color:#0097a7;">ช.พ.ค.</h4>
            <h2 style="margin:0;">933,962</h2>
            <p style="color:grey; font-size:14px;">สมาชิกทั้งหมด</p>
            <div style="display:flex; justify-content:space-around; margin-top:10px;">
                <span style="color:green;">+12,456 เพิ่ม</span>
                <span style="color:red;">-8,967 จำหน่าย</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
    with col_k2:
        st.markdown("""
        <div class="kpi-card" style="border-top: 5px solid #d81b60;">
            <h4 style="color:#d81b60;">ช.พ.ส.</h4>
            <h2 style="margin:0;">287,654</h2>
            <p style="color:grey; font-size:14px;">สมาชิกทั้งหมด</p>
            <div style="display:flex; justify-content:space-around; margin-top:10px;">
                <span style="color:green;">+4,532 เพิ่ม</span>
                <span style="color:red;">-5,234 จำหน่าย</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # --- Charts Section ---
    st.write("<br>", unsafe_allow_html=True)
    st.markdown("### 🧬 ข้อมูลประชากรและสถิติการเสียชีวิต")
    
    row2_1, row2_2, row2_3, row2_4 = st.columns(4)
    with row2_1:
        fig_p1 = px.pie(values=[38, 62], names=["ชาย", "หญิง"], hole=0.7, title="เพศ ช.พ.ค.", color_discrete_sequence=['#03A9F4', '#E91E63'])
        fig_p1.update_layout(margin=dict(t=30, b=0, l=0, r=0), height=250)
        st.plotly_chart(fig_p1, use_container_width=True)
    with row2_2:
        fig_a1 = px.bar(x=["<40", "40-59", "60-69", ">70"], y=[10, 35, 30, 25], title="ช่วงอายุ ช.พ.ค.", color_discrete_sequence=['#FFC107'])
        fig_a1.update_layout(margin=dict(t=30, b=0, l=0, r=0), height=250, xaxis_title=None, yaxis_title=None)
        st.plotly_chart(fig_a1, use_container_width=True)
    with row2_3:
        fig_p2 = px.pie(values=[42, 58], names=["ชาย", "หญิง"], hole=0.7, title="เพศ ช.พ.ส.", color_discrete_sequence=['#03A9F4', '#E91E63'])
        fig_p2.update_layout(margin=dict(t=30, b=0, l=0, r=0), height=250)
        st.plotly_chart(fig_p2, use_container_width=True)
    with row2_4:
        fig_a2 = px.bar(x=["<40", "40-59", "60-69", ">70"], y=[8, 28, 40, 24], title="ช่วงอายุ ช.พ.ส.", color_discrete_sequence=['#9C27B0'])
        fig_a2.update_layout(margin=dict(t=30, b=0, l=0, r=0), height=250, xaxis_title=None, yaxis_title=None)
        st.plotly_chart(fig_a2, use_container_width=True)

    # --- Death Causes ---
    st.divider()
    col_d1, col_d2 = st.columns(2)
    death_labels = ["โรคมะเร็ง", "โรคหัวใจ", "โรคปอด", "โรคชรา", "อื่นๆ"]
    with col_d1:
        st.caption("5 อันดับสาเหตุการเสียชีวิต ช.พ.ค.")
        fig_d1 = px.bar(x=[198, 90, 125, 70, 50], y=death_labels, orientation='h', color=death_labels, color_discrete_sequence=px.colors.qualitative.Vivid)
        fig_d1.update_layout(height=300, showlegend=False, margin=dict(t=0, b=0, l=0, r=0), yaxis={'categoryorder':'total ascending'})
        st.plotly_chart(fig_d1, use_container_width=True)
    with col_d2:
        st.caption("5 อันดับสาเหตุการเสียชีวิต ช.พ.ส.")
        fig_d2 = px.bar(x=[45, 38, 32, 28, 15], y=death_labels, orientation='h', color=death_labels, color_discrete_sequence=px.colors.qualitative.Vivid)
        fig_d2.update_layout(height=300, showlegend=False, margin=dict(t=0, b=0, l=0, r=0), yaxis={'categoryorder':'total ascending'})
        st.plotly_chart(fig_d2, use_container_width=True)

# --- 6. PAGE: LEGAL DASHBOARD (หน้าเดิม) ---
def show_legal_dashboard():
    st.title("⚖️ Legal Dashboard - ข้อมูลคดีความ")
    st.info("ส่วนแสดงผลข้อมูลคดีความแยกตามประเภทและสถานะ")
    # ใส่โค้ดกราฟคดีความเดิมที่นี่...
    st.metric("จำนวนคดีทั้งหมด", "45 เรื่อง", delta="5 เรื่องจากเดือนก่อน")

# --- 7. MAIN NAVIGATION ---
if not st.session_state.logged_in:
    login_page()
else:
    # Sidebar
    st.sidebar.markdown(f"### 👤 {st.session_state.name}")
    st.sidebar.write(f"สิทธิ์: **{st.session_state.role}**")
    if st.sidebar.button("Log out"):
        st.session_state.logged_in = False
        st.rerun()
    
    st.sidebar.divider()
    
    # เมนูที่ทั้ง User และ Admin เข้าถึงได้
    menu_options = ["บทสรุปผู้บริหาร (EIS Dashboard)", "ข้อมูลคดีความ (Legal Dashboard)"]
    
    # เมนูสำหรับ Admin เท่านั้น
    if st.session_state.role == "Admin":
        menu_options.append("ระบบจัดการ Admin")
        
    choice = st.sidebar.radio("เลือกหน้าแดชบอร์ด:", menu_options)

    if "บทสรุปผู้บริหาร" in choice:
        show_eis_dashboard()
    elif "ข้อมูลคดีความ" in choice:
        show_legal_dashboard()
    elif "ระบบจัดการ Admin" in choice:
        st.title("⚙️ ระบบจัดการ Admin")
        st.write("จัดการสิทธิ์ผู้ใช้งานและ Log ระบบ")
