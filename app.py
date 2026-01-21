import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# --- 1. CONFIGURATION & STYLE ---
st.set_page_config(page_title="EIS Platform", layout="wide", page_icon="🏛️")

# Injecting Sarabun Font and Custom CSS for specific design themes [cite: 5, 6, 7]
st.markdown("""
    <link href="https://fonts.googleapis.com/css2?family=Sarabun:wght@300;400;500;700&display=swap" rel="stylesheet">
    <style>
        html, body, [class*="css"] {
            font-family: 'Sarabun', sans-serif !important;
        }
        /* Login Container */
        .login-box {
            background-color: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
            max-width: 400px;
            margin: 50px auto;
            border-top: 5px solid #E91E63;
        }
        /* EIS Dashboard: Card Styles */
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
        .finance-header {
            background-color: #E3F2FD;
            padding: 10px;
            border-left: 5px solid #2196F3;
            margin-bottom: 15px;
            font-weight: bold;
            border-radius: 0 5px 5px 0;
        }
        /* Custom metric styles */
        .stat-value { font-size: 28px; font-weight: bold; margin: 0; }
        .stat-label { color: grey; font-size: 14px; }
        .stat-up { color: #4CAF50; font-weight: bold; font-size: 14px; }
        .stat-down { color: #E91E63; font-weight: bold; font-size: 14px; }
        
        /* Finance Color Cards */
        .fin-card-blue { background-color: #00BCD4; color: white; padding: 15px; border-radius: 8px; text-align: center; }
        .fin-card-green { background-color: #66BB6A; color: white; padding: 15px; border-radius: 8px; text-align: center; }
        .fin-card-gold { background-color: #FBC02D; color: white; padding: 15px; border-radius: 8px; text-align: center; }
    </style>
""", unsafe_allow_html=True)

# --- 2. SESSION STATE (Authentication) ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.role = None
    st.session_state.username = ""

# --- 3. LOGIN PAGE [cite: 10] ---
def login_page():
    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        st.markdown('<div class="login-box">', unsafe_allow_html=True)
        st.markdown("<h2 style='text-align: center;'>🔐 เข้าสู่ระบบ (Login)</h2>", unsafe_allow_html=True)
        
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        
        if st.button("Sign In", use_container_width=True):
            # Roles definition [cite: 12, 13, 14]
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

