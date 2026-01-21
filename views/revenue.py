import streamlit as st
import plotly.express as px
import pandas as pd
from utils.styles import render_header
from utils.data_mock import get_dashboard_data

def show_view():
    render_header("รายได้ - โรงพยาบาล (Revenue)", border_color="#E91E63")
    c1, c2 = st.columns(2)
    with c1: sel_year = st.selectbox("ปีงบประมาณ", ["2568", "2567", "2566"])
    data = get_dashboard_data(sel_year, "มกราคม") # Month doesn't matter much for yearly view

    k1, k2, k3 = st.columns(3)
    k1.markdown(f"""<div class="rev-card-bg"><p class="rev-title">รายได้รวม</p><p class="rev-value">{data['revenue']['total']}</p><small>ล้านบาท</small></div>""", unsafe_allow_html=True)
    k2.markdown(f"""<div class="rev-card-bg"><p class="rev-title">ผู้รับบริการ</p><p class="rev-value">{data['revenue']['users']}</p><small>ราย</small></div>""", unsafe_allow_html=True)
    k3.markdown(f"""<div class="rev-card-bg"><p class="rev-title">เฉลี่ยต่อราย</p><p class="rev-value">{data['revenue']['avg']}</p><small>บาท</small></div>""", unsafe_allow_html=True)

    st.write("---")
    col1, col2 = st.columns([1, 2])
    with col1:
        st.markdown("#### 📍 สถานะ")
        st.progress(min(data['revenue']['checkup_rate'], 1.0))
        st.caption(f"Success Rate: {data['revenue']['checkup_rate']*100:.1f}%")
    with col2:
        st.markdown("#### 📊 กลุ่มอายุ")
        df_age = pd.DataFrame({"Age": ["20-30", "31-40", "41-50", "51-60", "60+"], "Count": data['revenue']['age_dist']})
        fig = px.bar(df_age, x="Age", y="Count", color="Age")
        fig.update_layout(font_family="Kanit", height=300)
        st.plotly_chart(fig, use_container_width=True)
