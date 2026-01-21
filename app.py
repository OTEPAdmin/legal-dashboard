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
        .sub-header { background-color: #f8f9fa; padding: 5px 15px; border-radius: 5px; margin: 15px 0; border-left: 5px solid #5f6368; font-weight: bold; border-bottom: 1px solid #dee2e6; }
        .kpi-card { background-color: white; padding: 15px; border-radius: 10px; border: 1px solid #e0e0e0; text-align: center; height: 100%; }
        .finance-card { padding: 15px; border-radius: 8px; color: white; text-align: center; min-height: 100px; display: flex; flex-direction: column; justify-content: center; }
        .metric-sub { font-size: 12px; color: #666; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. SESSION STATE FOR LOGIN ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = True  # ตั้งเป็น True เพื่อความสะดวกในการทดสอบ
    st.session_state.role = "Admin"
    st.session_state.name = "ผู้ดูแลระบบ"

# --- 4. PAGE: EIS DASHBOARD (COMPLETE VERSION) ---
def show_eis_dashboard():
    # --- Filter Section ---
    st.markdown('<div class="executive-header"><h2>📊 บทสรุปผู้บริหาร (Executive Summary)</h2></div>', unsafe_allow_html=True)
    
    with st.container():
        f1, f2, f3, f4 = st.columns(4)
        f1.selectbox("ช่วงเวลา", ["กุมภาพันธ์", "มกราคม"], index=0)
        f2.selectbox("ปี", ["2568", "2567"], index=0)
        f3.selectbox("ถึง", ["กุมภาพันธ์"], index=0)
        f4.selectbox("ปี", ["2568"], index=0)

    # --- SECTION 1: ภาพรวมสมาชิก (image_10ab00.png) ---
    st.markdown('<div class="sub-header">👥 ภาพรวมสมาชิก ช.พ.ค. และ ช.พ.ส.</div>', unsafe_allow_html=True)
    
    col_mem1, col_mem2 = st.columns(2)
    with col_mem1:
        st.markdown("""
            <div class="kpi-card" style="border-top: 5px solid #0097a7;">
                <p style="text-align:left; color:#5f6368; font-weight:bold;">👥 ภาพรวมสมาชิก ช.พ.ค. <span style="float:right; font-weight:normal;">ปี 2568</span></p>
                <div style="display:flex; justify-content:space-around; align-items:center;">
                    <div><h2 style="color:#0097a7; margin:0;">933,962</h2><p class="metric-sub">จำนวนสมาชิก</p></div>
                    <div><h2 style="color:#43a047; margin:0;">12,456</h2><p class="metric-sub">สมาชิกเพิ่ม</p></div>
                    <div><h2 style="color:#e91e63; margin:0;">8,967</h2><p class="metric-sub">จำหน่าย</p></div>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        c1, c2 = st.columns(2)
        with c1:
            st.caption("📈 สมาชิกเพิ่ม ช.พ.ค.")
            fig1 = px.bar(x=[10587, 1869], y=["สมัคร", "ขอกลับ"], orientation='h', color_discrete_sequence=['#6ECB93'])
            fig1.update_layout(height=150, margin=dict(l=0,r=0,t=0,b=0), xaxis_title=None, yaxis_title=None)
            st.plotly_chart(fig1, use_container_width=True)
        with c2:
            st.caption("📉 จำหน่าย ช.พ.ค.")
            fig2 = px.bar(x=[2242, 1345, 4500, 448], y=["ถอนชื่อ", "ลาออก", "ตาย", "อื่นๆ"], orientation='h', color_discrete_sequence=['#E91E63'])
            fig2.update_layout(height=150, margin=dict(l=0,r=0,t=0,b=0), xaxis_title=None, yaxis_title=None)
            st.plotly_chart(fig2, use_container_width=True)

    with col_mem2:
        st.markdown("""
            <div class="kpi-card" style="border-top: 5px solid #8e24aa;">
                <p style="text-align:left; color:#5f6368; font-weight:bold;">👥 ภาพรวมสมาชิก ช.พ.ส. <span style="float:right; font-weight:normal;">ปี 2568</span></p>
                <div style="display:flex; justify-content:space-around; align-items:center;">
                    <div><h2 style="color:#8e24aa; margin:0;">287,654</h2><p class="metric-sub">จำนวนสมาชิก</p></div>
                    <div><h2 style="color:#43a047; margin:0;">4,532</h2><p class="metric-sub">สมาชิกเพิ่ม</p></div>
                    <div><h2 style="color:#e91e63; margin:0;">5,234</h2><p class="metric-sub">จำหน่าย</p></div>
                </div>
            </div>
        """, unsafe_allow_html=True)

        c1, c2 = st.columns(2)
        with c1:
            st.caption("📈 สมาชิกเพิ่ม ช.พ.ส.")
            fig3 = px.bar(x=[3626, 906], y=["สมัคร", "ขอกลับ"], orientation='h', color_discrete_sequence=['#6ECB93'])
            fig3.update_layout(height=150, margin=dict(l=0,r=0,t=0,b=0), xaxis_title=None, yaxis_title=None)
            st.plotly_chart(fig3, use_container_width=True)
        with c2:
            st.caption("📉 จำหน่าย ช.พ.ส.")
            fig4 = px.bar(x=[1047, 628, 3245, 314], y=["ถอนชื่อ", "ลาออก", "ตาย", "อื่นๆ"], orientation='h', color_discrete_sequence=['#E91E63'])
            fig4.update_layout(height=150, margin=dict(l=0,r=0,t=0,b=0), xaxis_title=None, yaxis_title=None)
            st.plotly_chart(fig4, use_container_width=True)

    # --- SECTION 2: DEMOGRAPHIC & DEATH CAUSES (image_10ab00.png) ---
    st.write("<br>", unsafe_allow_html=True)
    st.markdown('<div class="sub-header">👥 ข้อมูลสมาชิก | DEMOGRAPHIC</div>', unsafe_allow_html=True)
    d1, d2, d3, d4 = st.columns(4)
    with d1:
        st.caption("สัดส่วนเพศ ช.พ.ค.")
        fig_p1 = px.pie(values=[38, 62], names=["ชาย 38%", "หญิง 62%"], hole=0.7, color_discrete_sequence=['#03A9F4', '#E91E63'])
        fig_p1.update_layout(height=220, margin=dict(t=0,b=0,l=0,r=0), showlegend=True, legend=dict(orientation="h", y=-0.1))
        st.plotly_chart(fig_p1, use_container_width=True)
    with d2:
        st.caption("กลุ่มอายุ ช.พ.ค.")
        fig_a1 = px.bar(x=["<40", "40-49", "50-59", "60-69", ">70"], y=[8, 12, 25, 32, 22], color_discrete_sequence=['#FFC107'])
        fig_a1.update_layout(height=220, margin=dict(t=10,b=0,l=0,r=0), xaxis_title=None, yaxis_title=None)
        st.plotly_chart(fig_a1, use_container_width=True)
    with d3:
        st.caption("สัดส่วนเพศ ช.พ.ส.")
        fig_p2 = px.pie(values=[42, 58], names=["ชาย 42%", "หญิง 58%"], hole=0.7, color_discrete_sequence=['#03A9F4', '#E91E63'])
        fig_p2.update_layout(height=220, margin=dict(t=0,b=0,l=0,r=0), showlegend=True, legend=dict(orientation="h", y=-0.1))
        st.plotly_chart(fig_p2, use_container_width=True)
    with d4:
        st.caption("กลุ่มอายุ ช.พ.ส.")
        fig_a2 = px.bar(x=["<40", "40-49", "50-59", "60-69", ">70"], y=[5, 10, 25, 35, 25], color_discrete_sequence=['#9C27B0'])
        fig_a2.update_layout(height=220, margin=dict(t=10,b=0,l=0,r=0), xaxis_title=None, yaxis_title=None)
        st.plotly_chart(fig_a2, use_container_width=True)

    # --- SECTION 3: การนำส่งเงิน & งบการเงิน (image_10c166.png) ---
    st.write("<br>", unsafe_allow_html=True)
    st.markdown('<div class="sub-header">💳 การนำส่งเงิน & งบการเงิน (ประจำงวด พฤศจิกายน 2568)</div>', unsafe_allow_html=True)
    
    col_fin1, col_fin2 = st.columns(2)
    with col_fin1:
        st.markdown('<p style="font-weight:bold; color:#5f6368;">💰 เงินสงเคราะห์ ช.พ.ค.</p>', unsafe_allow_html=True)
        c1, c2, c3 = st.columns(3)
        c1.markdown('<div class="finance-card" style="background-color:#0097a7;"><h3>879 ราย</h3><p>จำนวนผู้ตาย</p></div>', unsafe_allow_html=True)
        c2.markdown('<div class="finance-card" style="background-color:#43a047;"><h3>879.-</h3><p>เงินสงเคราะห์รายศพ</p></div>', unsafe_allow_html=True)
        c3.markdown('<div class="finance-card" style="background-color:#fbc02d; color:black;"><h3>900,000.-</h3><p>เงินครอบครัว</p></div>', unsafe_allow_html=True)
        
        st.write("**สถานะการนำส่งเงิน ช.พ.ค.**")
        sc1, sc2, sc3 = st.columns(3)
        sc1.metric("นำส่งภายในกำหนด", "90.64%", "834,394 ราย")
        sc2.metric("ค้างชำระ", "9.36%", "84,478 ราย")
        sc3.metric("จังหวัดส่งครบ", "66/77", "จังหวัด")

    with col_fin2:
        st.markdown('<p style="font-weight:bold; color:#5f6368;">💰 เงินสงเคราะห์ ช.พ.ส.</p>', unsafe_allow_html=True)
        c1, c2, c3 = st.columns(3)
        c1.markdown('<div class="finance-card" style="background-color:#0097a7;"><h3>383 ราย</h3><p>จำนวนผู้ตาย</p></div>', unsafe_allow_html=True)
        c2.markdown('<div class="finance-card" style="background-color:#43a047;"><h3>383.-</h3><p>เงินสงเคราะห์รายศพ</p></div>', unsafe_allow_html=True)
        c3.markdown('<div class="finance-card" style="background-color:#fbc02d; color:black;"><h3>368,311.-</h3><p>เงินครอบครัว</p></div>', unsafe_allow_html=True)
        
        st.write("**สถานะการนำส่งเงิน ช.พ.ส.**")
        sc1, sc2, sc3 = st.columns(3)
        sc1.metric("นำส่งภายในกำหนด", "91.25%", "357,178 ราย")
        sc2.metric("ค้างชำระ", "8.75%", "35,565 ราย")
        sc3.metric("จังหวัดส่งครบ", "71/77", "จังหวัด")

    # --- SECTION 4: LINE CHARTS (image_10c166.png) ---
    st.write("<br>", unsafe_allow_html=True)
    cg1, cg2 = st.columns(2)
    months = [f"งวด {i}" for i in range(1, 11)]
    
    with cg1:
        st.caption("📈 แนวโน้มอัตราการชำระ ช.พ.ค. ปี 2568")
        fig_l1 = px.line(x=months, y=[87.5, 87.8, 89.5, 89.1, 90, 90.5, 90.2, 90.8, 90.5, 90.9], markers=True)
        fig_l1.update_traces(line_color='#0097a7', fill='tozeroy')
        fig_l1.update_layout(height=280, font_family="Sarabun", xaxis_title=None, yaxis_title="อัตราการชำระ (%)")
        st.plotly_chart(fig_l1, use_container_width=True)
        
    with cg2:
        st.caption("📈 แนวโน้มอัตราการชำระ ช.พ.ส. ปี 2568")
        fig_l2 = px.line(x=months, y=[88.2, 89.3, 92.8, 94.2, 94, 90.8, 89.5, 93.5, 92.1, 92.8], markers=True)
        fig_l2.update_traces(line_color='#8e24aa', fill='tozeroy')
        fig_l2.update_layout(height=280, font_family="Sarabun", xaxis_title=None, yaxis_title="อัตราการชำระ (%)")
        st.plotly_chart(fig_l2, use_container_width=True)

# --- 5. MAIN EXECUTION ---
if st.session_state.logged_in:
    show_eis_dashboard()
else:
    st.warning("Please login to access the EIS Dashboard")
