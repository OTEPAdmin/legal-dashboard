import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# --- 1. SET PAGE CONFIG ---
st.set_page_config(page_title="Dashboard นิติการ", layout="wide")

# --- 2. THAI FONT & CUSTOM CSS ---
# ใช้ Font 'Sarabun' เพื่อให้เหมือนกับระบบราชการและดูเป็นมืออาชีพ
st.markdown("""
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Sarabun:wght@300;400;700&display=swap" rel="stylesheet">
    <style>
        html, body, [class*="css"] {
            font-family: 'Sarabun', sans-serif !important;
        }
        .stMetric {
            background-color: #ffffff;
            padding: 15px;
            border-radius: 10px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        }
        /* ปรับสีปุ่มกรองข้อมูล */
        .stButton>button {
            background-color: #45B1CD;
            color: white;
            border-radius: 5px;
        }
    </style>
    """, unsafe_allow_html=True)

# --- 3. HEADER & FILTERS ---
st.title("⚖️ Dashboard นิติการ")

with st.container():
    col_f1, col_f2, col_f3, col_f4, col_f5 = st.columns([2, 1, 0.5, 2, 1])
    with col_f1:
        st.selectbox("ช่วงเวลา:", ["ตุลาคม", "พฤศจิกายน", "ธันวาคม", "มกราคม"], index=0)
    with col_f2:
        st.selectbox("ปี:", ["2567", "2568"], index=1)
    with col_f3:
        st.write("<br>ถึง", unsafe_allow_html=True)
    with col_f4:
        st.selectbox("สิ้นสุด:", ["ธันวาคม", "มกราคม", "กุมภาพันธ์"], index=1)
    with col_f5:
        st.write("<br>", unsafe_allow_html=True)
        st.button("🔍 กรองข้อมูล", use_container_width=True)

st.divider()

# --- 4. KPI CARDS (ภาพรวม) ---
st.subheader("ภาพรวม")
kpi1, kpi2, kpi3, kpi4 = st.columns(4)

with kpi1:
    st.metric(label="ทั้งหมด", value="45 เรื่อง")
with kpi2:
    st.metric(label="อยู่ระหว่างดำเนินการ", value="28 เรื่อง")
with kpi3:
    st.metric(label="ดำเนินการเสร็จสิ้น", value="17 เรื่อง")
with kpi4:
    st.metric(label="มูลค่าความเสียหาย", value="1.25 ล้านบาท")

st.write("<br>", unsafe_allow_html=True)

# --- 5. MIDDLE ROW: BAR CHARTS ---
col_left, col_right = st.columns([1.5, 1])

with col_left:
    st.markdown("### 📊 ภาระงานตามกลุ่ม (แยกตามสถานะ)")
    df_stack = pd.DataFrame({
        "กลุ่มงาน": ["สืบสวน-วินัย", "อุทธรณ์-ร้องทุกข์", "ร้องเรียน", "ละเมิด", "คดี"],
        "อยู่ระหว่างดำเนินการ": [9, 5, 6, 2, 6],
        "ดำเนินการเสร็จสิ้น": [3, 5, 4, 2, 4]
    })
    fig_stack = px.bar(
        df_stack, y="กลุ่มงาน", x=["อยู่ระหว่างดำเนินการ", "ดำเนินการเสร็จสิ้น"], 
        orientation='h', barmode='stack',
        color_discrete_map={"อยู่ระหว่างดำเนินการ": "#45B1CD", "ดำเนินการเสร็จสิ้น": "#6ECB93"}
    )
    fig_stack.update_layout(font_family="Sarabun", margin=dict(l=0, r=0, t=20, b=0), height=300, legend=dict(orientation="h", y=1.1))
    st.plotly_chart(fig_stack, use_container_width=True)

with col_right:
    st.markdown("### 📈 อัตราการดำเนินการเสร็จสิ้น")
    df_rate = pd.DataFrame({
        "กลุ่มงาน": ["สืบสวน-วินัย", "อุทธรณ์-ร้องทุกข์", "ร้องเรียน", "ละเมิด", "คดี"],
        "เปอร์เซ็นต์": [20, 50, 40, 50, 42],
        "Color": ["#45B1CD", "#6ECB93", "#FBC02D", "#F57C00", "#A367DC"]
    })
    fig_rate = px.bar(df_rate, x="เปอร์เซ็นต์", y="กลุ่มงาน", orientation='h', color="กลุ่มงาน", color_discrete_sequence=df_rate["Color"].tolist())
    fig_rate.update_layout(font_family="Sarabun", showlegend=False, height=300, margin=dict(l=0, r=0, t=20, b=0))
    st.plotly_chart(fig_rate, use_container_width=True)

# --- 6. ANALYSIS ROW: DONUT CHARTS ---
st.divider()
st.subheader("วิเคราะห์ข้อมูล")
d1, d2, d3 = st.columns(3)

with d1:
    st.write("**สัดส่วนงานตามกลุ่ม**")
    fig1 = px.pie(values=[24, 22, 22, 9, 22], names=["สืบสวน", "อุทธรณ์", "ร้องเรียน", "ละเมิด", "คดี"], hole=0.6,
                  color_discrete_sequence=['#A367DC', '#6ECB93', '#FBC02D', '#F57C00', '#45B1CD'])
    fig1.update_layout(font_family="Sarabun", margin=dict(l=20, r=20, t=20, b=20))
    st.plotly_chart(fig1, use_container_width=True)

with d2:
    st.write("**สถานะการดำเนินการรวม**")
    fig2 = go.Figure(go.Pie(values=[37.8, 62.2], hole=0.7, marker_colors=["#45B1CD", "#E9ECEF"], showlegend=False))
    fig2.add_annotation(text="37.8%<br>เสร็จสิ้น", x=0.5, y=0.5, font_size=20, showarrow=False, font_family="Sarabun")
    fig2.update_layout(margin=dict(l=20, r=20, t=20, b=20))
    st.plotly_chart(fig2, use_container_width=True)

with d3:
    st.write("**ประเภทคดีความ**")
    fig3 = px.pie(values=[5, 3, 2], names=["ปกครอง", "แพ่ง", "อาญา"], hole=0.6,
                  color_discrete_sequence=['#45B1CD', '#6ECB93', '#F57C00'])
    fig3.update_layout(font_family="Sarabun", margin=dict(l=20, r=20, t=20, b=20))
    st.plotly_chart(fig3, use_container_width=True)

# --- 7. BOTTOM ROW: DATA TABLE ---
st.divider()
st.subheader("📋 รายการคดีล่าสุด")
table_data = pd.DataFrame({
    "ลำดับ": [1, 2, 3, 4],
    "เรื่อง": ["คดีบรรจุแต่งตั้งตำแหน่ง", "คดีเลิกจ้างไม่เป็นธรรม", "คดียักยอกทรัพย์", "คดีฟ้องเพิกถอนคำสั่ง"],
    "ประเภทคดี": ["ปกครอง", "แพ่ง", "อาญา", "ปกครอง"],
    "ศาล": ["ปกครองกลาง", "แพ่งกรุงเทพ", "อาญากรุงเทพ", "ปกครองสูงสุด"],
    "สถานะสำนักงาน": ["โจทก์", "จำเลย", "โจทก์", "จำเลย"],
    "สถานะคดี": ["ศาลชั้นต้น", "ศาลอุทธรณ์", "เสร็จสิ้น", "ศาลฎีกา"]
})

# ปรับการแสดงผลตารางให้สวยงาม
st.dataframe(table_data, use_container_width=True, hide_index=True)

st.caption("อัปเดตข้อมูลล่าสุด: 24 ธันวาคม 2568")
