import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from utils.styles import render_header

def show_view():
    render_header("สำนักการคลัง - กลุ่มบัญชี", border_color="#9C27B0")
    
    if 'df_finance' not in st.session_state or st.session_state['df_finance'].empty:
        st.error("⚠️ ไม่พบข้อมูล Finance_Data ใน Excel")
        return

    df = st.session_state['df_finance'].copy()

    # --- YEAR RANGE FILTER ---
    available_years = sorted(df['Year'].unique(), reverse=True)
    if not available_years: available_years = ["2568"]

    c1, c2, c3 = st.columns([1, 1, 4])
    with c1: 
        start_year = st.selectbox("ปีเริ่มต้น", available_years, index=0)
    with c2: 
        end_year = st.selectbox("ถึงปี", available_years, index=0)
    
    # Logic: For financial position (Balances), we usually look at the SNAPSHOT of the latest date selected.
    # So we filter for the 'end_year'.
    df_filtered = df[df['Year'] == str(end_year)]

    if df_filtered.empty:
        st.warning(f"ไม่มีข้อมูลสำหรับปี {end_year}")
        return

    # --- SECTION 1: INVESTMENT BREAKDOWN ---
    df_invest = df_filtered[df_filtered['Category'] == 'Investment'].copy()
    total_invest = df_invest['Amount'].sum()

    st.markdown(f"""
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:10px;">
            <h5 style="margin:0; font-weight:bold; color:#555;">ประเภทเงินลงทุน</h5>
            <div style="color:#777; font-size:14px;">รวม {total_invest:,.2f} ล้านบาท</div>
        </div>
    """, unsafe_allow_html=True)
    
    st.write("---")

    c1, c2 = st.columns([2, 1])

    with c1:
        # Sort by amount descending
        df_invest = df_invest.sort_values('Amount', ascending=False)
        
        # Color Mapping
        color_map = {
            'CIMB': '#9C27B0', # Purple
            'ธอส.': '#8BC34A', # Green
            'กรุงไทย': '#2196F3', # Blue
            'อื่นๆ': '#BDBDBD'   # Grey
        }
        
        for index, row in df_invest.iterrows():
            pct = (row['Amount'] / total_invest * 100) if total_invest > 0 else 0
            color = color_map.get(str(row.get('Detail', 'อื่นๆ')), '#999')
            
            # HTML for Custom Progress Bar Row
            st.markdown(f"""
            <div style="margin-bottom:15px;">
                <div style="display:flex; align-items:center; margin-bottom:5px;">
                    <span style="background:{color}; color:white; padding:2px 6px; border-radius:4px; font-size:10px; margin-right:8px; width:40px; text-align:center;">{row.get('Detail', '')}</span>
                    <span style="font-weight:bold; font-size:14px; color:#333; flex:1;">{row['Item']}</span>
                    <span style="font-weight:bold; font-size:16px; color:{color};">{pct:.1f}%</span>
                </div>
                <div style="font-size:12px; color:#777; margin-bottom:2px;">{row['Amount']:,.2f} ล้านบาท</div>
                <div style="width:100%; background-color:#eee; height:8px; border-radius:4px;">
                    <div style="width:{pct}%; background-color:{color}; height:8px; border-radius:4px;"></div>
                </div>
            </div>
            """, unsafe_allow_html=True)

    with c2:
        # Donut Chart
        if not df_invest.empty:
            colors = [color_map.get(str(x), '#999') for x in df_invest['Detail']]
            fig = go.Figure(data=[go.Pie(
                labels=df_invest['Detail'], 
                values=df_invest['Amount'], 
                hole=.6,
                marker=dict(colors=colors),
                textinfo='none' # Hide text on chart, rely on legend
            )])
            fig.update_layout(
                height=250, 
                margin=dict(l=0,r=0,t=0,b=0),
                showlegend=True,
                legend=dict(orientation="h", yanchor="top", y=-0.1),
                annotations=[dict(text="สัดส่วน<br>เงินลงทุน", x=0.5, y=0.5, font_size=14, showarrow=False)]
            )
            st.plotly_chart(fig, use_container_width=True, key="invest_donut")

    st.write("---")

    # --- SECTION 2: PROVINCIAL DEPOSITS ---
    df_dep = df_filtered[df_filtered['Category'] == 'Deposit'].copy()
    
    total_dep = df_dep['Amount'].sum()
    prov_count = df_dep['Item'].nunique() # Assuming Item is Province Name
    avg_dep = total_dep / prov_count if prov_count > 0 else 0
    max_dep = df_dep['Amount'].max()
    max_prov = df_dep.loc[df_dep['Amount'].idxmax()]['Item'] if not df_dep.empty else "-"
    min_dep = df_dep['Amount'].min()
    min_prov = df_dep.loc[df_dep['Amount'].idxmin()]['Item'] if not df_dep.empty else "-"

    st.markdown(f"""
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:10px;">
            <h5 style="margin:0; font-weight:bold; color:#555;">เงินฝาก สกสค.จังหวัด/กทม.</h5>
            <div style="color:#777; font-size:14px;">{prov_count} จังหวัด รวม {total_dep:,.2f} ล้านบาท</div>
        </div>
    """, unsafe_allow_html=True)

    # 4 Cards
    k1, k2, k3, k4 = st.columns(4)
    
    def metric_card(title, value, unit, subtext, bg_color="white", text_color="#333", border_color="#ddd"):
        st.markdown(f"""
        <div style="background:{bg_color}; padding:15px; border-radius:8px; border:1px solid {border_color}; text-align:center; height:120px; display:flex; flex-direction:column; justify-content:center;">
            <div style="font-size:13px; color:{text_color if bg_color=='white' else 'white'}; opacity:0.8;">{title}</div>
            <div style="font-size:26px; font-weight:bold; color:{text_color if bg_color=='white' else 'white'};">{value}</div>
            <div style="font-size:12px; color:{text_color if bg_color=='white' else 'white'}; opacity:0.8;">{unit}</div>
            <div style="font-size:12px; color:{text_color if bg_color=='white' else 'white'}; margin-top:5px;">{subtext}</div>
        </div>
        """, unsafe_allow_html=True)

    with k1: metric_card("รวมทั้งหมด", f"{total_dep:,.2f}", "ล้านบาท", "", bg_color="#4285F4", border_color="#4285F4")
    with k2: metric_card("ค่าเฉลี่ย", f"{avg_dep:,.2f}", "ล้านบาท/จังหวัด", "")
    with k3: metric_card("สูงสุด", f"{max_dep:,.2f}", "ล้านบาท", max_prov)
    with k4: metric_card("ต่ำสุด", f"{min_dep:,.2f}", "ล้านบาท", min_prov)

    st.write("")
    
    # --- DATA TABLE ---
    # Sort and create Rank
    df_dep = df_dep.sort_values('Amount', ascending=False).reset_index(drop=True)
    df_dep.index = df_dep.index + 1 # Rank starts at 1
    
    # Display as a clean dataframe
    st.markdown("###### 📋 รายละเอียดรายจังหวัด")
    
    # Create 3 columns layout for the list to look like the image
    # We will just show a nice interactive table for simplicity and better UX than static list
    
    # Custom CSS for table
    st.markdown("""
    <style>
        .stDataFrame { font-size: 14px; }
    </style>
    """, unsafe_allow_html=True)
    
    # Format for display
    display_df = df_dep[['Item', 'Amount']].rename(columns={'Item': 'จังหวัด', 'Amount': 'ยอดเงินฝาก (ล้านบาท)'})
    
    st.dataframe(
        display_df,
        use_container_width=True,
        column_config={
            "ยอดเงินฝาก (ล้านบาท)": st.column_config.NumberColumn(format="%.2f")
        },
        height=400
    )
