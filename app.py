import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# [cite_start]--- 1. PAGE CONFIGURATION & CSS INJECTION [cite: 3, 5, 7] ---
st.set_page_config(page_title="EIS Platform", layout="wide", page_icon="🏛️")

# Injecting Sarabun Font and Custom CSS for Cards
st.markdown("""
    <link href="https://fonts.googleapis.com/css2?family=Sarabun:wght@300;400;500;700&display=swap" rel="stylesheet">
    <style>
        html, body, [class*="css"] {
            font-family: 'Sarabun', sans-serif !important;
        }
        /* Custom Card Styles for EIS */
        .card-header-cyan {
            background-color: #e0f7fa;
            border-top: 5px solid #00acc1;
            padding: 15px;
            border-radius: 8px 8px 0 0;
            color: #006064;
            font-weight: bold;
        }
        .card-header-purple {
            background-color: #f3e5f5;
            border-top: 5px solid #8e24aa;
            padding: 15px;
            border-radius: 8px 8px 0 0;
            color: #4a148c;
            font-weight: bold;
        }
        .kpi-box {
            background-color: white;
            padding: 20px;
            border-radius: 0 0 8px 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
            text-align: center;
            border: 1px solid #eee;
        }
        .finance-card-blue { background-color: #00bcd4; color: white; padding: 15px; border-radius: 8px; text-align: center; }
        .finance-card-green { background-color: #66bb6a; color: white; padding: 15px; border-radius: 8px; text-align: center; }
        .finance-card-gold { background-color: #d4a017; color: white; padding: 15px; border-radius: 8px; text-align: center; }
        
        /* Login Box Style */
        .login-container {
            max-width: 400px;
            margin: 100px auto;
            padding: 30px;
            background-color: white;
            border-radius: 10px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
            border-top: 5px solid #e91e63;
        }
    </style>
""", unsafe_allow_html=True)

# [cite_start]--- 2. SESSION STATE MANAGEMENT [cite: 15] ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.role = None
    st.session_state.username = ""

# [cite_start]--- 3. AUTHENTICATION LOGIC [cite: 9, 10, 11] ---
def login():
    st.markdown('<div class="login-container">', unsafe_allow_html=True)
    st.markdown("<h2 style='text-align: center; color: #333;'>🔐 EIS Login</h2>", unsafe_allow_html=True)
    
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    
    if st.button("Sign In", use_container_width=True):
        # [cite_start]Hardcoded credentials per requirements [cite: 12, 13, 14]
        if username == "admin" and password == "admin123":
            st.session_state.logged_in = True
            st.session_state.role = "Admin"
            st.session_state.username = "Admin"
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
            st.error("Invalid Username or Password")
    
    st.markdown("</div>", unsafe_allow_html=True)

