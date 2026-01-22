import streamlit as st
import plotly.express as px
import pandas as pd
from utils.styles import render_header
from utils.data_loader import get_dashboard_data

def show_view():
    render_header("💰 รายได้ (Revenue Dashboard)", border_color="#FF9800")
    
    # Check if data exists to get years
    available_years = ["2568"]
    if 'df_rev' in st.session_state and not st.session_state['df_rev'].empty:
        df = st.session_state['df_rev']
        df['Year'] = df['Year'].astype(str)
        available_years = sorted(df['Year'].unique(), reverse=True)

    thai_months = ["มกราคม", "กุมภาพันธ์", "มีนาคม", "เมษายน", "พฤษภาคม", "มิถุนายน", 
                   "กรกฎาคม", "สิงหาคม", "กันยายน", "ตุลาคม", "พฤศจิกายน", "ธันวาคม"]
    
    c1, c2, c3, c4 = st.columns(4)
    with c1: sel_month = st.selectbox("ช่วงเวลา", thai_months, index=10)
    with c2: sel_year = st.selectbox("ปี", available_years, index=0)

    data = get_dashboard_data(sel_year, sel_month)
    st.write("---")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("รายได้รวม (ล้านบาท)", data['revenue']['total'], delta="1.2%")
    with col2:
        st.metric("จำนวนผู้ใช้บริการ (ราย)", data['revenue']['users'], delta="530")
    with col3:
        st.metric("รายได้เฉลี่ยต่อหัว (บาท)", data['revenue']['avg'], delta="15")

    st.write("---")
    
    st.markdown("### 🏥 สถิติการตรวจสุขภาพ")
    c1, c2 = st.columns([1, 2])
    
    with c1:
        s = data['revenue']['checkup_stats']
        st.markdown(f"""
        <div style="background:#FFF3E0; padding:15px; border-radius:10px;">
            <h4>จังหวัดที่ให้บริการ: <b>{s[0]}</b></h4>
            <h4>หน่วยบริการ: <b>{s[1]}</b></h4>
            <hr>
            <h4>ลงทะเบียน: <b style="color:#E65100;">{s[2]:,}</b></h4>
            <h4>เข้ารับบริการ: <b style="color:#43A047;">{s[3]:,}</b></h4>
        </div>
        """, unsafe_allow_html=True)
        
        rate = data['revenue']['checkup_rate'] * 100
        st.progress(rate/100, text=f"อัตราการเข้ารับบริการ {rate:.1f}%")

    with c2:
        df_age = pd.DataFrame({
            "Age Group": ["<30", "30-40", "41-50", "51-60", ">60"],
            "Count": data['revenue']['age_dist']
        })
        fig = px.bar(df_age, x="Age Group", y="Count", title="ช่วงอายุผู้รับบริการ", color_discrete_sequence=['#FF9800'])
        fig.update_layout(height=250, margin=dict(t=30, b=0), font_family="Kanit")
        st.plotly_chart(fig, use_container_width=True, key="revenue_age_chart")
