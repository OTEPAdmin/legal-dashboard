import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os

# --- 1. CONFIGURATION & STYLE ---
st.set_page_config(page_title="EIS Platform", layout="wide", page_icon="🏛️")

# Injecting Sarabun Font globally and specific Card Styles
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Sarabun:wght@300;400;500;700&display=swap');

        /* Force Sarabun font on EVERYTHING including Streamlit widgets */
        html, body, [class*="css"], .stMarkdown, .stButton, .stTextField, .stNumberInput, .stSelectbox, .stMetric {
            font-family: 'Sarabun', sans-serif !important;
        }
        
        /* Login Container */
        .login-box {
            background-color: white;
            padding: 40px;
            border-radius: 10px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
            max-width: 400px;
            margin: 0 auto;
            border-top: 5px solid #E91E63;
        }

        /* Dashboard Card Styles */
        .card-cpk {
            background-color: white;
            border-radius: 10px;
            border-top: 6px solid #00ACC1; /* Cyan */
            padding: 15px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.05);
            text-align: center;
        }
        .card-cps {
            background-color: white;
            border-radius: 10px;
            border-top: 6px solid #8E24AA; /* Purple */
            padding: 15px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.05);
            text-align: center;
        }
        
        /* Metric Styling */
        .stat-value { font-size: 28px; font-weight: bold; margin: 0; color: #333; }
        .stat-label { color: grey; font-size: 14px; }
        .stat-up { color: #4CAF50; font-weight: bold; font-size: 14px; }
        .stat-down { color: #E91E63; font-weight: bold; font-size: 14px; }
        
        /* Finance Cards */
        .fin-card-blue { background-color: #00BCD4; color: white; padding: 15px; border-radius: 8px; text-align: center; }
        .fin-card-green { background-color: #66BB6A; color: white; padding: 15px; border-radius: 8px; text-align: center; }
        .fin-card-gold { background-color: #FBC02D; color: white; padding: 15px; border-radius: 8px; text-align: center; }
        
        /* Revenue Dashboard Cards */
        .rev-card-bg { background-color: #f8f9fa; border-radius: 10px; padding: 15px; border: 1px solid #ddd; text-align: center; }
        .rev-title { font-size: 16px; color: #555; margin-bottom: 5px; }
        .rev-value { font-size: 32px; font-weight: bold; color: #E91E63; }
        .rev-unit { font-size: 14px; color: #888; }
        
    </style>
""", unsafe_allow_html=True)

# FILENAME OF THE LOGO
LOGO_FILENAME = "image_11b1c9.jpg"

# --- HELPER: RENDER HEADER WITH LOGO ---
def render_header(title, border_color="#607D8B"):
    col1, col2 = st.columns([9, 1])
    with col1:
        st.markdown(f"""
            <div style="background-color: #F5F5F5; padding: 15px; border-radius: 5px; margin-bottom: 20px; border-left: 5px solid {border_color};">
                <h2 style="margin:0; color:#333;">{title}</h2>
            </div>
        """, unsafe_allow_html=True)
    with col2:
        # Place logo at top right
        if os.path.exists(LOGO_FILENAME):
            st.image(LOGO_FILENAME, width=100)
        else:
            st.write("Logo not found")

# --- 2. SESSION STATE (Authentication) ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.role = None
    st.session_state.username = ""

# --- 3. LOGIN PAGE ---
def login_page():
    st.markdown("<br>", unsafe_allow_html=True)
    
    # --- LOGO CENTERED ON TOP ---
    c1, c2, c3 = st.columns([1, 1, 1])
    with c2:
        if os.path.exists(LOGO_FILENAME):
            st.image(LOGO_FILENAME, width=150, use_container_width=False) 
        else:
            st.warning(f"Please upload '{LOGO_FILENAME}' to the folder.")
            
    st.markdown("<br>", unsafe_allow_html=True)

    # --- LOGIN BOX ---
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        st.markdown('<div class="login-box">', unsafe_allow_html=True)
        st.markdown("<h2 style='text-align: center; margin-top:0;'>🔐 เข้าสู่ระบบ (Login)</h2>", unsafe_allow_html=True)
        
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        
        if st.button("Sign In", use_container_width=True):
            if username == "admin" and password == "admin123":
                st.session_state.logged_in = True
                st.session_state.role = "Admin"
                st.session_state.username = "Administrator"
                st.rerun()
            elif username == "superuser" and password == "superuser1234":
                st.session_state.logged_in = True
                st.session_state.role = "Superuser"
                st.session_state.username = "Super User"
                st.rerun()
            elif username == "user" and password == "user123":
                st.session_state.logged_in = True
                st.session_state.role = "User"
                st.session_state.username = "General User"
                st.rerun()
            else:
                st.error("ชื่อผู้ใช้หรือรหัสผ่านไม่ถูกต้อง")
        st.markdown('</div>', unsafe_allow_html=True)

# --- 4. PAGE: EIS DASHBOARD (Member & Finance) ---
def show_eis_dashboard():
    # Header with Logo
    render_header("📊 บทสรุปผู้บริหาร (Executive Summary)", border_color="#607D8B")
    
    # Filters
    c1, c2, c3, c4 = st.columns(4)
    with c1: st.selectbox("ช่วงเวลา", ["พฤศจิกายน", "ธันวาคม"], index=0)
    with c2: st.selectbox("ปี", ["2568", "2567"], index=0)
    
    st.write("---")

    # --- ROW 1: MEMBER OVERVIEW ---
    col_kpi1, col_kpi2 = st.columns(2)
    
    # Card 1: Ch.P.K.
    with col_kpi1:
        st.markdown("""
            <div class="card-cpk">
                <h3 style="margin:0; color:#00ACC1;">ภาพรวมสมาชิก ช.พ.ค.</h3>
                <div style="display:flex; justify-content:space-around; margin-top:15px;">
                    <div><p class="stat-value" style="color:#00ACC1;">933,962</p><p class="stat-label">จำนวนสมาชิก</p></div>
                    <div><p class="stat-value" style="color:#4CAF50;">12,456</p><p class="stat-up">สมาชิกเพิ่ม</p></div>
                    <div><p class="stat-value" style="color:#E91E63;">8,967</p><p class="stat-down">จำหน่าย</p></div>
                </div>
            </div>
        """, unsafe_allow_html=True)
        # Charts for Ch.P.K.
        c_sub1, c_sub2 = st.columns(2)
        with c_sub1:
            st.caption("📈 สมาชิกเพิ่ม ช.พ.ค.")
            fig = px.bar(x=[10587, 1869], y=["สมัคร", "ขอกลับ"], orientation='h', color_discrete_sequence=['#4CAF50'])
            fig.update_layout(height=180, margin=dict(l=0,r=0,t=0,b=0), xaxis_visible=False, font_family="Sarabun")
            st.plotly_chart(fig, use_container_width=True)
        with c_sub2:
            st.caption("📉 จำหน่าย ช.พ.ค.")
            fig = px.bar(x=[2242, 1345, 4500, 448], y=["ถอนชื่อ", "ลาออก", "ตาย", "อื่นๆ"], orientation='h', 
                         color_discrete_sequence=['#FBC02D', '#AB47BC', '#E91E63', '#BDBDBD'])
            fig.update_traces(marker_color=['#FBC02D', '#AB47BC', '#E91E63', '#BDBDBD'])
            fig.update_layout(height=180, margin=dict(l=0,r=0,t=0,b=0), xaxis_visible=False, font_family="Sarabun")
            st.plotly_chart(fig, use_container_width=True)

    # Card 2: Ch.P.S.
    with col_kpi2:
        st.markdown("""
            <div class="card-cps">
                <h3 style="margin:0; color:#8E24AA;">ภาพรวมสมาชิก ช.พ.ส.</h3>
                <div style="display:flex; justify-content:space-around; margin-top:15px;">
                    <div><p class="stat-value" style="color:#8E24AA;">287,654</p><p class="stat-label">จำนวนสมาชิก</p></div>
                    <div><p class="stat-value" style="color:#4CAF50;">4,532</p><p class="stat-up">สมาชิกเพิ่ม</p></div>
                    <div><p class="stat-value" style="color:#E91E63;">5,234</p><p class="stat-down">จำหน่าย</p></div>
                </div>
            </div>
        """, unsafe_allow_html=True)
        # Charts for Ch.P.S.
        c_sub3, c_sub4 = st.columns(2)
        with c_sub3:
            st.caption("📈 สมาชิกเพิ่ม ช.พ.ส.")
            fig = px.bar(x=[3626, 906], y=["สมัคร", "ขอกลับ"], orientation='h', color_discrete_sequence=['#4CAF50'])
            fig.update_layout(height=180, margin=dict(l=0,r=0,t=0,b=0), xaxis_visible=False, font_family="Sarabun")
            st.plotly_chart(fig, use_container_width=True)
        with c_sub4:
            st.caption("📉 จำหน่าย ช.พ.ส.")
            fig = px.bar(x=[1047, 628, 3245, 314], y=["ถอนชื่อ