# [cite_start]--- 4. DASHBOARD PAGE: EIS (EXECUTIVE SUMMARY) [cite: 20, 22] ---
def show_eis_dashboard():
    [cite_start]st.markdown("## 📊 บทสรุปผู้บริหาร (Executive Summary)") # [cite: 21]
    
    # --- SECTION A: MEMBER OVERVIEW (Matches image_10ab00.png) ---
    col1, col2 = st.columns(2)
    
    # --- Ch.P.K. (Cyan Theme) ---
    with col1:
        st.markdown("""
            <div class="card-header-cyan">👥 ภาพรวมสมาชิก ช.พ.ค. <span style="float:right">ปี 2568</span></div>
            <div class="kpi-box">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div><h2 style="color:#00acc1; margin:0;">933,962</h2><p style="color:grey; font-size:12px;">จำนวนสมาชิก</p></div>
                    <div><h3 style="color:#4caf50; margin:0;">12,456</h3><p style="color:grey; font-size:12px;">สมาชิกเพิ่ม</p></div>
                    <div><h3 style="color:#e91e63; margin:0;">8,967</h3><p style="color:grey; font-size:12px;">จำหน่าย</p></div>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        # Mock Data for Charts
        df_new_cpk = pd.DataFrame({'Status': ['สมัคร', 'ขอกลับ'], 'Value': [10587, 1869]})
        df_rem_cpk = pd.DataFrame({'Reason': ['ถอนชื่อ', 'ลาออก', 'ตาย', 'อื่นๆ'], 'Value': [2242, 1345, 4500, 448]})
        
        c1, c2 = st.columns(2)
        with c1:
            st.caption("📈 สมาชิกเพิ่ม ช.พ.ค.")
            fig = px.bar(df_new_cpk, x='Value', y='Status', orientation='h', text='Value', color_discrete_sequence=['#4caf50'])
            fig.update_layout(height=200, margin=dict(l=0,r=0,t=0,b=0), xaxis_visible=False, yaxis_title=None)
            st.plotly_chart(fig, use_container_width=True)
        with c2:
            st.caption("📉 จำหน่าย ช.พ.ค.")
            fig = px.bar(df_rem_cpk, x='Value', y='Reason', orientation='h', text='Value', 
                         color='Reason', color_discrete_map={'ถอนชื่อ':'#fbc02d', 'ลาออก':'#ab47bc', 'ตาย':'#e91e63', 'อื่นๆ':'#9e9e9e'})
            fig.update_layout(height=200, margin=dict(l=0,r=0,t=0,b=0), xaxis_visible=False, yaxis_title=None, showlegend=False)
            st.plotly_chart(fig, use_container_width=True)

    # --- Ch.P.S. (Purple Theme) ---
    with col2:
        st.markdown("""
            <div class="card-header-purple">👥 ภาพรวมสมาชิก ช.พ.ส. <span style="float:right">ปี 2568</span></div>
            <div class="kpi-box">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div><h2 style="color:#8e24aa; margin:0;">287,654</h2><p style="color:grey; font-size:12px;">จำนวนสมาชิก</p></div>
                    <div><h3 style="color:#4caf50; margin:0;">4,532</h3><p style="color:grey; font-size:12px;">สมาชิกเพิ่ม</p></div>
                    <div><h3 style="color:#e91e63; margin:0;">5,234</h3><p style="color:grey; font-size:12px;">จำหน่าย</p></div>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        df_new_cps = pd.DataFrame({'Status': ['สมัคร', 'ขอกลับ'], 'Value': [3626, 906]})
        df_rem_cps = pd.DataFrame({'Reason': ['ถอนชื่อ', 'ลาออก', 'ตาย', 'อื่นๆ'], 'Value': [1047, 628, 3245, 314]})
        
        c3, c4 = st.columns(2)
        with c3:
            st.caption("📈 สมาชิกเพิ่ม ช.พ.ส.")
            fig = px.bar(df_new_cps, x='Value', y='Status', orientation='h', text='Value', color_discrete_sequence=['#4caf50'])
            fig.update_layout(height=200, margin=dict(l=0,r=0,t=0,b=0), xaxis_visible=False, yaxis_title=None)
            st.plotly_chart(fig, use_container_width=True)
        with c4:
            st.caption("📉 จำหน่าย ช.พ.ส.")
            fig = px.bar(df_rem_cps, x='Value', y='Reason', orientation='h', text='Value', 
                         color='Reason', color_discrete_map={'ถอนชื่อ':'#fbc02d', 'ลาออก':'#03a9f4', 'ตาย':'#e91e63', 'อื่นๆ':'#9e9e9e'})
            fig.update_layout(height=200, margin=dict(l=0,r=0,t=0,b=0), xaxis_visible=False, yaxis_title=None, showlegend=False)
            st.plotly_chart(fig, use_container_width=True)

    st.write("---")

    # --- SECTION B: DEMOGRAPHICS (Matches image_10ab00.png) ---
    st.subheader("👥 ข้อมูลสมาชิก | DEMOGRAPHIC")
    d1, d2, d3, d4 = st.columns(4)
    
    with d1:
        st.markdown("**สัดส่วนเพศ ช.พ.ค.**")
        fig = px.pie(values=[38, 62], names=['ชาย', 'หญิง'], hole=0.6, color_discrete_sequence=['#039be5', '#e91e63'])
        fig.update_layout(height=200, margin=dict(l=20,r=20,t=0,b=20), showlegend=True, legend=dict(orientation="h", y=-0.1))
        st.plotly_chart(fig, use_container_width=True)
    with d2:
        st.markdown("**กลุ่มอายุ ช.พ.ค.**")
        df_age = pd.DataFrame({'Age': ['<40', '40-49', '50-59', '60-69', '≥70'], 'Value': [8, 18, 32, 28, 14], 'Color': ['#26a69a', '#66bb6a', '#fbc02d', '#ab47bc', '#ff7043']})
        fig = px.bar(df_age, x='Age', y='Value', color='Age', color_discrete_sequence=df_age['Color'].tolist())
        fig.update_layout(height=200, margin=dict(l=0,r=0,t=0,b=0), showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
    with d3:
        st.markdown("**สัดส่วนเพศ ช.พ.ส.**")
        fig = px.pie(values=[42, 58], names=['ชาย', 'หญิง'], hole=0.6, color_discrete_sequence=['#039be5', '#e91e63'])
        fig.update_layout(height=200, margin=dict(l=20,r=20,t=0,b=20), showlegend=True, legend=dict(orientation="h", y=-0.1))
        st.plotly_chart(fig, use_container_width=True)
    with d4:
        st.markdown("**กลุ่มอายุ ช.พ.ส.**")
        df_age2 = pd.DataFrame({'Age': ['<40', '40-49', '50-59', '60-69', '≥70'], 'Value': [5, 12, 25, 35, 23], 'Color': ['#26a69a', '#66bb6a', '#fbc02d', '#ab47bc', '#ff7043']})
        fig = px.bar(df_age2, x='Age', y='Value', color='Age', color_discrete_sequence=df_age2['Color'].tolist())
        fig.update_layout(height=200, margin=dict(l=0,r=0,t=0,b=0), showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

    # --- SECTION C: CAUSE OF DEATH ---
    st.write("---")
    c_death1, c_death2 = st.columns(2)
    df_death = pd.DataFrame({
        'Cause': ['โรคมะเร็ง', 'โรคปอด', 'โรคหัวใจ', 'โรคชรา', 'โรคสมอง'],
        'CPK': [198, 125, 90, 70, 65],
        'CPS': [45, 32, 38, 28, 22]
    })
    
    with c_death1:
        st.markdown("**5 อันดับสาเหตุการเสียชีวิต ช.พ.ค.**")
        fig = px.bar(df_death, x='CPK', y='Cause', orientation='h', text='CPK', 
                     color='Cause', color_discrete_sequence=px.colors.qualitative.Bold)
        fig.update_layout(height=300, yaxis={'categoryorder':'total ascending'}, showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
    
    with c_death2:
        st.markdown("**5 อันดับสาเหตุการเสียชีวิต ช.พ.ส.**")
        fig = px.bar(df_death, x='CPS', y='Cause', orientation='h', text='CPS', 
                     color='Cause', color_discrete_sequence=px.colors.qualitative.Bold)
        fig.update_layout(height=300, yaxis={'categoryorder':'total ascending'}, showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

    # --- SECTION D: FINANCE (Matches image_10c166.png) ---
    st.markdown("### 💳 การนำส่งเงิน & งบการเงิน")
    
    fin_col1, fin_col2 = st.columns(2)
    
    # Left: Ch.P.K. Finance
    with fin_col1:
        st.markdown('<div class="card-header-cyan">💰 เงินสงเคราะห์ ช.พ.ค.</div>', unsafe_allow_html=True)
        st.markdown("""
            <div style="background-color:white; padding:15px; border:1px solid #eee;">
                <div style="display:flex; gap:10px;">
                    <div style="flex:1; background-color:#00bcd4; color:white; padding:10px; border-radius:5px; text-align:center;">
                        <small>จำนวนผู้ตาย</small><h3>879 ราย</h3>
                    </div>
                    <div style="flex:1; background-color:#66bb6a; color:white; padding:10px; border-radius:5px; text-align:center;">
                        <small>เงินสงเคราะห์รายศพ</small><h3>879.-</h3>
                    </div>
                    <div style="flex:1; background-color:#d4a017; color:white; padding:10px; border-radius:5px; text-align:center;">
                        <small>เงินสงเคราะห์ครอบครัว</small><h3>900,000.-</h3>
                    </div>
                </div>
                <div style="margin-top:15px; display:flex; justify-content:space-around; text-align:center;">
                    <div><h3 style="color:#4caf50; margin:0;">90.64%</h3><small>นำส่งภายในกำหนด</small></div>
                    <div><h3 style="color:#fbc02d; margin:0;">9.36%</h3><small>ค้างชำระ</small></div>
                    <div><h3 style="color:#8e24aa; margin:0;">66/77</h3><small>จังหวัดนำส่งครบ</small></div>
                </div>
            </div>
        """, unsafe_allow_html=True)
        # Line Chart
        df_trend1 = pd.DataFrame({'Period': [f'งวด {i}' for i in range(1,11)], 'Rate': [87.5, 87.8, 89.5, 89.1, 90.0, 90.5, 90.2, 90.8, 90.5, 90.9]})
        fig = px.line(df_trend1, x='Period', y='Rate', markers=True, title="แนวโน้มอัตราการชำระ ช.พ.ค. ปี 2568")
        fig.update_traces(line_color='#00acc1', fill='tozeroy')
        fig.update_layout(height=250, margin=dict(t=30), yaxis_range=[85, 92])
        st.plotly_chart(fig, use_container_width=True)

    # Right: Ch.P.S. Finance
    with fin_col2:
        st.markdown('<div class="card-header-purple">💰 เงินสงเคราะห์ ช.พ.ส.</div>', unsafe_allow_html=True)
        st.markdown("""
            <div style="background-color:white; padding:15px; border:1px solid #eee;">
                <div style="display:flex; gap:10px;">
                    <div style="flex:1; background-color:#00bcd4; color:white; padding:10px; border-radius:5px; text-align:center;">
                        <small>จำนวนผู้ตาย</small><h3>383 ราย</h3>
                    </div>
                    <div style="flex:1; background-color:#66bb6a; color:white; padding:10px; border-radius:5px; text-align:center;">
                        <small>เงินสงเคราะห์รายศพ</small><h3>383.-</h3>
                    </div>
                    <div style="flex:1; background-color:#d4a017; color:white; padding:10px; border-radius:5px; text-align:center;">
                        <small>เงินสงเคราะห์ครอบครัว</small><h3>368,311.-</h3>
                    </div>
                </div>
                <div style="margin-top:15px; display:flex; justify-content:space-around; text-align:center;">
                    <div><h3 style="color:#4caf50; margin:0;">91.25%</h3><small>นำส่งภายในกำหนด</small></div>
                    <div><h3 style="color:#fbc02d; margin:0;">8.75%</h3><small>ค้างชำระ</small></div>
                    <div><h3 style="color:#8e24aa; margin:0;">71/77</h3><small>จังหวัดนำส่งครบ</small></div>
                </div>
            </div>
        """, unsafe_allow_html=True)
        # Line Chart
        df_trend2 = pd.DataFrame({'Period': [f'งวด {i}' for i in range(1,11)], 'Rate': [88.2, 89.3, 92.8, 94.2, 94.0, 90.8, 89.5, 93.5, 92.1, 92.8]})
        fig = px.line(df_trend2, x='Period', y='Rate', markers=True, title="แนวโน้มอัตราการชำระ ช.พ.ส. ปี 2568")
        fig.update_traces(line_color='#8e24aa', fill='tozeroy')
        fig.update_layout(height=250, margin=dict(t=30), yaxis_range=[85, 96])
        st.plotly_chart(fig, use_container_width=True)

# [cite_start]--- 5. DASHBOARD PAGE: LEGAL (Matches legal-fullV2_P1.jpg) [cite: 1] ---
def show_legal_dashboard():
    st.markdown("## ⚖️ Dashboard นิติการ")
    
    # KPI Metrics
    k1, k2, k3, k4 = st.columns(4)
    k1.metric("ทั้งหมด", "45 เรื่อง", delta=None)
    k2.metric("อยู่ระหว่างดำเนินการ", "28 เรื่อง", delta="62.2%")
    k3.metric("ดำเนินการเสร็จสิ้น", "17 เรื่อง", delta="37.8%")
    k4.metric("มูลค่าความเสียหาย", "1.25 ล้านบาท")
    
    st.write("---")
    
    # Charts Row
    lc1, lc2 = st.columns([2, 1])
    with lc1:
        st.subheader("ภาระงานตามกลุ่ม (แยกสถานะ)")
        df_workload = pd.DataFrame({
            'Group': ['สืบสวน-วินัย', 'อุทธรณ์-ร้องทุกข์', 'ร้องเรียน', 'ละเมิด', 'คดี'],
            'Pending': [9, 5, 6, 2, 6],
            'Done': [3, 5, 4, 2, 4]
        })
        fig = px.bar(df_workload, y='Group', x=['Pending', 'Done'], orientation='h', barmode='stack',
                     color_discrete_map={'Pending': '#00bcd4', 'Done': '#66bb6a'})
        st.plotly_chart(fig, use_container_width=True)
        
    with lc2:
        st.subheader("สถานะการดำเนินการรวม")
        fig = px.pie(values=[28, 17], names=['อยู่ระหว่างดำเนินการ', 'เสร็จสิ้น'], hole=0.6, 
                     color_discrete_sequence=['#00bcd4', '#66bb6a'])
        fig.add_annotation(text="37.8%", showarrow=False, font_size=20)
        st.plotly_chart(fig, use_container_width=True)
    
    # Table Row
    st.subheader("📋 รายการคดีล่าสุด")
    df_cases = pd.DataFrame({
        'ลำดับ': [1, 2, 3, 4],
        'เรื่อง': ['คดีบรรจุแต่งตั้งตำแหน่ง', 'คดีเลิกจ้างไม่เป็นธรรม', 'คดียักยอกทรัพย์', 'คดีฟ้องเพิกถอนคำสั่ง'],
        'ประเภทคดี': ['ปกครอง', 'แพ่ง', 'อาญา', 'ปกครอง'],
        'สถานะ': ['ศาลชั้นต้น', 'ศาลอุทธรณ์', 'เสร็จสิ้น', 'ศาลฎีกา']
    })
    st.dataframe(df_cases, use_container_width=True, hide_index=True)

# [cite_start]--- 6. ADMIN PANEL [cite: 12] ---
def show_admin_panel():
    st.title("⚙️ Admin Control Panel")
    st.write("Manage Users & System Settings")
    st.info("Currently viewing as Administrator.")
    
    df_users = pd.DataFrame({
        'Username': ['admin', 'superuser', 'user'],
        'Role': ['Admin', 'Superuser', 'User'],
        'Last Login': ['2026-01-20', '2026-01-19', '2026-01-21']
    })
    st.table(df_users)

# [cite_start]--- 7. MAIN NAVIGATION LOGIC [cite: 16, 17, 18] ---
if not st.session_state.logged_in:
    login()
else:
    # Sidebar
    st.sidebar.markdown(f"### 👤 {st.session_state.username}")
    st.sidebar.write(f"Role: **{st.session_state.role}**")
    
    if st.sidebar.button("🚪 Log Off"):
        st.session_state.logged_in = False
        st.session_state.role = None
        st.rerun()
    
    st.sidebar.divider()
    
    # Role-Based Menu
    menu_options = []
    
    if st.session_state.role in ["User", "Superuser", "Admin"]:
        menu_options.append("EIS Dashboard")
    
    if st.session_state.role in ["Superuser", "Admin"]:
        menu_options.append("Legal Dashboard")
        
    if st.session_state.role == "Admin":
        menu_options.append("Admin Panel")
        
    choice = st.sidebar.radio("Navigate", menu_options)
    
    # Render Selected Page
    if choice == "EIS Dashboard":
        show_eis_dashboard()
    elif choice == "Legal Dashboard":
        show_legal_dashboard()
    elif choice == "Admin Panel":
        show_admin_panel()
