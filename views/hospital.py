import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from utils.styles import render_header

def show_view():
    render_header("🏥 โรงพยาบาล (Hospital Dashboard)", border_color="#00897B")
    
    if 'df_hospital' not in st.session_state or st.session_state['df_hospital'].empty:
        st.error("⚠️ ไม่พบข้อมูล Hospital_Data ใน Excel (Please add 'Hospital_Data' tab)")
        return

    df = st.session_state['df_hospital'].copy()

    # --- 1. RANGE FILTER LOGIC ---
    thai_month_map = {
        "มกราคม": 1, "กุมภาพันธ์": 2, "มีนาคม": 3, "เมษายน": 4, "พฤษภาคม": 5, "มิถุนายน": 6,
        "กรกฎาคม": 7, "สิงหาคม": 8, "กันยายน": 9, "ตุลาคม": 10, "พฤศจิกายน": 11, "ธันวาคม": 12
    }
    
    # Create numeric keys for sorting
    df['YearNum'] = pd.to_numeric(df['Year'], errors='coerce').fillna(0).astype(int)
    df['MonthNum'] = df['Month'].map(thai_month_map).fillna(0).astype(int)
    df['SortKey'] = (df['YearNum'] * 100) + df['MonthNum']

    available_years = sorted(df['Year'].unique(), reverse=True)
    if not available_years: available_years = ["2568"]
    months_list = list(thai_month_map.keys())

    # Range Selectors
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

    # --- 2. AGGREGATE DATA ---
    # Sum up columns if data exists
    if df_filtered.empty:
        st.warning(f"ไม่พบข้อมูลในช่วงเวลา: {m_start} {y_start} - {m_end} {y_end}")
        sums = {col: 0 for col in df.columns if col not in ['Year','Month','SortKey']}
    else:
        # Sum numeric columns
        sums = df_filtered.sum(numeric_only=True)
        # Average "Avg Revenue" instead of summing it? No, usually in dashboard totals we recalculate
        # But for simplicity, we can calculate Avg Revenue as (Total Rev / Total Patients) later
    
    total_rev = sums.get('Revenue_Million', 0)
    total_patients = sums.get('Patients', 0)
    # Re-calculate average based on total range
    avg_rev = (total_rev * 1000000 / total_patients) if total_patients > 0 else 0
    # For provinces/units, we usually want the MAX or Unique count, not Sum. 
    # But if we treat it as "Total Service Events", Sum is okay. 
    # Let's assume user wants "Latest" snapshot for Unit Count, but Sum for Attendance.
    # Actually, for "Range", summing Provinces/Units might be wrong (double counting).
    # Let's use the MAX of the period for infrastructure counts.
    if not df_filtered.empty:
        max_prov = df_filtered['Provinces'].max()
        max_units = df_filtered['Units'].max()
    else:
        max_prov, max_units = 0, 0
        
    registered = sums.get('Registered', 0)
    attended = sums.get('Attended', 0)
    attend_rate = (attended / registered * 100) if registered > 0 else 0

    st.markdown("### 📊 สรุปภาพรวม")

    # --- ROW 1: KPI CARDS ---
    c1, c2, c3, c4 = st.columns(4)
    
    with c1:
        st.markdown(f"""
        <div style="background:white; padding:15px; border-radius:8px; border-top: 5px solid #FFCA28; box-shadow: 0 2px 5px rgba(0,0,0,0.1);">
            <div style="color:#555; font-size:14px;">💰 รายได้รวม</div>
            <div style="font-size:32px; font-weight:bold; color:#0288D1;">{total_rev:,.2f} <span style="font-size:16px; color:#333;">ล้านบาท</span></div>
        </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown(f"""
        <div style="background:white; padding:15px; border-radius:8px; border-top: 5px solid #29B6F6; box-shadow: 0 2px 5px rgba(0,0,0,0.1);">
            <div style="color:#555; font-size:14px;">👥 ผู้รับบริการรวม</div>
            <div style="font-size:32px; font-weight:bold; color:#43A047;">{int(total_patients):,} <span style="font-size:16px; color:#333;">ราย</span></div>
        </div>
        """, unsafe_allow_html=True)
    with c3:
        st.markdown(f"""
        <div style="background:white; padding:15px; border-radius:8px; border-top: 5px solid #AB47BC; box-shadow: 0 2px 5px rgba(0,0,0,0.1);">
            <div style="color:#555; font-size:14px;">📈 รายได้เฉลี่ยต่อราย</div>
            <div style="font-size:32px; font-weight:bold; color:#8E24AA;">{int(avg_rev):,} <span style="font-size:16px; color:#333;">บาท/ราย</span></div>
        </div>
        """, unsafe_allow_html=True)
    with c4:
        st.markdown(f"""
        <div style="background:white; padding:15px; border-radius:8px; border-top: 5px solid #EF5350; box-shadow: 0 2px 5px rgba(0,0,0,0.1);">
            <div style="color:#555; font-size:14px;">📍 จำนวนการออกหน่วยบริการ</div>
            <div style="font-size:32px; font-weight:bold; color:#F57F17;">{int(max_prov)} <span style="font-size:16px; color:#333;">จังหวัด</span></div>
            <div style="color:#777; font-size:12px;">{int(max_units)} หน่วยตรวจ</div>
        </div>
        """, unsafe_allow_html=True)

    st.write("---")
    st.markdown("##### 🩺 ผลตรวจสุขภาพ")

    # --- ROW 2: DETAILED STATS ---
    col1, col2, col3 = st.columns([1, 1.5, 1])

    # 1. Summary Box (Left)
    with col1:
        st.markdown("###### 📍 สรุปออกหน่วยตรวจสุขภาพ")
        st.markdown(f"""
        <div style="background:white; padding:20px; border-radius:10px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); text-align:center;">
            <div style="display:flex; justify-content:space-around; margin-bottom:15px;">
                <div>
                    <div style="font-size:24px; color:#0288D1; font-weight:bold;">{int(max_prov)}</div>
                    <div style="font-size:12px; color:#666;">จังหวัด</div>
                </div>
                <div>
                    <div style="font-size:24px; color:#8E24AA; font-weight:bold;">{int(max_units)}</div>
                    <div style="font-size:12px; color:#666;">หน่วยตรวจ</div>
                </div>
            </div>
            <hr style="margin:10px 0;">
            <div style="display:flex; justify-content:space-around;">
                <div>
                    <div style="font-size:20px; color:#F57C00; font-weight:bold;">{int(registered):,}</div>
                    <div style="font-size:12px; color:#666;">ผู้แจ้งตรวจ</div>
                </div>
                <div>
                    <div style="font-size:20px; color:#2E7D32; font-weight:bold;">{int(attended):,}</div>
                    <div style="font-size:12px; color:#666;">ผู้ตรวจจริง</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.write("")
        st.markdown("**อัตราการมาตรวจ**")
        st.progress(attend_rate/100)
        st.caption(f"ผู้ตรวจจริง {attend_rate:.1f}% | ไม่มาตรวจ {100-attend_rate:.1f}%")

    # 2. Age Group Chart (Center)
    with col2:
        st.markdown("###### 📊 ผู้เข้ารับการตรวจแยกตามกลุ่มอายุ")
        
        age_data = pd.DataFrame({
            "Age Group": ["20-30 ปี", "31-40 ปี", "41-50 ปี", "51-60 ปี", "60+ ปี"],
            "Count": [
                sums.get('Age_20_30', 0),
                sums.get('Age_31_40', 0),
                sums.get('Age_41_50', 0),
                sums.get('Age_51_60', 0),
                sums.get('Age_60_Plus', 0)
            ]
        })
        
        fig_age = px.bar(age_data, x="Age Group", y="Count", color="Age Group",
                         color_discrete_sequence=['#29B6F6', '#66BB6A', '#AB47BC', '#FFCA28', '#EF5350'])
        fig_age.update_layout(height=350, margin=dict(t=20, b=0, l=0, r=0), showlegend=False, font_family="Kanit")
        st.plotly_chart(fig_age, use_container_width=True, key="hosp_age_chart")

    # 3. Donut Charts (Right)
    with col3:
        st.markdown("###### 👥 ผู้เข้ารับการตรวจ")
        
        # Donut 1: Member Status
        labels_mem = ['ในประจำการ', 'นอกประจำการ']
        values_mem = [sums.get('Member_In', 0), sums.get('Member_Out', 0)]
        fig_mem = go.Figure(data=[go.Pie(labels=labels_mem, values=values_mem, hole=.6, 
                                         marker_colors=['#039BE5', '#43A047'])])
        fig_mem.update_layout(height=180, margin=dict(t=0, b=0, l=0, r=0), showlegend=True, 
                              legend=dict(orientation="v", yanchor="middle", y=0.5, xanchor="left", x=1.1))
        st.plotly_chart(fig_mem, use_container_width=True, key="hosp_mem_pie")
        
        # Donut 2: Gender
        labels_gen = ['ชาย', 'หญิง']
        values_gen = [sums.get('Male', 0), sums.get('Female', 0)]
        fig_gen = go.Figure(data=[go.Pie(labels=labels_gen, values=values_gen, hole=.6, 
                                         marker_colors=['#00ACC1', '#E91E63'])])
        fig_gen.update_layout(height=180, margin=dict(t=0, b=0, l=0, r=0), showlegend=True,
                              legend=dict(orientation="v", yanchor="middle", y=0.5, xanchor="left", x=1.1))
        st.plotly_chart(fig_gen, use_container_width=True, key="hosp_gen_pie")
