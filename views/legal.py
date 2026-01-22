import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from utils.styles import render_header

def show_view():
    render_header("⚖️ สำนักนิติการ (Legal Affairs Office)", border_color="#8E24AA")
    
    # 1. LOAD DATA
    if 'df_legal' not in st.session_state or st.session_state['df_legal'].empty:
        st.error("⚠️ ไม่พบข้อมูล Legal_Data ใน Excel (Please add 'Legal_Data' tab)")
        return

    df = st.session_state['df_legal'].copy()
    
    # 2. PREPARE DATA FOR FILTERING
    # Map Thai months to numbers 1-12
    thai_month_map = {
        "มกราคม": 1, "กุมภาพันธ์": 2, "มีนาคม": 3, "เมษายน": 4, "พฤษภาคม": 5, "มิถุนายน": 6,
        "กรกฎาคม": 7, "สิงหาคม": 8, "กันยายน": 9, "ตุลาคม": 10, "พฤศจิกายน": 11, "ธันวาคม": 12
    }
    
    # Create numeric columns for filtering
    # Ensure Year is numeric
    df['YearNum'] = pd.to_numeric(df['Year'], errors='coerce').fillna(0).astype(int)
    # Map Month name to Month Number
    df['MonthNum'] = df['Month'].map(thai_month_map).fillna(0).astype(int)
    # Create a "SortKey" (e.g., 256801 for Jan 2568) to compare ranges easily
    df['SortKey'] = (df['YearNum'] * 100) + df['MonthNum']

    # Get lists for dropdowns
    available_years = sorted(df['Year'].unique(), reverse=True)
    if not available_years: available_years = ["2568"]
    months_list = list(thai_month_map.keys())

    # 3. FILTER UI (Range Selector)
    c1, c2, c3, c4, c5 = st.columns([1,1,1,1,1])
    with c1: m_start = st.selectbox("เดือนเริ่มต้น", months_list, index=0) # Jan
    with c2: y_start = st.selectbox("ปีเริ่มต้น", available_years, index=0)
    with c3: m_end = st.selectbox("ถึงเดือน", months_list, index=11) # Dec
    with c4: y_end = st.selectbox("ถึงปี", available_years, index=0)
    with c5: 
        st.write("") 
        st.write("") 
        if st.button("🔍 กรองข้อมูล", use_container_width=True):
            st.rerun()

    # 4. APPLY FILTER LOGIC
    # Calculate Start and End Keys based on selection
    start_key = (int(y_start) * 100) + thai_month_map[m_start]
    end_key = (int(y_end) * 100) + thai_month_map[m_end]

    # Filter the dataframe
    mask = (df['SortKey'] >= start_key) & (df['SortKey'] <= end_key)
    df_filtered = df[mask]

    if df_filtered.empty:
        st.warning(f"ไม่พบข้อมูลในช่วงเวลา: {m_start} {y_start} - {m_end} {y_end}")
        # Create empty sum structure to avoid crash
        sums = {'Pending': 0, 'Completed': 0, 'Damages_Million': 0}
        group_data = pd.DataFrame(columns=['Group', 'Pending', 'Completed', 'Total', 'Rate'])
    else:
        # 5. AGGREGATE DATA (Summing up the filtered rows)
        sums = df_filtered[['Pending', 'Completed', 'Damages_Million']].sum()
        
        # Group by 'Group' (e.g. 'คดี', 'ละเมิด') to sum specific categories for charts
        group_data = df_filtered.groupby("Group")[['Pending', 'Completed']].sum().reset_index()
        group_data['Total'] = group_data['Pending'] + group_data['Completed']
        # Calculate Rate (Avoid division by zero)
        group_data['Rate'] = group_data.apply(lambda x: (x['Completed'] / x['Total'] * 100) if x['Total'] > 0 else 0, axis=1)

    # Calculate Totals for Cards
    total_cases = sums['Pending'] + sums['Completed']
    pending_total = sums['Pending']
    completed_total = sums['Completed']
    damages = sums['Damages_Million']

    st.markdown("### ภาพรวม")

    # --- ROW 1: KPI CARDS (Dynamic Data) ---
    c1, c2, c3, c4 = st.columns(4)

    # Card 1: Total Cases (Purple)
    with c1:
        st.markdown(f"""
        <div style="background:white; padding:15px; border-radius:10px; border-top: 5px solid #9C27B0; box-shadow: 0 2px 5px rgba(0,0,0,0.1);">
            <div style="font-size:36px; font-weight:bold; color:#9C27B0;">{int(total_cases):,} <span style="font-size:20px; color:#333;">เรื่อง</span></div>
            <div style="color:#777;">📋 ทั้งหมด (All Cases)</div>
        </div>
        """, unsafe_allow_html=True)

    # Card 2: Pending (Blue/Cyan)
    with c2:
        st.markdown(f"""
        <div style="background:white; padding:15px; border-radius:10px; border-top: 5px solid #03A9F4; box-shadow: 0 2px 5px rgba(0,0,0,0.1);">
            <div style="font-size:36px; font-weight:bold; color:#03A9F4;">{int(pending_total):,} <span style="font-size:20px; color:#333;">เรื่อง</span></div>
            <div style="color:#777;">⏳ อยู่ระหว่างดำเนินการ (Pending)</div>
        </div>
        """, unsafe_allow_html=True)

    # Card 3: Completed (Green)
    with c3:
        st.markdown(f"""
        <div style="background:white; padding:15px; border-radius:10px; border-top: 5px solid #4CAF50; box-shadow: 0 2px 5px rgba(0,0,0,0.1);">
            <div style="font-size:36px; font-weight:bold; color:#4CAF50;">{int(completed_total):,} <span style="font-size:20px; color:#333;">เรื่อง</span></div>
            <div style="color:#777;">✅ ดำเนินการเสร็จสิ้น (Done)</div>
        </div>
        """, unsafe_allow_html=True)

    # Card 4: Damages (Red)
    with c4:
        st.markdown(f"""
        <div style="background:white; padding:15px; border-radius:10px; border-top: 5px solid #F44336; box-shadow: 0 2px 5px rgba(0,0,0,0.1);">
            <div style="font-size:36px; font-weight:bold; color:#F44336;">{damages:,.2f} <span style="font-size:20px; color:#333;">ล้านบาท</span></div>
            <div style="color:#777;">💰 มูลค่าความเสียหาย (Damages)</div>
        </div>
        """, unsafe_allow_html=True)

    st.write("---")
    
    # --- ROW 2: CHARTS ---
    st.markdown("##### ภาระงานตามกลุ่ม แยกตาม 5 กลุ่มงาน")
    
    gc1, gc2 = st.columns([2, 1])

    # Left Chart: Stacked Bar (Workload)
    with gc1:
        st.markdown("###### 📊 ภาระงานตามกลุ่ม (แยกสถานะ)")
        if not group_data.empty:
            fig = go.Figure()
            # Pending Bar
            fig.add_trace(go.Bar(
                y=group_data['Group'], x=group_data['Pending'], 
                name='อยู่ระหว่างดำเนินการ',
                orientation='h', marker_color='#29B6F6',
                text=group_data['Pending'], textposition='auto'
            ))
            # Completed Bar
            fig.add_trace(go.Bar(
                y=group_data['Group'], x=group_data['Completed'], 
                name='ดำเนินการเสร็จสิ้น',
                orientation='h', marker_color='#66BB6A',
                text=group_data['Completed'], textposition='auto'
            ))
            
            fig.update_layout(
                barmode='stack', 
                height=350, 
                margin=dict(l=0,r=0,t=0,b=0), 
                font_family="Kanit",
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
            )
            st.plotly_chart(fig, use_container_width=True, key="legal_stack_chart")
        else:
            st.info("ไม่มีข้อมูลสำหรับแสดงกราฟ")

    # Right Chart: Rate (Completion %)
    with gc2:
        st.markdown("###### 📈 อัตราการดำเนินการเสร็จสิ้น")
        if not group_data.empty:
            # Color mapping for groups
            colors = ['#AB47BC', '#EF6C00', '#FFCA28', '#66BB6A', '#29B6F6'] 
            
            fig = px.bar(
                group_data, 
                x='Rate', 
                y='Group', 
                orientation='h', 
                text_auto='.1f',
                color='Group', # Color by group name to differentiate
                color_discrete_sequence=colors
            )
            
            fig.update_layout(
                height=350, 
                margin=dict(l=0,r=0,t=0,b=0), 
                xaxis_range=[0,105], # Give space for text
                font_family="Kanit",
                showlegend=False
            )
            fig.update_xaxes(title="เปอร์เซ็นต์ความสำเร็จ (%)")
            fig.update_yaxes(title=None, showticklabels=False) # Hide labels (redundant)
            st.plotly_chart(fig, use_container_width=True, key="legal_rate_chart")
        else:
            st.info("ไม่มีข้อมูล")
