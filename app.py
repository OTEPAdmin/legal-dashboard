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

# --- 6. PAGE: ANALYTICS (ดีไซน์ใหม่ตามภาพที่ส่งมา) ---
def show_analytics():
    st.title("📊 บทสรุปผู้บริหาร & ข้อมูลสมาชิกเชิงลึก")
    st.write("ข้อมูลภาพรวมสมาชิก ช.พ.ค. และ ช.พ.ส. ประจำปี 2568")

    # --- ROW 1: ภาพรวมสมาชิก (KPI Cards) ---
    col_a, col_b = st.columns(2)
    
    with col_a:
        st.markdown("""
            <div style="background-color:#f0f7f9; padding:15px; border-radius:10px; border-top:5px solid #00acc1">
                <h4 style="color:#00acc1; margin:0">👥 ภาพรวมสมาชิก ช.พ.ค.</h4>
                <div style="display:flex; justify-content:space-between; align-items:center; margin-top:10px">
                    <div><h2 style="margin:0">933,962</h2><p style="font-size:12px; color:grey">จำนวนสมาชิก</p></div>
                    <div style="color:#4caf50; text-align:right"><h3 style="margin:0">12,456</h3><p style="font-size:12px">สมาชิกเพิ่ม</p></div>
                    <div style="color:#e91e63; text-align:right"><h3 style="margin:0">8,967</h3><p style="font-size:12px">จำหน่าย</p></div>
                </div>
            </div>
        """, unsafe_allow_html=True)

    with col_b:
        st.markdown("""
            <div style="background-color:#f9f0f5; padding:15px; border-radius:10px; border-top:5px solid #8e24aa">
                <h4 style="color:#8e24aa; margin:0">👥 ภาพรวมสมาชิก ช.พ.ส.</h4>
                <div style="display:flex; justify-content:space-between; align-items:center; margin-top:10px">
                    <div><h2 style="margin:0">287,654</h2><p style="font-size:12px; color:grey">จำนวนสมาชิก</p></div>
                    <div style="color:#4caf50; text-align:right"><h3 style="margin:0">4,532</h3><p style="font-size:12px">สมาชิกเพิ่ม</p></div>
                    <div style="color:#e91e63; text-align:right"><h3 style="margin:0">5,234</h3><p style="font-size:12px">จำหน่าย</p></div>
                </div>
            </div>
        """, unsafe_allow_html=True)

    st.write("<br>", unsafe_allow_html=True)

    # --- ROW 2: สมาชิกเพิ่ม/จำหน่าย (Horizontal Bars) ---
    c1, c2, c3, c4 = st.columns(4)
    
    with c1:
        st.caption("📈 สมาชิกเพิ่ม ช.พ.ค.")
        fig1 = px.bar(x=[10587, 1869], y=["สมัคร", "ขอกลับ"], orientation='h', color_discrete_sequence=['#6ECB93'])
        fig1.update_layout(height=200, margin=dict(l=0,r=0,t=0,b=0), xaxis_title=None, yaxis_title=None)
        st.plotly_chart(fig1, use_container_width=True)

    with c2:
        st.caption("📉 จำหน่าย ช.พ.ค.")
        fig2 = px.bar(x=[2242, 1345, 4500, 448], y=["ถอนชื่อ", "ลาออก", "ตาย", "อื่นๆ"], orientation='h', 
                      color=["ถอนชื่อ", "ลาออก", "ตาย", "อื่นๆ"], color_discrete_sequence=['#FBC02D', '#A367DC', '#E91E63', '#90A4AE'])
        fig2.update_layout(height=200, margin=dict(l=0,r=0,t=0,b=0), showlegend=False, xaxis_title=None, yaxis_title=None)
        st.plotly_chart(fig2, use_container_width=True)
    
    # (ทำเช่นเดียวกันกับ c3, c4 สำหรับ ช.พ.ส.)
    with c3:
        st.caption("📈 สมาชิกเพิ่ม ช.พ.ส.")
        fig3 = px.bar(x=[3626, 906], y=["สมัคร", "ขอกลับ"], orientation='h', color_discrete_sequence=['#6ECB93'])
        fig3.update_layout(height=200, margin=dict(l=0,r=0,t=0,b=0), xaxis_title=None, yaxis_title=None)
        st.plotly_chart(fig3, use_container_width=True)

    with c4:
        st.caption("📉 จำหน่าย ช.พ.ส.")
        fig4 = px.bar(x=[1047, 628, 3245, 314], y=["ถอนชื่อ", "ลาออก", "ตาย", "อื่นๆ"], orientation='h', 
                      color_discrete_sequence=['#FBC02D', '#00BCD4', '#E91E63', '#90A4AE'])
        fig4.update_layout(height=200, margin=dict(l=0,r=0,t=0,b=0), xaxis_title=None, yaxis_title=None)
        st.plotly_chart(fig4, use_container_width=True)

    # --- ROW 3: ข้อมูลสมาชิก DEMOGRAPHIC ---
    st.divider()
    st.subheader("👥 ข้อมูลสมาชิก | DEMOGRAPHIC")
    d1, d2, d3, d4 = st.columns(4)

    with d1:
        st.caption("สัดส่วนเพศ ช.พ.ค.")
        fig_p1 = px.pie(values=[38, 62], names=["ชาย", "หญิง"], hole=0.7, color_discrete_sequence=['#03A9F4', '#E91E63'])
        fig_p1.update_layout(height=200, margin=dict(l=10,r=10,t=10,b=10), showlegend=False)
        st.plotly_chart(fig_p1, use_container_width=True)

    with d2:
        st.caption("กลุ่มอายุ ช.พ.ค.")
        fig_a1 = px.bar(x=["<40", "40-49", "50-59", "60-69", ">70"], y=[8, 12, 25, 22, 12], color_discrete_sequence=['#FF9800'])
        fig_a1.update_layout(height=200, margin=dict(l=0,r=0,t=0,b=0), xaxis_title=None, yaxis_title=None)
        st.plotly_chart(fig_a1, use_container_width=True)
        
    # (ทำ d3, d4 ให้เหมือน d1, d2 แต่เปลี่ยนข้อมูลเป็น ช.พ.ส.)
    with d3:
        st.caption("สัดส่วนเพศ ช.พ.ส.")
        fig_p2 = px.pie(values=[42, 58], names=["ชาย", "หญิง"], hole=0.7, color_discrete_sequence=['#03A9F4', '#E91E63'])
        fig_p2.update_layout(height=200, margin=dict(l=10,r=10,t=10,b=10), showlegend=False)
        st.plotly_chart(fig_p2, use_container_width=True)
        
    with d4:
        st.caption("กลุ่มอายุ ช.พ.ส.")
        fig_a2 = px.bar(x=["<40", "40-49", "50-59", "60-69", ">70"], y=[5, 10, 25, 32, 22], color_discrete_sequence=['#9C27B0'])
        fig_a2.update_layout(height=200, margin=dict(l=0,r=0,t=0,b=0), xaxis_title=None, yaxis_title=None)
        st.plotly_chart(fig_a2, use_container_width=True)

    # --- ROW 4: สาเหตุการเสียชีวิต ---
    st.divider()
    st.subheader("⚰️ 5 อันดับสาเหตุการเสียชีวิต")
    col_death1, col_death2 = st.columns(2)

    death_data = pd.DataFrame({
        "สาเหตุ": ["โรคมะเร็ง", "โรคปอด", "โรคหัวใจ", "โรคชรา", "โรคสมอง"],
        "ชพค": [198, 125, 90, 70, 65],
        "ชพส": [45, 38, 32, 28, 22]
    })

    with col_death1:
        st.caption("5 อันดับสาเหตุการเสียชีวิต ช.พ.ค.")
        fig_d1 = px.bar(death_data, x="ชพค", y="สาเหตุ", orientation='h', color="สาเหตุ",
                        color_discrete_sequence=['#FF7043', '#26C6DA', '#AB47BC', '#FBC02D', '#66BB6A'])
        fig_d1.update_layout(showlegend=False, height=300, yaxis={'categoryorder':'total ascending'})
        st.plotly_chart(fig_d1, use_container_width=True)

    with col_death2:
        st.caption("5 อันดับสาเหตุการเสียชีวิต ช.พ.ส.")
        fig_d2 = px.bar(death_data, x="ชพส", y="สาเหตุ", orientation='h', color="สาเหตุ",
                        color_discrete_sequence=['#FF7043', '#AB47BC', '#26C6DA', '#FBC02D', '#66BB6A'])
        fig_d2.update_layout(showlegend=False, height=300, yaxis={'categoryorder':'total ascending'})
        st.plotly_chart(fig_d2, use_container_width=True)

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

