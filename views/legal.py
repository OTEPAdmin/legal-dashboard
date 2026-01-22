import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from utils.styles import render_header

def show_view():
    render_header("⚖️ สำนักนิติการ (Legal Affairs Office)", border_color="#8E24AA")
    
    if 'df_legal' not in st.session_state or st.session_state['df_legal'].empty:
        st.error("⚠️ ไม่พบข้อมูล Legal_Data ใน Excel (Please add 'Legal_Data' tab)")
        return

    df = st.session_state['df_legal']
    
    # --- DYNAMIC YEARS ---
    df['Year'] = df['Year'].astype(str)
    available_years = sorted(df['Year'].unique(), reverse=True)
    if not available_years: available_years = ["2568"]

    months = ["มกราคม", "กุมภาพันธ์", "มีนาคม", "เมษายน", "พฤษภาคม", "มิถุนายน", 
              "กรกฎาคม", "สิงหาคม", "กันยายน", "ตุลาคม", "พฤศจิกายน", "ธันวาคม"]

    # --- FILTER UI ---
    c1, c2, c3, c4, c5 = st.columns([1,1,1,1,1])
    with c1: m_start = st.selectbox("เดือนเริ่มต้น", months, index=0)
    with c2: y_start = st.selectbox("ปีเริ่มต้น", available_years, index=0)
    with c3: m_end = st.selectbox("ถึงเดือน", months, index=11)
    with c4: y_end = st.selectbox("ถึงปี", available_years, index=0)
    with c5: 
        st.write("") 
        st.write("") 
        if st.button("🔍 กรองข้อมูล", use_container_width=True):
            st.rerun()

    # --- FILTER LOGIC ---
    # For this view, we will just use the "End Year" to keep it simple, 
    # or you can implement complex date range logic if needed.
    # Here we filter by the selected 'y_end' year for the overview.
    df_yr = df[df['Year'] == str(y_end)]
    
    # Calculate Totals
    pending_total = df_yr['Pending'].sum()
    completed_total = df_yr['Completed'].sum()
    total_cases = pending_total + completed_total
    damages = df_yr['Damages_Million'].sum()

    st.markdown("### ภาพรวม")

    # --- ROW 1: KPI CARDS ---
    c1, c2, c3, c4 = st.columns(4)

    # Card 1: Total (Purple)
    with c1:
        st.markdown(f"""
        <div style="background:white; padding:15px; border-radius:10px; border-top: 5px solid #9C27B0; box-shadow: 0 2px 5px rgba(0,0,0,0.1);">
            <div style="font-size:36px; font-weight:bold; color:#9C27B0;">{total_cases} <span style="font-size:20px; color:#333;">เรื่อง</span></div>
            <div style="color:#777;">📋 ทั้งหมด</div>
        </div>
        """, unsafe_allow_html=True)

    # Card 2: Pending (Brown/Orange)
    with c2:
        st.markdown(f"""
        <div style="background:white; padding:15px; border-radius:10px; border-top: 5px solid #8D6E63; box-shadow: 0 2px 5px rgba(0,0,0,0.1);">
            <div style="font-size:36px; font-weight:bold; color:#03A9F4;">{pending_total} <span style="font-size:20px; color:#333;">เรื่อง</span></div>
            <div style="color:#777;">⏳ อยู่ระหว่างดำเนินการ</div>
        </div>
        """, unsafe_allow_html=True)

    # Card 3: Completed (Green)
    with c3:
        st.markdown(f"""
        <div style="background:white; padding:15px; border-radius:10px; border-top: 5px solid #4CAF50; box-shadow: 0 2px 5px rgba(0,0,0,0.1);">
            <div style="font-size:36px; font-weight:bold; color:#4CAF50;">{completed_total} <span style="font-size:20px; color:#333;">เรื่อง</span></div>
            <div style="color:#777;">✅ ดำเนินการเสร็จสิ้น</div>
        </div>
        """, unsafe_allow_html=True)

    # Card 4: Damages (Red)
    with c4:
        st.markdown(f"""
        <div style="background:white; padding:15px; border-radius:10px; border-top: 5px solid #F44336; box-shadow: 0 2px 5px rgba(0,0,0,0.1);">
            <div style="font-size:36px; font-weight:bold; color:#F44336;">{damages:.2f} <span style="font-size:20px; color:#333;">ล้านบาท</span></div>
            <div style="color:#777;">💰 มูลค่าความเสียหาย</div>
        </div>
        """, unsafe_allow_html=True)

    st.write("---")
    
    # --- ROW 2: CHARTS ---
    st.markdown("##### ภาระงานตามกลุ่ม แยกตาม 5 กลุ่มงาน")
    
    gc1, gc2 = st.columns([2, 1])

    # Aggregate Data by Group
    group_data = df_yr.groupby("Group")[['Pending', 'Completed']].sum().reset_index()
    # Calculate Completion Rate
    group_data['Total'] = group_data['Pending'] + group_data['Completed']
    group_data['Rate'] = (group_data['Completed'] / group_data['Total'] * 100).fillna(0)

    # Left Chart: Stacked Bar (Workload)
    with gc1:
        st.markdown("###### 📊 ภาระงานตามกลุ่ม (แยกสถานะ)")
        fig = go.Figure()
        fig.add_trace(go.Bar(
            y=group_data['Group'], x=group_data['Pending'], name='อยู่ระหว่างดำเนินการ',
            orientation='h', marker_color='#29B6F6'
        ))
        fig.add_trace(go.Bar(
            y=group_data['Group'], x=group_data['Completed'], name='ดำเนินการเสร็จสิ้น',
            orientation='h', marker_color='#66BB6A'
        ))
        fig.update_layout(barmode='stack', height=350, margin=dict(l=0,r=0,t=0,b=0), font_family="Kanit")
        st.plotly_chart(fig, use_container_width=True, key="legal_stack_chart")

    # Right Chart: Rate (Completion %)
    with gc2:
        st.markdown("###### 📈 อัตราการดำเนินการเสร็จสิ้น")
        
        # Color mapping for groups to match image
        colors = ['#29B6F6', '#66BB6A', '#FFCA28', '#EF6C00', '#AB47BC'] # Blue, Green, Yellow, Orange, Purple
        
        fig = px.bar(group_data, x='Rate', y='Group', orientation='h', text_auto='.1f')
        fig.update_traces(marker_color=colors[:len(group_data)], textposition='inside')
        fig.update_layout(height=350, margin=dict(l=0,r=0,t=0,b=0), xaxis_range=[0,100], font_family="Kanit")
        fig.update_xaxes(title="เปอร์เซ็นต์ความสำเร็จ")
        fig.update_yaxes(title=None, showticklabels=False) # Hide y labels as they duplicate left chart
        st.plotly_chart(fig, use_container_width=True, key="legal_rate_chart")