# --- 4. PAGE: EIS DASHBOARD (Executive Summary) [cite: 20] ---
def show_eis_dashboard():
    # Header [cite: 21]
    st.markdown("""
        <div style="background-color: #F5F5F5; padding: 15px; border-radius: 5px; margin-bottom: 20px;">
            <h2 style="margin:0; color:#333;">📊 บทสรุปผู้บริหาร (Executive Summary)</h2>
        </div>
    """, unsafe_allow_html=True)
    
    # Filters
    c1, c2, c3, c4 = st.columns(4)
    with c1: st.selectbox("ช่วงเวลา", ["พฤศจิกายน", "ธันวาคม"], index=0)
    with c2: st.selectbox("ปี", ["2568", "2567"], index=0)
    
    st.write("---")

    # --- ROW 1: MEMBER OVERVIEW [cite: 22] ---
    col_kpi1, col_kpi2 = st.columns(2)
    
    # Card 1: Ch.P.K. (Cyan Theme)
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
            fig.update_layout(height=180, margin=dict(l=0,r=0,t=0,b=0), xaxis_visible=False)
            st.plotly_chart(fig, use_container_width=True)
        with c_sub2:
            st.caption("📉 จำหน่าย ช.พ.ค.")
            fig = px.bar(x=[2242, 1345, 4500, 448], y=["ถอนชื่อ", "ลาออก", "ตาย", "อื่นๆ"], orientation='h', 
                         color_discrete_sequence=['#FBC02D', '#AB47BC', '#E91E63', '#BDBDBD'])
            fig.update_traces(marker_color=['#FBC02D', '#AB47BC', '#E91E63', '#BDBDBD'])
            fig.update_layout(height=180, margin=dict(l=0,r=0,t=0,b=0), xaxis_visible=False)
            st.plotly_chart(fig, use_container_width=True)

    # Card 2: Ch.P.S. (Purple Theme)
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
            fig.update_layout(height=180, margin=dict(l=0,r=0,t=0,b=0), xaxis_visible=False)
            st.plotly_chart(fig, use_container_width=True)
        with c_sub4:
            st.caption("📉 จำหน่าย ช.พ.ส.")
            fig = px.bar(x=[1047, 628, 3245, 314], y=["ถอนชื่อ", "ลาออก", "ตาย", "อื่นๆ"], orientation='h')
            fig.update_traces(marker_color=['#FBC02D', '#00BCD4', '#E91E63', '#BDBDBD'])
            fig.update_layout(height=180, margin=dict(l=0,r=0,t=0,b=0), xaxis_visible=False)
            st.plotly_chart(fig, use_container_width=True)

    # --- ROW 2: DEMOGRAPHICS ---
    st.markdown("#### 👥 ข้อมูลสมาชิก | DEMOGRAPHIC")
    d1, d2, d3, d4 = st.columns(4)
    
    with d1:
        st.caption("สัดส่วนเพศ ช.พ.ค.")
        fig = px.pie(values=[38, 62], names=["ชาย", "หญิง"], hole=0.6, color_discrete_sequence=['#03A9F4', '#E91E63'])
        fig.update_layout(height=200, margin=dict(l=20,r=20,t=0,b=20), showlegend=True, legend=dict(orientation="h"))
        st.plotly_chart(fig, use_container_width=True)
    with d2:
        st.caption("กลุ่มอายุ ช.พ.ค.")
        fig = px.bar(x=["<40", "40-49", "50-59", "60-69", "≥70"], y=[8, 18, 32, 28, 14], color_discrete_sequence=['#FFCA28'])
        fig.update_layout(height=200, margin=dict(l=0,r=0,t=0,b=0), xaxis_title=None)
        st.plotly_chart(fig, use_container_width=True)
    with d3:
        st.caption("สัดส่วนเพศ ช.พ.ส.")
        fig = px.pie(values=[42, 58], names=["ชาย", "หญิง"], hole=0.6, color_discrete_sequence=['#03A9F4', '#E91E63'])
        fig.update_layout(height=200, margin=dict(l=20,r=20,t=0,b=20), showlegend=True, legend=dict(orientation="h"))
        st.plotly_chart(fig, use_container_width=True)
    with d4:
        st.caption("กลุ่มอายุ ช.พ.ส.")
        fig = px.bar(x=["<40", "40-49", "50-59", "60-69", "≥70"], y=[5, 12, 25, 35, 23], color_discrete_sequence=['#AB47BC'])
        fig.update_layout(height=200, margin=dict(l=0,r=0,t=0,b=0), xaxis_title=None)
        st.plotly_chart(fig, use_container_width=True)

    # --- ROW 3: CAUSES OF DEATH ---
    st.markdown("#### ⚰️ สาเหตุการเสียชีวิต")
    cd1, cd2 = st.columns(2)
    death_causes = ["โรคมะเร็ง", "โรคปอด", "โรคหัวใจ", "โรคชรา", "โรคสมอง"]
    
    with cd1:
        st.caption("5 อันดับสาเหตุการเสียชีวิต ช.พ.ค.")
        fig = px.bar(x=[198, 125, 90, 70, 65], y=death_causes, orientation='h', 
                     color=death_causes, color_discrete_sequence=px.colors.qualitative.Bold)
        fig.update_layout(height=250, showlegend=False, yaxis={'categoryorder':'total ascending'})
        st.plotly_chart(fig, use_container_width=True)
    with cd2:
        st.caption("5 อันดับสาเหตุการเสียชีวิต ช.พ.ส.")
        fig = px.bar(x=[45, 32, 38, 28, 22], y=death_causes, orientation='h',
                     color=death_causes, color_discrete_sequence=px.colors.qualitative.Bold)
        fig.update_layout(height=250, showlegend=False, yaxis={'categoryorder':'total ascending'})
        st.plotly_chart(fig, use_container_width=True)

    # --- ROW 4: FINANCE ---
    st.markdown('<div class="finance-header">💳 การนำส่งเงิน & งบการเงิน</div>', unsafe_allow_html=True)
    f1, f2 = st.columns(2)
    
    # Finance Ch.P.K.
    with f1:
        st.markdown("**💰 เงินสงเคราะห์ ช.พ.ค.**")
        fc1, fc2, fc3 = st.columns(3)
        fc1.markdown('<div class="fin-card-blue"><h5>879 ราย</h5><small>ผู้วายชนม์</small></div>', unsafe_allow_html=True)
        fc2.markdown('<div class="fin-card-green"><h5>879.-</h5><small>รายศพ</small></div>', unsafe_allow_html=True)
        fc3.markdown('<div class="fin-card-gold" style="color:black"><h5>900K.-</h5><small>ครอบครัว</small></div>', unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        # Payment Status
        col_s1, col_s2, col_s3 = st.columns(3)
        col_s1.metric("นำส่งในกำหนด", "90.64%", "834,394 ราย")
        col_s2.metric("ค้างชำระ", "9.36%", "84,478 ราย", delta_color="inverse")
        col_s3.metric("จว. ครบ", "66/77", "จังหวัด")
        
        # Trend Chart
        df_trend = pd.DataFrame({'งวด': [f'งวด {i}' for i in range(1,11)], 'อัตรา': [87.5, 87.8, 89.5, 89.1, 90, 90.5, 90.2, 90.8, 90.5, 90.9]})
        fig = px.line(df_trend, x='งวด', y='อัตรา', markers=True, title="แนวโน้มอัตราการชำระ ช.พ.ค.")
        fig.update_traces(line_color='#00ACC1', fill='tozeroy')
        fig.update_layout(height=250, margin=dict(t=30))
        st.plotly_chart(fig, use_container_width=True)

    # Finance Ch.P.S.
    with f2:
        st.markdown("**💰 เงินสงเคราะห์ ช.พ.ส.**")
        fc4, fc5, fc6 = st.columns(3)
        fc4.markdown('<div class="fin-card-blue"><h5>383 ราย</h5><small>ผู้วายชนม์</small></div>', unsafe_allow_html=True)
        fc5.markdown('<div class="fin-card-green"><h5>383.-</h5><small>รายศพ</small></div>', unsafe_allow_html=True)
        fc6.markdown('<div class="fin-card-gold" style="color:black"><h5>368K.-</h5><small>ครอบครัว</small></div>', unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        # Payment Status
        col_s4, col_s5, col_s6 = st.columns(3)
        col_s4.metric("นำส่งในกำหนด", "91.25%", "357,178 ราย")
        col_s5.metric("ค้างชำระ", "8.75%", "35,565 ราย", delta_color="inverse")
        col_s6.metric("จว. ครบ", "71/77", "จังหวัด")
        
        # Trend Chart
        df_trend2 = pd.DataFrame({'งวด': [f'งวด {i}' for i in range(1,11)], 'อัตรา': [88.2, 89.3, 92.8, 94.2, 94, 90.8, 89.5, 93.5, 92.1, 92.8]})
        fig = px.line(df_trend2, x='งวด', y='อัตรา', markers=True, title="แนวโน้มอัตราการชำระ ช.พ.ส.")
        fig.update_traces(line_color='#8E24AA', fill='tozeroy')
        fig.update_layout(height=250, margin=dict(t=30))
        st.plotly_chart(fig, use_container_width=True)

# --- 5. PAGE: LEGAL DASHBOARD ---
def show_legal_dashboard():
    st.title("⚖️ Dashboard นิติการ")
    
    # KPI Metrics
    k1, k2, k3, k4 = st.columns(4)
    k1.metric("คดีทั้งหมด", "45 เรื่อง")
    k2.metric("อยู่ระหว่างดำเนินการ", "28 เรื่อง")
    k3.metric("เสร็จสิ้น", "17 เรื่อง")
    k4.metric("มูลค่าความเสียหาย", "1.25 ล้านบาท")
    
    st.write("---")
    
    # Charts
    lc1, lc2 = st.columns([2, 1])
    with lc1:
        st.subheader("ภาระงานตามกลุ่ม")
        df_work = pd.DataFrame({
            "กลุ่ม": ["สืบสวน", "อุทธรณ์", "ร้องเรียน", "ละเมิด", "คดี"],
            "Pending": [9, 5, 6, 2, 6],
            "Done": [3, 5, 4, 2, 4]
        })
        fig = px.bar(df_work, y="กลุ่ม", x=["Pending", "Done"], orientation='h', barmode='stack', 
                     color_discrete_map={"Pending": "#00BCD4", "Done": "#66BB6A"})
        st.plotly_chart(fig, use_container_width=True)
    
    with lc2:
        st.subheader("สถานะรวม")
        fig = px.pie(values=[28, 17], names=["Pending", "Done"], hole=0.6, 
                     color_discrete_sequence=["#00BCD4", "#66BB6A"])
        fig.add_annotation(text="37.8%", showarrow=False, font_size=20)
        st.plotly_chart(fig, use_container_width=True)
    
    # Table
    st.subheader("📋 รายการคดีล่าสุด")
    df_table = pd.DataFrame({
        "ลำดับ": [1, 2, 3, 4],
        "เรื่อง": ["คดีแต่งตั้ง", "เลิกจ้าง", "ยักยอก", "เพิกถอนคำสั่ง"],
        "ศาล": ["ปกครอง", "แพ่ง", "อาญา", "ปกครองสูงสุด"],
        "สถานะ": ["ศาลชั้นต้น", "อุทธรณ์", "เสร็จสิ้น", "ฎีกา"]
    })
    st.dataframe(df_table, use_container_width=True, hide_index=True)

# --- 6. PAGE: ADMIN PANEL ---
def show_admin_panel():
    st.title("⚙️ Admin Control Panel")
    st.write("จัดการผู้ใช้งานและสิทธิ์การเข้าถึง")
    
    df_users = pd.DataFrame({
        "Username": ["admin", "superuser", "user"],
        "Role": ["Admin", "Superuser", "User"],
        "Status": ["Active", "Active", "Active"]
    })
    st.table(df_users)

# --- 7. MAIN APP LOGIC & NAVIGATION [cite: 16, 17] ---
if not st.session_state.logged_in:
    login_page()
else:
    # Sidebar Navigation
    st.sidebar.title(f"👤 {st.session_state.username}")
    st.sidebar.write(f"Role: **{st.session_state.role}**")
    
    if st.sidebar.button("🚪 ออกจากระบบ (Log off)"):
        st.session_state.logged_in = False
        st.rerun()
        
    st.sidebar.markdown("---")
    
    # Menu Access Control [cite: 14]
    menu_options = []
    
    # Everyone sees Executive Dashboard
    menu_options.append("EIS Dashboard (บทสรุปผู้บริหาร)")
    
    # Superuser & Admin see Legal Dashboard [cite: 13]
    if st.session_state.role in ["Superuser", "Admin"]:
        menu_options.append("Legal Dashboard")
        
    # Only Admin sees Admin Panel [cite: 12]
    if st.session_state.role == "Admin":
        menu_options.append("Admin Panel")
        
    selection = st.sidebar.radio("เลือกเมนู:", menu_options)
    
    # Router
    if "EIS Dashboard" in selection:
        show_eis_dashboard()
    elif "Legal Dashboard" in selection:
        show_legal_dashboard()
    elif "Admin Panel" in selection:
        show_admin_panel()
