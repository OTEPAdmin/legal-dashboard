import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from utils.styles import render_header

def show_view():
    render_header("📈 กลุ่มนโยบายและยุทธศาสตร์ (Policy & Strategy)", border_color="#4CAF50")
    
    if 'df_strategy' not in st.session_state or st.session_state['df_strategy'].empty:
        st.error("⚠️ ไม่พบข้อมูล Strategy_Data ใน Excel")
        return

    df = st.session_state['df_strategy'].copy()
    
    # --- DATA CLEANING (Fixes "No Data" issues) ---
    # 1. Strip whitespace from Category names (e.g., "Unit_Perf " -> "Unit_Perf")
    df['Category'] = df['Category'].astype(str).str.strip()
    
    # 2. Ensure Unit_Score is numeric for sorting
    if 'Unit_Score' in df.columns:
        df['Unit_Score'] = pd.to_numeric(df['Unit_Score'], errors='coerce').fillna(0)
    
    # --- COMPARISON FILTER ---
    available_years = sorted(df['Year'].unique(), reverse=True)
    if not available_years: available_years = ["2568"]
    
    idx_main = 0
    idx_comp = 1 if len(available_years) > 1 else 0

    c1, c2, c3 = st.columns([1, 1, 4])
    with c1: 
        year_main = st.selectbox("ปีงบประมาณ (Current)", available_years, index=idx_main)
    with c2: 
        year_comp = st.selectbox("เปรียบเทียบกับ (Previous)", available_years, index=idx_comp)
    
    # Filter Data
    df_curr = df[df['Year'] == str(year_main)]
    df_prev = df[df['Year'] == str(year_comp)]
    
    st.write("---")
    st.markdown(f"##### 💰 รายรับ - รายจ่าย สกสค. ปีงบประมาณ {year_main}")

    # --- 1. TOP CARDS ---
    def get_fin_data(dframe):
        rev = dframe[dframe['Category'] == 'Revenue_Total']['Actual_Amount'].sum()
        rev_plan = dframe[dframe['Category'] == 'Revenue_Total']['Plan_Amount'].sum()
        exp = dframe[dframe['Category'] == 'Expense_Total']['Actual_Amount'].sum()
        exp_plan = dframe[dframe['Category'] == 'Expense_Total']['Plan_Amount'].sum()
        return rev, rev_plan, exp, exp_plan

    cur_rev, cur_rev_plan, cur_exp, cur_exp_plan = get_fin_data(df_curr)
    prev_rev, _, _, _ = get_fin_data(df_prev)

    cur_net = cur_rev - cur_exp
    prev_net = prev_rev - (df_prev[df_prev['Category'] == 'Expense_Total']['Actual_Amount'].sum())

    rev_pct = (cur_rev / cur_rev_plan * 100) if cur_rev_plan > 0 else 0
    exp_pct = (cur_exp / cur_exp_plan * 100) if cur_exp_plan > 0 else 0
    net_growth = ((cur_net - prev_net) / prev_net * 100) if prev_net > 0 else 0

    c1, c2, c3 = st.columns(3)

    # Card 1
    with c1:
        st.markdown(f"""
        <div style="background:white; padding:15px; border-radius:10px; border: 1px solid #ddd; box-shadow: 0 2px 5px rgba(0,0,0,0.05);">
            <div style="color:#555; font-size:14px; font-weight:bold;">รายรับรวม</div>
            <div style="font-size:36px; font-weight:bold; color:#4CAF50;">{cur_rev:,.2f} <span style="font-size:16px; color:#333;">ล้านบาท</span></div>
            <div style="color:#FFC107; font-size:13px; margin-bottom:10px;">▲ {rev_pct:.1f}% ของแผน</div>
            <div style="display:flex; justify-content:space-between; font-size:12px; color:#777; border-top:1px solid #eee; padding-top:5px;">
                <span>แผน</span> <span>{cur_rev_plan:,.2f} ล้านบาท</span>
            </div>
             <div style="display:flex; justify-content:space-between; font-size:12px; color:#4CAF50;">
                <span>ผล</span> <span>{cur_rev:,.2f} ล้านบาท</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Card 2
    with c2:
        st.markdown(f"""
        <div style="background:white; padding:15px; border-radius:10px; border: 1px solid #ddd; box-shadow: 0 2px 5px rgba(0,0,0,0.05);">
            <div style="color:#555; font-size:14px; font-weight:bold;">รายจ่ายรวม</div>
            <div style="font-size:36px; font-weight:bold; color:#F44336;">{cur_exp:,.2f} <span style="font-size:16px; color:#333;">ล้านบาท</span></div>
            <div style="color:#FFC107; font-size:13px; margin-bottom:10px;">{exp_pct:.1f}% ของงบประมาณ</div>
            <div style="display:flex; justify-content:space-between; font-size:12px; color:#777; border-top:1px solid #eee; padding-top:5px;">
                <span>งบประมาณ</span> <span>{cur_exp_plan:,.2f} ล้านบาท</span>
            </div>
             <div style="display:flex; justify-content:space-between; font-size:12px; color:#F44336;">
                <span>เบิกจ่าย</span> <span>{cur_exp:,.2f} ล้านบาท</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Card 3
    with c3:
        color = "#008CBA" if net_growth >= 0 else "#F44336"
        arrow = "▲" if net_growth >= 0 else "▼"
        st.markdown(f"""
        <div style="background:white; padding:15px; border-radius:10px; border: 1px solid #ddd; box-shadow: 0 2px 5px rgba(0,0,0,0.05);">
            <div style="color:#555; font-size:14px; font-weight:bold;">รายรับสุทธิ</div>
            <div style="font-size:36px; font-weight:bold; color:#008CBA;">{cur_net:,.2f} <span style="font-size:16px; color:#333;">ล้านบาท</span></div>
            <div style="color:{color}; font-size:13px; margin-bottom:10px;">{arrow} {net_growth:.1f}% จากปีก่อน</div>
            <div style="display:flex; justify-content:space-between; font-size:12px; color:#777; border-top:1px solid #eee; padding-top:5px;">
                <span>ปี {year_comp}</span> <span>{prev_net:,.2f} ล้านบาท</span>
            </div>
             <div style="display:flex; justify-content:space-between; font-size:12px; color:#008CBA;">
                <span>ปี {year_main}</span> <span>{cur_net:,.2f} ล้านบาท</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.write("---")

    # --- 2. MIDDLE CHARTS ---
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("##### 📊 รายจ่ายตามยุทธศาสตร์ (ล้านบาท)")
        df_strat = df_curr[df_curr['Category'] == 'Strategy'].copy()
        if not df_strat.empty:
            fig = go.Figure()
            fig.add_trace(go.Bar(name='งบประมาณ', x=df_strat['Item'], y=df_strat['Plan_Amount'], marker_color='#B2EBF2'))
            fig.add_trace(go.Bar(name='เบิกจ่ายจริง', x=df_strat['Item'], y=df_strat['Actual_Amount'], marker_color='#4CAF50'))
            fig.update_layout(barmode='group', height=350, margin=dict(l=0,r=0,t=20,b=0), font_family="Kanit", legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
            st.plotly_chart(fig, use_container_width=True, key="strat_exp_chart")
        else:
            st.info("ไม่มีข้อมูลยุทธศาสตร์")

    with c2:
        st.markdown("##### 📊 รายรับตามประเภท (ล้านบาท)")
        df_src = df_curr[df_curr['Category'] == 'Rev_Source'].copy()
        if not df_src.empty:
            fig = go.Figure()
            fig.add_trace(go.Bar(name='แผน', x=df_src['Item'], y=df_src['Plan_Amount'], marker_color='#B2EBF2'))
            fig.add_trace(go.Bar(name='ผล', x=df_src['Item'], y=df_src['Actual_Amount'], marker_color='#4CAF50'))
            fig.update_layout(barmode='group', height=350, margin=dict(l=0,r=0,t=20,b=0), font_family="Kanit", legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
            st.plotly_chart(fig, use_container_width=True, key="strat_rev_chart")
        else:
            st.info("ไม่มีข้อมูลประเภทรายรับ")

    st.write("---")

    # --- 3. KPI CARDS ---
    k1, k2, k3, k4 = st.columns(4)
    with k1: st.metric("อัตราความสำเร็จเฉลี่ย", "91.3%", "23 ตัวชี้วัด")
    with k2: st.markdown(f"""<div style="text-align:center; padding:10px; border:1px solid #eee; border-radius:10px;"><div style="font-size:12px; color:#555;">บรรลุเป้าหมาย</div><div style="font-size:32px; font-weight:bold; color:#FF9800;">17</div><div style="font-size:10px; color:#aaa;">≥ 70%</div></div>""", unsafe_allow_html=True)
    with k3: st.markdown(f"""<div style="text-align:center; padding:10px; border:1px solid #eee; border-radius:10px;"><div style="font-size:12px; color:#555;">ใกล้บรรลุ</div><div style="font-size:32px; font-weight:bold; color:#FFC107;">4</div><div style="font-size:10px; color:#aaa;">80-99%</div></div>""", unsafe_allow_html=True)
    with k4: st.markdown(f"""<div style="text-align:center; padding:10px; border:1px solid #eee; border-radius:10px;"><div style="font-size:12px; color:#555;">ต้องปรับปรุง</div><div style="font-size:32px; font-weight:bold; color:#F44336;">2</div><div style="font-size:10px; color:#aaa;"> < 80%</div></div>""", unsafe_allow_html=True)

    st.write("---")

    # --- 4. RANKING CHARTS (FIXED) ---
    c1, c2 = st.columns(2)
    
    # Filter for Unit Performance (and strip spaces again just in case)
    df_perf = df_curr[df_curr['Category'] == 'Unit_Perf'].copy()
    
    if not df_perf.empty:
        # Sort by numeric score
        top_5 = df_perf.sort_values('Unit_Score', ascending=False).head(5)
        bot_5 = df_perf.sort_values('Unit_Score', ascending=True).head(5)

        with c1:
            st.markdown("##### 🏆 Top 5 หน่วยงานผลงานดีเด่น")
            fig = px.bar(top_5, x='Unit_Score', y='Item', orientation='h', text='Unit_Score')
            fig.update_traces(marker_color='#4CAF50', textposition='inside')
            fig.update_layout(height=300, margin=dict(l=0,r=0,t=10,b=0), font_family="Kanit", 
                              yaxis={'categoryorder':'total ascending'}, xaxis_title=None, yaxis_title=None, xaxis_range=[0,105])
            st.plotly_chart(fig, use_container_width=True, key="top5_chart")

        with c2:
            st.markdown("##### 📉 Bottom 5 หน่วยงานต้องปรับปรุง")
            fig = px.bar(bot_5, x='Unit_Score', y='Item', orientation='h', text='Unit_Score')
            fig.update_traces(marker_color='#FF9800', textposition='inside')
            fig.update_layout(height=300, margin=dict(l=0,r=0,t=10,b=0), font_family="Kanit", 
                              yaxis={'categoryorder':'total descending'}, xaxis_title=None, yaxis_title=None, xaxis_range=[0,105])
            st.plotly_chart(fig, use_container_width=True, key="bot5_chart")
    else:
        st.info(f"ไม่มีข้อมูลผลการปฏิบัติงานหน่วยงาน ของปี {year_main} (กรุณาตรวจสอบข้อมูลใน Excel tab: Strategy_Data)")
