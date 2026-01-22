import streamlit as st
import plotly.express as px
import pandas as pd
from utils.styles import render_header
from utils.data_loader import get_dashboard_data

def show_view():
    # --- CHANGED TITLE HERE ---
    render_header("📊 บทสรุปผู้บริหาร", border_color="#607D8B")
    
    # Check if data exists in session to get years
    available_years = ["2568"]
    if 'df_eis' in st.session_state and not st.session_state['df_eis'].empty:
        df = st.session_state['df_eis']
        df['Year'] = df['Year'].astype(str)
        available_years = sorted(df['Year'].unique(), reverse=True)

    thai_months = ["มกราคม", "กุมภาพันธ์", "มีนาคม", "เมษายน", "พฤษภาคม", "มิถุนายน", 
                   "กรกฎาคม", "สิงหาคม", "กันยายน", "ตุลาคม", "พฤศจิกายน", "ธันวาคม"]
    
    c1, c2, c3, c4 = st.columns(4)
    with c1: sel_month = st.selectbox("ช่วงเวลา", thai_months, index=10)
    with c2: sel_year = st.selectbox("ปี", available_years, index=0)
    
    data = get_dashboard_data(sel_year, sel_month)
    st.write("---")

    c1, c2 = st.columns(2)
    
    with c1:
        st.markdown(f"""
            <div class="card-cpk">
                <h3>ช.พ.ค.</h3>
                <div style="display:flex; justify-content:space-around;">
                    <p class="stat-value" style="color:#00ACC1;">{data['cpk']['total']}</p> 
                    <p class="stat-up">{data['cpk']['new']} เพิ่ม</p> 
                    <p class="stat-down">{data['cpk']['resign']} จำหน่าย</p>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
        fig = px.bar(x=data['cpk']['apply_vals'], y=["สมัคร", "ขอกลับ"], orientation='h', color_discrete_sequence=['#4CAF50'])
        fig.update_layout(height=180, margin=dict(l=0,r=0,t=0,b=0), font_family="Kanit")
        st.plotly_chart(fig, use_container_width=True, key="chart_cpk_bar")

    with c2:
        st.markdown(f"""
            <div class="card-cps">
                <h3>ช.พ.ส.</h3>
                <div style="display:flex; justify-content:space-around;">
                    <p class="stat-value" style="color:#8E24AA;">{data['cps']['total']}</p> 
                    <p class="stat-up">{data['cps']['new']} เพิ่ม</p> 
                    <p class="stat-down">{data['cps']['resign']} จำหน่าย</p>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
        fig = px.bar(x=data['cps']['apply_vals'], y=["สมัคร", "ขอกลับ"], orientation='h', color_discrete_sequence=['#4CAF50'])
        fig.update_layout(height=180, margin=dict(l=0,r=0,t=0,b=0), font_family="Kanit")
        st.plotly_chart(fig, use_container_width=True, key="chart_cps_bar")
    
    st.markdown("### 💳 การนำส่งเงิน & งบการเงิน")
    f1, f2 = st.columns(2)
    
    with f1:
        st.caption(f"แนวโน้มการชำระ ช.พ.ค. ({data['finance']['cpk_paid']})")
        df_trend = pd.DataFrame({'M': range(12), 'V': data['finance']['cpk_trend']})
        fig = px.line(df_trend, x='M', y='V', markers=True)
        fig.update_layout(height=200, margin=dict(t=10,b=10), font_family="Kanit")
        st.plotly_chart(fig, use_container_width=True, key="chart_cpk_trend")
        
    with f2:
        st.caption(f"แนวโน้มการชำระ ช.พ.ส. ({data['finance']['cps_paid']})")
        df_trend = pd.DataFrame({'M': range(12), 'V': data['finance']['cps_trend']})
        fig = px.line(df_trend, x='M', y='V', markers=True)
        fig.update_traces(line_color='#8E24AA')
        fig.update_layout(height=200, margin=dict(t=10,b=10), font_family="Kanit")
        st.plotly_chart(fig, use_container_width=True, key="chart_cps_trend")
