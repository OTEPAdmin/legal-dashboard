import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# --- PAGE CONFIG ---
st.set_page_config(page_title="Legal Affairs Dashboard", layout="wide")

# Custom CSS to match the light grey background and card styling
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    div[data-testid="stMetricValue"] { font-size: 28px; font-weight: bold; }
    .stTable { background-color: white; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- HEADER / FILTERS ---
st.title("⚖️ Dashboard นิติการ (Legal Dashboard)")

with st.container():
    col_f1, col_f2, col_f3, col_f4, col_f5 = st.columns([2, 1, 1, 2, 1])
    with col_f1:
        st.selectbox("ช่วงเวลา (Start Month):", ["ตุลาคม", "พฤศจิกายน", "ธันวาคม"], index=0)
    with col_f2:
        st.selectbox("ปี (Year):", ["2567", "2568"], index=1)
    with col_f3:
        st.write("ถึง")
    with col_f4:
        st.selectbox("สิ้นสุด (End Month):", ["ธันวาคม", "มกราคม"], index=0)
    with col_f5:
        st.button("🔍 กรองข้อมูล", use_container_width=True)

st.divider()

# --- ROW 1: KPI CARDS ---
col1, col2, col3, col4 = st.columns(4)

metrics = [
    {"label": "45 เรื่อง", "sub": "ทั้งหมด", "color": "#7b2cbf"},
    {"label": "28 เรื่อง", "sub": "อยู่ระหว่างดำเนินการ", "color": "#00b4d8"},
    {"label": "17 เรื่อง", "sub": "ดำเนินการเสร็จสิ้น", "color": "#70e000"},
    {"label": "1.25 ล้านบาท", "sub": "มูลค่าความเสียหาย", "color": "#e63946"}
]

for i, col in enumerate([col1, col2, col3, col4]):
    with col:
        st.markdown(f"""
            <div style="padding:20px; border-radius:10px; background-color:white; border-left: 8px solid {metrics[i]['color']}; box-shadow: 2px 2px 5px rgba(0,0,0,0.05)">
                <h2 style="margin:0; color:{metrics[i]['color']}">{metrics[i]['label']}</h2>
                <p style="margin:0; color:grey;">{metrics[i]['sub']}</p>
            </div>
        """, unsafe_allow_html=True)

st.write("") # Spacer

# --- ROW 2: MAIN CHARTS ---
chart_col_left, chart_col_right = st.columns([2, 1])

with chart_col_left:
    st.subheader("ภาระงานตามกลุ่ม (แยกตามสถานะ)")
    # Mock data for stacked bar
    df_stack = pd.DataFrame({
        "กลุ่มงาน": ["สืบสวน-วินัย", "อุทธรณ์-ร้องทุกข์", "ร้องเรียน", "ละเมิด", "คดี"],
        "อยู่ระหว่างดำเนินการ": [9, 5, 6, 2, 6],
        "ดำเนินการเสร็จสิ้น": [3, 5, 4, 2, 4]
    })
    fig_stack = px.bar(df_stack, y="กลุ่มงาน", x=["อยู่ระหว่างดำเนินการ", "ดำเนินการเสร็จสิ้น"], 
                       orientation='h', barmode='stack',
                       color_discrete_map={"อยู่ระหว่างดำเนินการ": "#00b4d8", "ดำเนินการเสร็จสิ้น": "#70e000"})
    fig_stack.update_layout(height=350, margin=dict(l=0, r=0, t=20, b=0), legend=dict(orientation="h", y=1.1))
    st.plotly_chart(fig_stack, use_container_width=True)

with chart_col_right:
    st.subheader("อัตราการดำเนินการเสร็จสิ้น")
    df_perc = pd.DataFrame({
        "กลุ่มงาน": ["สืบสวน-วินัย", "อุทธรณ์-ร้องทุกข์", "ร้องเรียน", "ละเมิด", "คดี"],
        "Percentage": [20, 50, 40, 50, 42],
        "Color": ["#00b4d8", "#70e000", "#ffbe0b", "#fb5607", "#8338ec"]
    })
    fig_perc = px.bar(df_perc, x="Percentage", y="กลุ่มงาน", orientation='h', color="กลุ่มงาน",
                      color_discrete_sequence=df_perc["Color"].tolist())
    fig_perc.update_layout(showlegend=False, height=350)
    st.plotly_chart(fig_perc, use_container_width=True)

# --- ROW 3: DONUT CHARTS ---
st.subheader("วิเคราะห์ข้อมูล")
d1, d2, d3 = st.columns(3)

with d1:
    st.write("สัดส่วนงานตามกลุ่ม")
    fig1 = px.pie(values=[24, 22, 22, 9, 22], names=["สืบสวน", "อุทธรณ์", "ร้องเรียน", "ละเมิด", "คดี"], hole=0.6)
    st.plotly_chart(fig1, use_container_width=True)

with d2:
    st.write("สถานะการดำเนินการรวม")
    # Custom Gauge/Donut for 37.8%
    fig2 = go.Figure(go.Pie(values=[37.8, 62.2], hole=0.7, marker_colors=["#00b4d8", "#e9ecef"], showlegend=False))
    fig2.add_annotation(text="37.8%", x=0.5, y=0.5, font_size=24, showarrow=False)
    st.plotly_chart(fig2, use_container_width=True)

with d3:
    st.write("ประเภทคดีความ")
    fig3 = px.pie(values=[5, 3, 2], names=["ปกครอง", "แพ่ง", "อาญา"], hole=0.6)
    st.plotly_chart(fig3, use_container_width=True)

# --- ROW 4: DATA TABLE ---
st.subheader("รายการคดีล่าสุด")
table_data = {
    "ลำดับ": [1, 2, 3, 4],
    "เรื่อง": ["คดีบรรจุแต่งตั้งตำแหน่ง", "คดีเลิกจ้างไม่เป็นธรรม", "คดียักยอกทรัพย์", "คดีฟ้องเพิกถอนคำสั่ง"],
    "ประเภทคดี": ["ปกครอง", "แพ่ง", "อาญา", "ปกครอง"],
    "ศาล": ["ปกครองกลาง", "แพ่งกรุงเทพ", "อาญากรุงเทพ", "ปกครองสูงสุด"],
    "สถานะ": ["โจทก์", "จำเลย", "โจทก์", "จำเลย"],
    "สถานะคดี": ["ศาลชั้นต้น", "ศาลอุทธรณ์", "เสร็จสิ้น", "ศาลฎีกา"]
}
st.table(pd.DataFrame(table_data))