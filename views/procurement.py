import streamlit as st
import pandas as pd
import plotly.express as px
from utils.styles import render_header

def show_view():
    render_header("สำนักการคลัง - กลุ่มการพัสดุและอาคารสถานที่", border_color="#795548")

    # 1. LOAD DATA
    if 'df_procure' not in st.session_state or st.session_state['df_procure'].empty:
        st.warning("⚠️ ไม่พบข้อมูล Procure_Data (กรุณาอัปโหลดไฟล์ Excel)")
        return

    df = st.session_state['df_procure'].copy()

    # --- SAFETY CHECK: Verify Columns Exist ---
    required_cols = ['Year', 'Month', 'Category', 'Item', 'Value']
    missing_cols = [c for c in required_cols if c not in df.columns]
    
    if missing_cols:
        st.error(f"❌ ข้อมูลไม่ถูกต้อง: ไม่พบคอลัมน์ {missing_cols} ใน Tab 'Procure_Data'")
        st.info("💡 กรุณาตรวจสอบหัวตารางใน Excel ต้องมี: Year, Month, Category, Item, Value")
        return
    # ------------------------------------------

    # 2. FILTER LOGIC
    thai_month_map = {
        "มกราคม": 1, "กุมภาพันธ์": 2, "มีนาคม": 3, "เมษายน": 4, "พฤษภาคม": 5, "มิถุนายน": 6,
        "กรกฎาคม": 7, "สิงหาคม": 8, "กันยายน": 9, "ตุลาคม": 10, "พฤศจิกายน": 11, "ธันวาคม": 12
    }

    # Generate SortKey if missing
    if 'SortKey' not in df.columns:
        df['YearNum'] = pd.to_numeric(df['Year'], errors='coerce').fillna(0).astype(int)
        df['MonthNum'] = df['Month'].map(thai_month_map).fillna(0).astype(int)
        df['SortKey'] = (df['YearNum'] * 100) + df['MonthNum']

    available_years = sorted(df['Year'].unique(), reverse=True)
    if not available_years: available_years = ["2568"]
    months_list = list(thai_month_map.keys())

    # Filter UI
    st.markdown("##### 🔎 ตัวเลือกการกรอง (Filter)")
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

    # Apply Filter
    start_key = (int(y_start) * 100) + thai_month_map[m_start]
    end_key = (int(y_end) * 100) + thai_month_map[m_end]
    mask = (df['SortKey'] >= start_key) & (df['SortKey'] <= end_key)
    df_filtered = df[mask]

    if df_filtered.empty:
        st.warning(f"ไม่พบข้อมูลในช่วงเวลา: {m_start} {y_start} - {m_end} {y_end}")
        return

    # --- KPI CARDS ---
    # 1. Procurement Value (Sum of filtered period)
    procure_val = df_filtered[df_filtered['Category'] == 'Procurement']['Value'].sum()
    
    # 2. Budget Remaining (Budget - Procurement)
    budget_val = df_filtered[df_filtered['Category'] == 'Budget']['Value'].sum()
    budget_remain = budget_val - procure_val
    
    # 3. Inventory Count (Snapshot of latest month only)
    latest_key = df_filtered['SortKey'].max()
    inventory_val = df_filtered[(df_filtered['SortKey'] == latest_key) & (df_filtered['Category'] == 'Inventory')]['Value'].sum()

    c1, c2, c3 = st.columns(3)
    with c1:
        st.metric("📦 มูลค่าการจัดซื้อสะสม", f"{procure_val:,.0f} บาท", delta="Year-to-Date")
    with c2:
        st.metric("💰 งบประมาณคงเหลือ", f"{budget_remain:,.0f} บาท", delta=f"จากงบ {budget_val:,.0f}")
    with c3:
        st.metric("🏢 ครุภัณฑ์คงเหลือ (ล่าสุด)", f"{int(inventory_val):,} รายการ", delta="จำนวนชิ้น")

    st.write("---")

    # --- CHARTS ---
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📊 การเบิกจ่ายงบประมาณ (Budget Usage)")
        # Filter for Chart
        df_chart1 = df_filtered[df_filtered['Category'].isin(['Procurement', 'Budget'])]
        if not df_chart1.empty:
            # Sort by Month
            df_chart1 = df_chart1.sort_values('SortKey')
            fig = px.bar(df_chart1, x='Month', y='Value', color='Category', barmode='group',
                         color_discrete_map={'Budget': '#BDBDBD', 'Procurement': '#795548'})
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("ไม่มีข้อมูลการเบิกจ่าย")

    with col2:
        st.subheader("📦 สัดส่วนการจัดซื้อ (By Item)")
        df_items = df_filtered[df_filtered['Category'] == 'Procurement']
        if not df_items.empty:
            fig = px.pie(df_items, values='Value', names='Item', hole=0.4,
                         color_discrete_sequence=px.colors.sequential.Brown)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("ไม่มีข้อมูลประเภทการจัดซื้อ")
