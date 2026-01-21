import streamlit as st
import plotly.express as px
from utils.styles import render_header
from utils.data_mock import get_dashboard_data

def show_view():
    render_header("📊 บทสรุปผู้บริหาร (Executive Summary)", border_color="#607D8B")

    # Filters
    thai_months = ["มกราคม", "กุมภาพันธ์", "มีนาคม", "เมษายน", "พฤษภาคม", "มิถุนายน", "กรกฎาคม", "สิงหาคม", "กันยายน", "ตุลาคม", "พฤศจิกายน", "ธันวาคม"]
    years = ["2568", "2567", "2566"]
    c1, c2, c3, c4 = st.columns(4)
    with c1: sel_month = st.selectbox("ช่วงเวลา", thai_months, index=10)
    with c2: sel_year = st.selectbox("ปี", years, index=0)

    data = get_dashboard_data(sel_year, sel_month)
    st.write("---")

    # KPIS
    c1, c2 = st.columns(2)
    with c1:
        st.markdown(f"""<div class="card-cpk"><h3>ช.พ.ค.</h3><div style="display:flex; justify-content:space-around;"><p class="stat-value" style="color:#00ACC1;">{data['cpk']['total']}</p> <p class="stat-up">{data['cpk']['new']} เพิ่ม</p> <p class="stat-down">{data['cpk']['resign']} จำหน่าย</p></div></div>""", unsafe_allow_html=True)
        fig = px.bar(x=data['cpk']['apply_vals'], y=["สมัคร", "ขอกลับ"], orientation='h', color_discrete_sequence=['#4CAF50'])
        fig.update_layout(height=180, margin=dict(l=0,r=0,t=0,b=0), font_family="Kanit")
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        st.markdown(f"""<div class="card-cps"><h3>ช.พ.ส.</h3><div style="display:flex; justify-content:space-around;"><p class="stat-value" style="color:#8E24AA;">{data['cps']['total']}</p> <p class="stat-up">{data['cps']['new']} เพิ่ม</p> <p class="stat-down">{data['cps']['resign']} จำหน่าย</p></div></div>""", unsafe_allow_html=True)
        fig = px.bar(x=data['cps']['apply_vals'], y=["สมัคร", "ขอกลับ"], orientation='h', color_discrete_sequence=['#4CAF50'])
        fig.update_layout(height=180, margin=dict(l=0,r=0,t=0,b=0), font_family="Kanit")
        st.plotly_chart(fig, use_container_width=True)

    # Finance
    st.markdown("### 💳 การนำส่งเงิน & งบการเงิน")
    f1, f2 = st.columns(2)
    with f1:
        st.caption(f"แนวโน้มการชำระ ช.พ.ค. ({data['finance']['cpk_paid']})")
        df_trend = pd.DataFrame({'M': range(12), 'V': data['finance']['cpk_trend']})
        fig = px.line(df_trend, x='M', y='V', markers=True)
        fig.update_layout(height=200, margin=dict(t=10,b=10), font_family="Kanit")
        st.plotly_chart(fig, use_container_width=True)
    with f2:
        st.caption(f"แนวโน้มการชำระ ช.พ.ส. ({data['finance']['cps_paid']})")
        df_trend = pd.DataFrame({'M': range(12), 'V': data['finance']['cps_trend']})
        fig = px.line(df_trend, x='M', y='V', markers=True)
        fig.update_traces(line_color='#8E24AA')
        fig.update_layout(height=200, margin=dict(t=10,b=10), font_family="Kanit")
        st.plotly_chart(fig, use_container_width=True)
    import pandas as pd # Import needed inside function or at top
