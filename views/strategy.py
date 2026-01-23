import streamlit as st
import pandas as pd
import plotly.express as px
from utils.styles import render_header

def show_view():
    render_header("สำนักนโยบาย และยุทธศาสตร์", border_color="#2196F3")

    # 1. READ DATA
    if 'df_strategy' not in st.session_state or st.session_state['df_strategy'].empty:
        st.warning("⚠️ ไม่พบข้อมูล Strategy_Data (กรุณาอัปโหลดไฟล์ Excel)")
        return

    df = st.session_state['df_strategy'].copy()
    
    # Check Columns
    required_cols = ['Year', 'Category', 'Item', 'SubItem', 'Value', 'Note']
    missing_cols = [c for c in required_cols if c not in df.columns]
    if missing_cols:
        st.error(f"❌ ข้อมูลไม่ถูกต้อง: ไม่พบคอลัมน์ {missing_cols}")
        return

    # --- YEAR COMPARISON FILTER ---
    available_years = sorted(df['Year'].unique(), reverse=True)
    if not available_years: available_years = ["2568"]
    
    col_filter1, col_filter2, col_blank = st.columns([1, 1, 3])
    with col_filter1:
        selected_year = st.selectbox("📅 ปีงบประมาณ (Fiscal Year)", available_years, index=0)
    with col_filter2:
        # Default compare year is the previous year (if exists)
        default_comp_idx = 1 if len(available_years) > 1 else 0
        compare_year = st.selectbox("⚖️ เปรียบเทียบกับ (Compare with)", available_years, index=default_comp_idx)

    # Filter Dataframes
    df_curr = df[df['Year'] == str(selected_year)]
    df_prev = df[df['Year'] == str(compare_year)]

    if df_curr.empty:
        st.warning(f"⚠️ ไม่พบข้อมูลสำหรับปี {selected_year}")
        return

    # Helper function to get comparison value
    def get_delta(cat, item, subitem):
        try:
            val_curr = df_curr[(df_curr['Category']==cat) & (df_curr['Item']==item) & (df_curr['SubItem']==subitem)]['Value'].sum()
            val_prev = df_prev[(df_prev['Category']==cat) & (df_prev['Item']==item) & (df_prev['SubItem']==subitem)]['Value'].sum()
            
            if val_prev == 0: return val_curr, 0
            
            delta_percent = ((val_curr - val_prev) / val_prev) * 100
            return val_curr, delta_percent
        except:
            return 0, 0

    # --- ROW 1: OVERVIEW CARDS ---
    c1, c2, c3 = st.columns(3)

    # 1.1 Revenue
    rev_act, rev_delta = get_delta('Overview', 'Revenue_Total', 'Actual')
    rev_plan = df_curr[(df_curr['Category']=='Overview') & (df_curr['Item']=='Revenue_Total') & (df_curr['SubItem']=='Plan')]['Value'].sum()
    
    with c1:
        st.markdown(f"""
        <div style="background:white; padding:15px; border-radius:10px; border:1px solid #eee; height:140px;">
            <div style="color:#666; font-size:14px;">รายรับรวม</div>
            <div style="color:#4CAF50; font-size:32px; font-weight:bold;">{rev_act:,.2f} <span style="font-size:16px; color:#333;">ล้านบาท</span></div>
            <div style="color:{'#4CAF50' if rev_delta >=0 else '#F44336'}; font-size:12px; margin-top:5px;">
                {'▲' if rev_delta >=0 else '▼'} {abs(rev_delta):.1f}% (เทียบปี {compare_year})
            </div>
            <div style="display:flex; justify-content:space-between; font-size:11px; color:#999; margin-top:15px;">
                <span>แผนปี {selected_year}</span><span>{rev_plan:,.2f} ล้านบาท</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # 1.2 Expense
    exp_act, exp_delta = get_delta('Overview', 'Expense_Total', 'Actual')
    exp_bud = df_curr[(df_curr['Category']=='Overview') & (df_curr['Item']=='Expense_Total') & (df_curr['SubItem']=='Budget')]['Value'].sum()

    with c2:
        st.markdown(f"""
        <div style="background:white; padding:15px; border-radius:10px; border:1px solid #eee; height:140px;">
            <div style="color:#666; font-size:14px;">รายจ่ายรวม</div>
            <div style="color:#E91E63; font-size:32px; font-weight:bold;">{exp_act:,.2f} <span style="font-size:16px; color:#333;">ล้านบาท</span></div>
            <div style="color:{'#F44336' if exp_delta > 0 else '#4CAF50'}; font-size:12px; margin-top:5px;">
                {'▲' if exp_delta >=0 else '▼'} {abs(exp_delta):.1f}% (เทียบปี {compare_year})
            </div>
            <div style="display:flex; justify-content:space-between; font-size:11px; color:#999; margin-top:15px;">
                <span>งบประมาณ</span><span>{exp_bud:,.2f} ล้านบาท</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # 1.3 Net Revenue
    net_act, net_delta = get_delta('Overview', 'Net_Revenue', 'Actual')

    with c3:
        st.markdown(f"""
        <div style="background:white; padding:15px; border-radius:10px; border:1px solid #eee; height:140px;">
            <div style="color:#666; font-size:14px;">รายรับสุทธิ</div>
            <div style="color:#00BCD4; font-size:32px; font-weight:bold;">{net_act:,.2f} <span style="font-size:16px; color:#333;">ล้านบาท</span></div>
            <div style="color:{'#00BCD4' if net_delta >=0 else '#F44336'}; font-size:12px; margin-top:5px;">
                {'▲' if net_delta >=0 else '▼'} {abs(net_delta):.1f}% (เทียบปี {compare_year})
            </div>
            <div style="display:flex; justify-content:space-between; font-size:11px; color:#999; margin-top:15px;">
                <span>สถานะ</span><span>{'กำไร' if net_act > 0 else 'ขาดทุน'}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.write("---")

    # --- ROW 2: BAR CHARTS (Use Data from Selected Year) ---
    c_left, c_right = st.columns(2)

    with c_left:
        st.markdown(f"**📊 รายจ่ายตามยุทธศาสตร์ (ปี {selected_year})**")
        df_chart1 = df_curr[df_curr['Category'] == 'Strategy_Chart']
        if not df_chart1.empty:
            fig = px.bar(df_chart1, x='Item', y='Value', color='SubItem', barmode='group',
                         color_discrete_map={'งบประมาณ': '#ADD8E6', 'เบิกจ่ายจริง': '#4CAF50'})
            fig.update_layout(xaxis_title=None, yaxis_title=None, legend_title=None, height=350, font_family="Kanit")
            st.plotly_chart(fig, use_container_width=True)

    with c_right:
        st.markdown(f"**📊 รายรับตามประเภท (ปี {selected_year})**")
        df_chart2 = df_curr[df_curr['Category'] == 'Revenue_Chart']
        if not df_chart2.empty:
            fig = px.bar(df_chart2, x='Item', y='Value', color='SubItem', barmode='group',
                         color_discrete_map={'แผน': '#ADD8E6', 'ผล': '#4CAF50'})
            fig.update_layout(xaxis_title=None, yaxis_title=None, legend_title=None, height=350, font_family="Kanit")
            st.plotly_chart(fig, use_container_width=True)

    st.write("---")

    # --- ROW 3: KPI STATUS ---
    k1, k2, k3, k4 = st.columns(4)

    # K1: Success Rate (Big Green)
    rate_val = df_curr[(df_curr['Category']=='KPI_Main')]['Value'].sum()
    rate_note = df_curr[(df_curr['Category']=='KPI_Main')]['Note'].iloc[0] if not df_curr[(df_curr['Category']=='KPI_Main')].empty else ""
    
    with k1:
        st.markdown(f"""
        <div style="background:white; padding:20px; border-radius:10px; border:1px solid #eee; text-align:center; height:150px;">
            <div style="font-size:14px; color:#555;">อัตราความสำเร็จเฉลี่ย</div>
            <div style="font-size:38px; font-weight:bold; color:#2E7D32;">{rate_val}%</div>
            <div style="background:#E8F5E9; color:#2E7D32; border-radius:15px; padding:2px 10px; display:inline-block; font-size:12px; margin-top:5px;">
                {rate_note}
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Helper for small cards
    def status_card(col, title, item_name, color):
        val = df_curr[(df_curr['Category']=='KPI_Sub') & (df_curr['Item']==item_name)]['Value'].sum()
        note = df_curr[(df_curr['Category']=='KPI_Sub') & (df_curr['Item']==item_name)]['Note'].iloc[0] if not df_curr[(df_curr['Category']=='KPI_Sub') & (df_curr['Item']==item_name)].empty else ""
        col.markdown(f"""
        <div style="background:white; padding:20px; border-radius:10px; border:1px solid #eee; text-align:center; height:150px;">
            <div style="font-size:14px; color:#555;">{title}</div>
            <div style="font-size:32px; font-weight:bold; color:{color}; margin-top:5px;">{int(val)}</div>
            <div style="font-size:12px; color:#999; margin-top:5px;">{note}</div>
        </div>
        """, unsafe_allow_html=True)

    status_card(k2, "บรรลุเป้าหมาย", "Achieved", "#FF9800")
    status_card(k3, "ใกล้บรรลุ", "Near_Achieved", "#FFC107")
    status_card(k4, "ต้องปรับปรุง", "Improve", "#D32F2F")

    st.write("---")

    # --- ROW 4: RANKING CHARTS ---
    r1, r2 = st.columns(2)

    with r1:
        st.markdown(f"**🏆 Top 5 หน่วยงานผลงานดีเด่น (ปี {selected_year})**")
        df_top = df_curr[df_curr['Category'] == 'Ranking_Top'].sort_values('Value', ascending=True)
        if not df_top.empty:
            fig = px.bar(df_top, x='Value', y='Item', orientation='h', text='Value')
            fig.update_traces(marker_color='#66BB6A', textposition='inside')
            fig.update_layout(xaxis_title=None, yaxis_title=None, height=300, xaxis_range=[0,105], font_family="Kanit")
            st.plotly_chart(fig, use_container_width=True)

    with r2:
        st.markdown(f"**📉 Bottom 5 หน่วยงานต้องปรับปรุง (ปี {selected_year})**")
        df_bot = df_curr[df_curr['Category'] == 'Ranking_Bottom'].sort_values('Value', ascending=True)
        if not df_bot.empty:
            fig = px.bar(df_bot, x='Value', y='Item', orientation='h', text='Value')
            fig.update_traces(marker_color='#FF9800', textposition='inside')
            fig.update_layout(xaxis_title=None, yaxis_title=None, height=300, xaxis_range=[0,105], font_family="Kanit")
            st.plotly_chart(fig, use_container_width=True)
