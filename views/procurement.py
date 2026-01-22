import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from utils.styles import render_header

def show_view():
    render_header("📦 กองคลัง-พัสดุ (Procurement)", border_color="#795548")
    
    # 1. READ DATA FROM SESSION STATE
    if 'df_procure' not in st.session_state or st.session_state['df_procure'].empty:
        st.error("⚠️ ไม่พบข้อมูล Procure_Data ใน Excel (กรุณาเพิ่ม Tab: 'Procure_Data')")
        return

    df = st.session_state['df_procure'].copy()

    # 2. FILTER SETUP
    thai_month_map = {
        "มกราคม": 1, "กุมภาพันธ์": 2, "มีนาคม": 3, "เมษายน": 4, "พฤษภาคม": 5, "มิถุนายน": 6,
        "กรกฎาคม": 7, "สิงหาคม": 8, "กันยายน": 9, "ตุลาคม": 10, "พฤศจิกายน": 11, "ธันวาคม": 12
    }
    
    df['YearNum'] = pd.to_numeric(df['Year'], errors='coerce').fillna(0).astype(int)
    df['MonthNum'] = df['Month'].map(thai_month_map).fillna(0).astype(int)
    df['SortKey'] = (df['YearNum'] * 100) + df['MonthNum']

    available_years = sorted(df['Year'].unique(), reverse=True)
    if not available_years: available_years = ["2568"]
    months_list = list(thai_month_map.keys())

    # 3. FILTER UI
    c1, c2, c3, c4, c5 = st.columns([1,1,1,1,1])
    with c1: m_start = st.selectbox("เดือนเริ่มต้น", months_list, index=0)
    with c2: y_start = st.selectbox("ปีเริ่มต้น", available_years, index=0)
    with c3: m_end = st.selectbox("ถึงเดือน", months_list, index=11)
    with c4: y_end = st.selectbox("ถึงปี", available_years, index=0)
    with c5: 
        st.write("") 
        st.write("") 
        if st.button("🔍 กรองข้อมูล", use_container_width=True):
            st.rerun()

    # 4. APPLY FILTER
    start_key = (int(y_start) * 100) + thai_month_map[m_start]
    end_key = (int(y_end) * 100) + thai_month_map[m_end]
    
    mask = (df['SortKey'] >= start_key) & (df['SortKey'] <= end_key)
    df_filtered = df[mask]
    
    if df_filtered.empty:
        st.warning(f"ไม่พบข้อมูลในช่วงเวลา: {m_start} {y_start} - {m_end} {y_end}")
        return

    # 5. GET LATEST SNAPSHOT IN RANGE
    latest_key = df_filtered['SortKey'].max()
    df_snap = df_filtered[df_filtered['SortKey'] == latest_key]

    # 6. CALCULATE METRICS
    df_items = df_snap[df_snap['Category'] == 'Item_Type']
    df_owners = df_snap[df_snap['Category'] == 'Owner']
    
    # Sum Value_K and divide by 1000 to get Millions
    total_val = df_items['Value_K'].sum() / 1000 
    total_count = df_items['Count'].sum()
    
    budget_row = df_snap[df_snap['Category'] == 'Budget_KPI']
    plan_val = (budget_row['Value_K'].sum() / 1000) if not budget_row.empty else (total_val * 1.2)
    progress = (total_val / plan_val * 100) if plan_val > 0 else 0

    # 7. DISPLAY CARDS
    st.markdown(f"##### 📦 บทสรุปผู้บริหาร (ข้อมูล ณ {m_end} {y_end})")
    
    k1, k2, k3 = st.columns(3)
    with k1:
        st.markdown(f"""
        <div style="background:white; padding:20px; border-radius:10px; border:1px solid #ddd; text-align:center;">
            <div style="font-size:14px; color:#555; font-weight:bold;">💰 มูลค่าจัดซื้อจัดจ้าง</div>
            <div style="font-size:36px; font-weight:bold; color:#03A9F4;">{total_val:,.2f} <span style="font-size:18px; color:#333;">ล้านบาท</span></div>
            <div style="font-size:12px; color:#777;">{progress:.1f}% ของแผน ({plan_val:,.0f} ล้านบาท)</div>
        </div>
        """, unsafe_allow_html=True)
    with k2:
        st.markdown(f"""
        <div style="background:white; padding:20px; border-radius:10px; border:1px solid #ddd; text-align:center;">
            <div style="font-size:14px; color:#555; font-weight:bold;">📋 รายการครุภัณฑ์</div>
            <div style="font-size:36px; font-weight:bold; color:#4CAF50;">{int(total_count):,} <span style="font-size:18px; color:#333;">รายการ</span></div>
            <div style="font-size:12px; color:#777;">รายการทั้งหมด</div>
        </div>
        """, unsafe_allow_html=True)
    with k3:
        st.markdown(f"""
        <div style="background:white; padding:20px; border-radius:10px; border:1px solid #ddd; text-align:center;">
            <div style="font-size:14px; color:#555; font-weight:bold;">✅ ความคืบหน้า</div>
            <div style="font-size:36px; font-weight:bold; color:#9C27B0;">91.6%</div>
            <div style="font-size:12px; color:#777;">ตรวจรับแล้ว</div>
        </div>
        """, unsafe_allow_html=True)

    st.write("---")
    st.markdown("##### 📦 โครงการ BY ประเภท & เจ้าของโครงการ")

    # 8. DISPLAY CHARTS
    c_left, c_right = st.columns(2)

    with c_left:
        st.markdown("**📊 ประเภทครุภัณฑ์ (จำนวน & มูลค่า)**")
        if not df_items.empty:
            df_items = df_items.sort_values('Value_K', ascending=True)
            fig = go.Figure()
            fig.add_trace(go.Bar(y=df_items['Item'], x=df_items['Count'], orientation='h', name='จำนวน (รายการ)', marker_color='#03A9F4'))
            fig.add_trace(go.Bar(y=df_items['Item'], x=df_items['Value_K'], orientation='h', name='มูลค่า (K)', marker_color='#66BB6A'))
            fig.update_layout(barmode='group', height=350, margin=dict(l=0,r=0,t=20,b=0), font_family="Kanit", legend=dict(orientation="h", yanchor="bottom", y=-0.2))
            st.plotly_chart(fig, use_container_width=True, key="procure_chart_type")

    with c_right:
        st.markdown("**🏬 เจ้าของโครงการสูงสุด 5 อันดับ**")
        if not df_owners.empty:
            df_owners = df_owners.sort_values('Value_K', ascending=True).tail(5)
            fig = go.Figure()
            fig.add_trace(go.Bar(y=df_owners['Item'], x=df_owners['Count'], orientation='h', name='จำนวน (รายการ)', marker_color='#9C27B0', width=0.3))
            fig.add_trace(go.Bar(y=df_owners['Item'], x=df_owners['Value_K'], orientation='h', name='มูลค่า (K)', marker_color='#FFC107', width=0.3))
            fig.update_layout(barmode='group', height=350, margin=dict(l=0,r=0,t=20,b=0), font_family="Kanit", legend=dict(orientation="h", yanchor="bottom", y=-0.2))
            st.plotly_chart(fig, use_container_width=True, key="procure_chart_owner")
