import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from utils.styles import render_header

def show_view():
    render_header("สำนักนโยบาย และยุทธศาสตร์", border_color="#2196F3")

    if 'df_strategy' not in st.session_state or st.session_state['df_strategy'].empty:
        # Fallback Mock Data
        total_projects = 45
        completed = 38
        success_rate = 91.3
        budget_used = 85.5
    else:
        df = st.session_state['df_strategy']
        total_projects = len(df) if not df.empty else 45
        completed = int(total_projects * 0.85)
        success_rate = 91.3 
        budget_used = 85.5

    # --- ROW 1: KPI CARDS ---
    c1, c2, c3, c4 = st.columns(4)

    # Card 1: Total Projects
    with c1:
        st.markdown(f"""
        <div style="background:white; padding:20px; border-radius:10px; border-left:5px solid #2196F3; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
            <div style="font-size:14px; color:#666;">📝 โครงการทั้งหมด</div>
            <div style="font-size:28px; font-weight:bold; color:#333;">{total_projects} <span style="font-size:16px;">โครงการ</span></div>
            <div style="font-size:12px; color:#888;">ปีงบประมาณ 2568</div>
        </div>
        """, unsafe_allow_html=True)

    # Card 2: Success Rate (REVERTED TO STANDARD STYLE)
    with c2:
        st.markdown(f"""
        <div style="background:white; padding:20px; border-radius:10px; border-left:5px solid #4CAF50; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
            <div style="font-size:14px; color:#666;">อัตราความสำเร็จเฉลี่ย</div>
            <div style="font-size:28px; font-weight:bold; color:#333;">{success_rate}%</div>
            <div style="font-size:12px; color:#888;">23 ตัวชี้วัด</div>
        </div>
        """, unsafe_allow_html=True)

    # Card 3: Completed
    with c3:
        st.markdown(f"""
        <div style="background:white; padding:20px; border-radius:10px; border-left:5px solid #FF9800; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
            <div style="font-size:14px; color:#666;">✅ ดำเนินการแล้วเสร็จ</div>
            <div style="font-size:28px; font-weight:bold; color:#333;">{completed} <span style="font-size:16px;">โครงการ</span></div>
            <div style="font-size:12px; color:#888;">คิดเป็น {completed/total_projects*100:.1f}%</div>
        </div>
        """, unsafe_allow_html=True)

    # Card 4: Budget
    with c4:
        st.markdown(f"""
        <div style="background:white; padding:20px; border-radius:10px; border-left:5px solid #9C27B0; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
            <div style="font-size:14px; color:#666;">💰 เบิกจ่ายงบประมาณ</div>
            <div style="font-size:28px; font-weight:bold; color:#333;">{budget_used}%</div>
            <div style="font-size:12px; color:#888;">ตามเป้าหมาย</div>
        </div>
        """, unsafe_allow_html=True)

    st.write("---")

    # --- ROW 2: CHARTS ---
    col1, col2 = st.columns([2, 1])

    with col1:
        st.subheader("📊 ความคืบหน้าโครงการรายเดือน")
        # Mock Trend Data
        months = ["ต.ค.", "พ.ย.", "ธ.ค.", "ม.ค.", "ก.พ.", "มี.ค."]
        progress = [15, 30, 45, 60, 75, 82]
        
        fig = px.bar(x=months, y=progress, text=progress, labels={'x':'เดือน', 'y':'ความคืบหน้า (%)'})
        fig.update_traces(marker_color='#2196F3', textposition='outside')
        fig.update_layout(height=350, margin=dict(l=20, r=20, t=20, b=20))
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("🎯 สถานะตัวชี้วัด")
        labels = ['บรรลุเป้าหมาย', 'กำลังดำเนินการ', 'ล่าช้า']
        values = [65, 25, 10]
        colors = ['#4CAF50', '#FFC107', '#F44336']
        
        fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.5, marker_colors=colors)])
        fig.update_layout(height=350, margin=dict(l=20, r=20, t=20, b=20), showlegend=True, legend=dict(orientation="h", y=-0.1))
        st.plotly_chart(fig, use_container_width=True)
