import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from utils.styles import render_header

def show_view():
    render_header("📊 สำนักตรวจสอบภายใน (Internal Audit Office)", border_color="#2C3E50")
    
    # Check data
    if 'df_audit' not in st.session_state or st.session_state['df_audit'].empty:
        st.error("⚠️ ไม่พบข้อมูล Audit_Data ใน Excel (Please add 'Audit_Data' tab to your file)")
        return

    df = st.session_state['df_audit']

    # Filter by Year (Simple filter for now, matching the fiscal year view)
    years = sorted(df['Year'].unique(), reverse=True)
    c1, c2 = st.columns([1, 4])
    with c1:
        sel_year = st.selectbox("เลือกปีงบประมาณ", years, index=0)

    # Filter Data
    df_yr = df[df['Year'] == sel_year]
    
    # Calculate Totals
    total_plan = df_yr['Plan_Count'].sum()
    total_actual = df_yr['Actual_Count'].sum()
    total_issues = df_yr['Issues_Found'].sum()
    
    # Breakdown totals for sub-labels
    prov_plan = df_yr['Province_Plan'].sum()
    unit_plan = df_yr['Unit_Plan'].sum()
    prov_act = df_yr['Province_Actual'].sum()
    unit_act = df_yr['Unit_Actual'].sum()
    
    # Action Status
    act_done = df_yr['Action_Complete'].sum()
    act_pending = df_yr['Action_Pending'].sum()
    act_not_start = df_yr['Action_NotStarted'].sum()
    total_actions = act_done + act_pending + act_not_start
    percent_done = (act_done / total_actions * 100) if total_actions > 0 else 0

    st.markdown("### 📊 สรุปภาพรวม")

    # --- ROW 1: COLORED CARDS ---
    c1, c2, c3, c4 = st.columns(4)

    # Card 1: Blue (Plan)
    with c1:
        st.markdown(f"""
        <div style="background-color:#203354; padding:15px; border-radius:8px; color:white; height:140px;">
            <div style="font-size:14px; opacity:0.8;">🗂️ แผนการตรวจสอบ</div>
            <div style="font-size:40px; font-weight:bold; margin-top:5px;">{total_plan} <span style="font-size:16px;">แห่ง</span></div>
            <div style="margin-top:10px; font-size:12px; opacity:0.8;">
                จังหวัด {prov_plan} | สำนัก {unit_plan}
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Card 2: Green (Result)
    with c2:
        st.markdown(f"""
        <div style="background-color:#28a745; padding:15px; border-radius:8px; color:white; height:140px;">
            <div style="font-size:14px; opacity:0.8;">✅ ผลการตรวจสอบ</div>
            <div style="font-size:40px; font-weight:bold; margin-top:5px;">{total_actual} <span style="font-size:16px;">แห่ง</span></div>
             <div style="margin-top:10px; font-size:12px; opacity:0.8;">
                จังหวัด {prov_act} | สำนัก {unit_act}
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Card 3: Yellow (Issues) - Black text for contrast
    with c3:
        st.markdown(f"""
        <div style="background-color:#ffc107; padding:15px; border-radius:8px; color:#333; height:140px;">
            <div style="font-size:14px; font-weight:bold;">📝 ประเด็นที่พบ</div>
            <div style="font-size:40px; font-weight:bold; margin-top:5px;">{total_issues} <span style="font-size:16px;">รายการ</span></div>
             <div style="margin-top:10px; font-size:12px;">
                จาก {total_actual} แห่ง
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Card 4: Cyan (Action)
    with c4:
        st.markdown(f"""
        <div style="background-color:#17a2b8; padding:15px; border-radius:8px; color:white; height:140px;">
            <div style="font-size:14px; opacity:0.8;">📈 การดำเนินการตามข้อเสนอแนะ</div>
            <div style="font-size:40px; font-weight:bold; margin-top:5px;">{percent_done:.1f}%</div>
             <div style="margin-top:10px; font-size:12px;">
                เสร็จสิ้น {act_done}/{total_actions} <br>
                <span style="color:#ffc107;">●</span> {act_pending} &nbsp; <span style="color:#dc3545;">●</span> {act_not_start}
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.write("---")
    
    # --- ROW 2: CHART ---
    st.markdown(f"##### 📊 แผน VS ผลการตรวจสอบ รายไตรมาส (ปีงบประมาณ {sel_year})")
    
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=df_yr['Quarter'],
        y=df_yr['Plan_Count'],
        name='แผน',
        marker_color='#5C8DFC',
        text=df_yr['Plan_Count'],
        textposition='auto'
    ))
    fig.add_trace(go.Bar(
        x=df_yr['Quarter'],
        y=df_yr['Actual_Count'],
        name='ผลการตรวจสอบ',
        marker_color='#4CAF50',
        text=df_yr['Actual_Count'],
        textposition='auto'
    ))

    fig.update_layout(
        barmode='group',
        height=350,
        font_family="Kanit",
        margin=dict(l=20, r=20, t=20, b=20),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    st.plotly_chart(fig, use_container_width=True, key="audit_chart")

    st.write("---")
    
    # --- ROW 3: ACTION STATUS CARDS ---
    st.markdown("##### 📋 สรุปสถานะการดำเนินการตามข้อเสนอแนะ")
    
    ac1, ac2, ac3 = st.columns(3)
    
    # Helper for bottom cards
    def status_card(count, label, percent, color, bg_color="#f8f9fa"):
        st.markdown(f"""
        <div style="background-color:{bg_color}; border-left: 5px solid {color}; padding:15px; border-radius:5px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); text-align:center;">
            <div style="font-size:36px; font-weight:bold; color:{color};">{count}</div>
            <div style="font-size:14px; color:#555; margin-top:5px;">{label}</div>
            <div style="font-size:12px; color:#888;">({percent:.1f}%)</div>
        </div>
        """, unsafe_allow_html=True)

    with ac1:
        status_card(act_done, "ดำเนินการเสร็จสิ้น", (act_done/total_actions*100) if total_actions else 0, "#28a745", "#e8f5e9")
    with ac2:
        status_card(act_pending, "อยู่ระหว่างดำเนินการ", (act_pending/total_actions*100) if total_actions else 0, "#ffc107", "#fff3cd")
    with ac3:
        status_card(act_not_start, "ยังไม่ดำเนินการ", (act_not_start/total_actions*100) if total_actions else 0, "#dc3545", "#f8d7da")
