import streamlit as st
import pandas as pd
import plotly.express as px
from utils.styles import render_header

def show_view():
    render_header("สำนักนโยบาย และยุทธศาสตร์", border_color="#2196F3")

    # 1. READ DATA
    if 'df_strategy' not in st.session_state or st.session_state['df_strategy'].empty:
        st.warning("⚠️ กรุณาอัปโหลดไฟล์ Excel ที่มี Tab: 'Strategy_Data'")
        return

    df = st.session_state['df_strategy'].copy()

    # --- CRITICAL FIX: Check if columns exist ---
    required_cols = ['Year', 'Category', 'Item', 'SubItem', 'Value', 'Note']
    missing_cols = [c for c in required_cols if c not in df.columns]
    
    if missing_cols:
        st.error(f"❌ ข้อมูลไม่ถูกต้อง: ไม่พบคอลัมน์ {missing_cols} ใน Tab 'Strategy_Data'")
        st.info("💡 กรุณาตรวจสอบไฟล์ Excel ว่าหัวตาราง (Row 1) เขียนถูกต้อง: Year, Category, Item, SubItem, Value, Note")
        return
    # --------------------------------------------
    
    # Filter for 2568 (Current Year View)
    df = df[df['Year'] == '2568']

    if df.empty:
        st.warning("⚠️ ไม่พบข้อมูลสำหรับปี 2568")
        return

    # --- ROW 1: OVERVIEW CARDS ---
    c1, c2, c3 = st.columns(3)

    # 1.1 Revenue
    # Use .get() or check empty to prevent errors if specific rows are missing
    try:
        rev_act_row = df[(df['Category']=='Overview') & (df['Item']=='Revenue_Total') & (df['SubItem']=='Actual')]
        rev_plan_row = df[(df['Category']=='Overview') & (df['Item']=='Revenue_Total') & (df['SubItem']=='Plan')]
        
        rev_act = rev_act_row['Value'].sum() if not rev_act_row.empty else 0
        rev_plan = rev_plan_row['Value'].sum() if not rev_plan_row.empty else 0
        rev_note = rev_act_row['Note'].iloc[0] if not rev_act_row.empty else "-"

        with c1:
            st.markdown(f"""
            <div style="background:white; padding:15px; border-radius:10px; border:1px solid #eee; height:140px;">
                <div style="color:#666; font-size:14px;">รายรับรวม</div>
                <div style="color:#4CAF50; font-size:32px; font-weight:bold;">{rev_act:,.2f} <span style="font-size:16px; color:#333;">ล้านบาท</span></div>
                <div style="color:#FF9800; font-size:12px; margin-top:5px;">▲ {rev_note}</div>
                <div style="display:flex; justify-content:space-between; font-size:11px; color:#999; margin-top:15px;">
                    <span>แผน</span><span>{rev_plan:,.2f} ล้านบาท</span>
                </div>
                 <div style="display:flex; justify-content:space-between; font-size:11px; color:#4CAF50;">
                    <span>ผล</span><span>{rev_act:,.2f} ล้านบาท</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
    except Exception as e:
        c1.error(f"Error loading Revenue: {e}")

    # 1.2 Expense
    try:
        exp_act_row = df[(df['Category']=='Overview') & (df['Item']=='Expense_Total') & (df['SubItem']=='Actual')]
        exp_bud_row = df[(df['Category']=='Overview') & (df['Item']=='Expense_Total') & (df['SubItem']=='Budget')]
        
        exp_act = exp_act_row['Value'].sum() if not exp_act_row.empty else 0
        exp_bud = exp_bud_row['Value'].sum() if not exp_bud_row.empty else 0
        exp_note = exp_act_row['Note'].iloc[0] if not exp_act_row.empty else "-"

        with c2:
            st.markdown(f"""
            <div style="background:white; padding:15px; border-radius:10px; border:1px solid #eee; height:140px;">
                <div style="color:#666; font-size:14px;">รายจ่ายรวม</div>
                <div style="color:#E91E63; font-size:32px; font-weight:bold;">{exp_act:,.2f} <span style="font-size:16px; color:#333;">ล้านบาท</span></div>
                <div style="color:#FFC107; font-size:12px; margin-top:5px;">{exp_note}</div>
                <div style="display:flex; justify-content:space-between; font-size:11px; color:#999; margin-top:15px;">
                    <span>งบประมาณ</span><span>{exp_bud:,.2f} ล้านบาท</span>
                </div>
                 <div style="display:flex; justify-content:space-between; font-size:11px; color:#E91E63;">
                    <span>เบิกจ่าย</span><span>{exp_act:,.2f} ล้านบาท</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
    except:
        c2.error("Error loading Expense")

    # 1.3 Net Revenue
    try:
        net_act_row = df[(df['Category']=='Overview') & (df['Item']=='Net_Revenue') & (df['SubItem']=='Actual')]
        net_last_row = df[(df['Category']=='Overview') & (df['Item']=='Net_Revenue') & (df['SubItem']=='LastYear')]
        
        net_act = net_act_row['Value'].sum() if not net_act_row.empty else 0
        net_last = net_last_row['Value'].sum() if not net_last_row.empty else 0
        net_note = net_act_row['Note'].iloc[0] if not net_act_row.empty else "-"

        with c3:
            st.markdown(f"""
            <div style="background:white; padding:15px; border-radius:10px; border:1px solid #eee; height:140px;">
                <div style="color:#666; font-size:14px;">รายรับสุทธิ</div>
                <div style="color:#00BCD4; font-size:32px; font-weight:bold;">{net_act:,.2f} <span style="font-size:16px; color:#333;">ล้านบาท</span></div>
                <div style="color:#009688; font-size:12px; margin-top:5px;">▲ {net_note}</div>
                <div style="display:flex; justify-content:space-between; font-size:11px; color:#999; margin-top:15px;">
                    <span>ปี 2567</span><span>{net_last:,.2f} ล้านบาท</span>
                </div>
                 <div style="display:flex; justify-content:space-between; font-size:11px; color:#00BCD4;">
                    <span>ปี 2568</span><span>{net_act:,.2f} ล้านบาท</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
    except:
        c3.error("Error loading Net Revenue")

    st.write("---")

    # --- ROW 2: BAR CHARTS ---
    c_left, c_right = st.columns(2)

    with c_left:
        st.markdown("**📊 รายจ่ายตามยุทธศาสตร์ (ล้านบาท)**")
        df_chart1 = df[df['Category'] == 'Strategy_Chart']
        if not df_chart1.empty:
            fig = px.bar(df_chart1, x='Item', y='Value', color='SubItem', barmode='group',
                         color_discrete_map={'งบประมาณ': '#ADD8E6', 'เบิกจ่ายจริง': '#4CAF50'})
            fig.update_layout(xaxis_title=None, yaxis_title=None, legend_title=None, height=350, font_family="Kanit")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("ไม่มีข้อมูลกราฟรายจ่าย")

    with c_right:
        st.markdown("**📊 รายรับตามประเภท (ล้านบาท)**")
        df_chart2 = df[df['Category'] == 'Revenue_Chart']
        if not df_chart2.empty:
            fig = px.bar(df_chart2, x='Item', y='Value', color='SubItem', barmode='group',
                         color_discrete_map={'แผน': '#ADD8E6', 'ผล': '#4CAF50'})
            fig.update_layout(xaxis_title=None, yaxis_title=None, legend_title=None, height=350, font_family="Kanit")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("ไม่มีข้อมูลกราฟรายรับ")

    st.write("---")

    # --- ROW 3: KPI STATUS ---
    k1, k2, k3, k4 = st.columns(4)

    # K1: Success Rate (Big Green)
    try:
        rate_row = df[(df['Category']=='KPI_Main')]
        rate_val = rate_row['Value'].sum() if not rate_row.empty else 0
        rate_note = rate_row['Note'].iloc[0] if not rate_row.empty else "-"
        
        with k1:
            st.markdown(f"""
            <div style="background:white; padding:20px; border-radius:10px; border:1px solid #eee; text-align:center; height:150px;">
                <div style="font-size:14px; color:#555;">อัตราความสำเร็จเฉลี่ย</div>
                <div style="font-size:38px; font-weight:bold; color:#2E7D32;">{rate_val}%</div>
                <div style="background:#E8F5E9; color:#2E7D32; border-radius:15px; padding:2px 10px; display:inline-block; font-size:12px; margin-top:5px;">
                    ↑ {rate_note}
                </div>
            </div>
            """, unsafe_allow_html=True)
    except:
        k1.error("Error KPI")

    # Helper for small cards
    def status_card(col, title, item_name, color):
        try:
            row = df[(df['Category']=='KPI_Sub') & (df['Item']==item_name)]
            val = row['Value'].sum() if not row.empty else 0
            note = row['Note'].iloc[0] if not row.empty else "-"
            col.markdown(f"""
            <div style="background:white; padding:20px; border-radius:10px; border:1px solid #eee; text-align:center; height:150px;">
                <div style="font-size:14px; color:#555;">{title}</div>
                <div style="font-size:32px; font-weight:bold; color:{color}; margin-top:5px;">{int(val)}</div>
                <div style="font-size:12px; color:#999; margin-top:5px;">{note}</div>
            </div>
            """, unsafe_allow_html=True)
        except:
            col.error("Error")

    status_card(k2, "บรรลุเป้าหมาย", "Achieved", "#FF9800")
    status_card(k3, "ใกล้บรรลุ", "Near_Achieved", "#FFC107")
    status_card(k4, "ต้องปรับปรุง", "Improve", "#D32F2F")

    st.write("---")

    # --- ROW 4: RANKING CHARTS ---
    r1, r2 = st.columns(2)

    with r1:
        st.markdown("**🏆 Top 5 หน่วยงานผลงานดีเด่น**")
        df_top = df[df['Category'] == 'Ranking_Top'].sort_values('Value', ascending=True)
        if not df_top.empty:
            fig = px.bar(df_top, x='Value', y='Item', orientation='h', text='Value')
            fig.update_traces(marker_color='#66BB6A', textposition='inside')
            fig.update_layout(xaxis_title=None, yaxis_title=None, height=300, xaxis_range=[0,105], font_family="Kanit")
            st.plotly_chart(fig, use_container_width=True)

    with r2:
        st.markdown("**📉 Bottom 5 หน่วยงานต้องปรับปรุง**")
        df_bot = df[df['Category'] == 'Ranking_Bottom'].sort_values('Value', ascending=True)
        if not df_bot.empty:
            fig = px.bar(df_bot, x='Value', y='Item', orientation='h', text='Value')
            fig.update_traces(marker_color='#FF9800', textposition='inside')
            fig.update_layout(xaxis_title=None, yaxis_title=None, height=300, xaxis_range=[0,105], font_family="Kanit")
            st.plotly_chart(fig, use_container_width=True)
