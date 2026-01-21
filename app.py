import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import random

# -----------------------------------------------------------------------------
# 1. CONFIG & STYLING
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="EIS Platform",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for "Sarabun" Font and Executive Theme
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Sarabun:wght@300;400;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Sarabun', sans-serif;
    }
    
    /* Header Styling */
    .header-box {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #00acc1;
        margin-bottom: 20px;
    }
    .header-title {
        color: #2c3e50;
        font-size: 24px;
        font-weight: 700;
        margin: 0;
    }
    
    /* KPI Card Styling */
    .kpi-card {
        background-color: white;
        padding: 15px;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        text-align: center;
        margin-bottom: 10px;
        border: 1px solid #eee;
    }
    .kpi-title { font-size: 16px; color: #666; font-weight: 600; }
    .kpi-value { font-size: 28px; font-weight: bold; color: #333; }
    .kpi-sub-green { color: #28a745; font-size: 14px; }
    .kpi-sub-red { color: #dc3545; font-size: 14px; }
    
    /* Custom Colored Cards */
    .card-teal { border-top: 4px solid #00acc1; }
    .card-pink { border-top: 4px solid #e91e63; }
    .card-green { border-top: 4px solid #28a745; }
    
    </style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 2. MOCK DATA GENERATION
# -----------------------------------------------------------------------------
def get_member_stats():
    # Mock Data for Ch.P.K. (Teal) and Ch.P.S. (Pink)
    data = {
        "chpk": {"total": 45200, "new": 120, "removed": 45},
        "chps": {"total": 38100, "new": 85, "removed": 30}
    }
    
    # Mock Demographics
    df_gender = pd.DataFrame({
        "Group": ["Male", "Female", "Male", "Female"],
        "Type": ["ChPK", "ChPK", "ChPS", "ChPS"],
        "Count": [20000, 25200, 15000, 23100]
    })
    
    df_age = pd.DataFrame({
        "Age": ["20-30", "31-40", "41-50", "51-60", "60+"] * 2,
        "Type": ["ChPK"]*5 + ["ChPS"]*5,
        "Count": [2000, 5000, 8000, 12000, 18200, 1500, 4000, 7000, 11000, 14600]
    })
    
    df_death = pd.DataFrame({
        "Cause": ["Illness", "Accident", "Old Age", "Heart Failure", "Cancer"],
        "Count": [120, 45, 80, 60, 55]
    })
    
    return data, df_gender, df_age, df_death

def get_finance_data():
    df_trend = pd.DataFrame({
        "Month": ["Jan", "Feb", "Mar", "Apr", "May", "Jun"],
        "Rate": [85, 88, 87, 90, 92, 95]
    })
    return df_trend

def get_legal_data():
    df_cases = pd.DataFrame({
        "Subject": ["Corruption Case A", "Appeal Request B", "Land Dispute C", "Disciplinary Action D", "Contract Breach E"],
        "Court": ["Civil Court", "Admin Court", "Supreme Court", "Civil Court", "Admin Court"],
        "Status": ["Pending", "In Progress", "Done", "Pending", "Done"],
        "Value": [1500000, 0, 5000000, 0, 200000]
    })
    
    df_workload = pd.DataFrame({
        "Type": ["Investigation", "Appeal", "Complaint", "Civil Suit"],
        "Count": [15, 24, 40, 10]
    })
    
    return df_cases, df_workload

# -----------------------------------------------------------------------------
# 3. AUTHENTICATION & STATE MANAGEMENT
# -----------------------------------------------------------------------------
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
if 'role' not in st.session_state:
    st.session_state['role'] = None
if 'username' not in st.session_state:
    st.session_state['username'] = None

USERS = {
    "admin": {"pass": "admin123", "role": "Admin", "name": "System Administrator"},
    "user": {"pass": "user123", "role": "User", "name": "General Officer"}
}

def login():
    st.markdown("<h1 style='text-align: center; color: #00acc1;'>EIS Platform Login</h1>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.button("Login", use_container_width=True):
            if username in USERS and USERS[username]["pass"] == password:
                st.session_state['logged_in'] = True
                st.session_state['username'] = USERS[username]["name"]
                st.session_state['role'] = USERS[username]["role"]
                st.rerun()
            else:
                st.error("Invalid username or password")

def logout():
    st.session_state['logged_in'] = False
    st.session_state['role'] = None
    st.rerun()

# -----------------------------------------------------------------------------
# 4. MAIN APP LOGIC
# -----------------------------------------------------------------------------
if not st.session_state['logged_in']:
    login()
else:
    # --- Sidebar ---
    st.sidebar.image("https://via.placeholder.com/150x50.png?text=EIS+LOGO", use_container_width=True)
    st.sidebar.markdown(f"**User:** {st.session_state['username']}")
    st.sidebar.markdown(f"**Role:** {st.session_state['role']}")
    st.sidebar.markdown("---")
    
    # Navigation Logic
    options = ["EIS Dashboard", "Legal Dashboard"]
    if st.session_state['role'] == "Admin":
        options.append("Admin Control Panel")
        
    page = st.sidebar.radio("Navigation", options)
    
    st.sidebar.markdown("---")
    if st.sidebar.button("Logout"):
        logout()

    # --- PAGE 1: EIS DASHBOARD ---
    if page == "EIS Dashboard":
        # Header
        st.markdown("""
        <div class="header-box">
            <h1 class="header-title">บทสรุปผู้บริหาร (Executive Summary)</h1>
        </div>
        """, unsafe_allow_html=True)
        
        # Filters
        c1, c2, c3 = st.columns([1,1,4])
        with c1: st.selectbox("Month", ["January", "February", "March", "April"])
        with c2: st.selectbox("Year", ["2568", "2567"])
        
        st.markdown("---")
        
        # === Section A: Member Stats ===
        st.subheader("📊 สถิติสมาชิก (Membership Statistics)")
        
        stats, df_gender, df_age, df_death = get_member_stats()
        
        # KPI Cards Row
        k1, k2 = st.columns(2)
        
        # Card 1: Ch.P.K. (Teal)
        with k1:
            st.markdown(f"""
            <div class="kpi-card card-teal">
                <div class="kpi-title">สมาชิก ช.พ.ค. (Ch.P.K.)</div>
                <div class="kpi-value">{stats['chpk']['total']:,}</div>
                <div>
                    <span class="kpi-sub-green">▲ {stats['chpk']['new']} New</span> &nbsp;|&nbsp; 
                    <span class="kpi-sub-red">▼ {stats['chpk']['removed']} Removed</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
        # Card 2: Ch.P.S. (Pink)
        with k2:
            st.markdown(f"""
            <div class="kpi-card card-pink">
                <div class="kpi-title">สมาชิก ช.พ.ส. (Ch.P.S.)</div>
                <div class="kpi-value">{stats['chps']['total']:,}</div>
                <div>
                    <span class="kpi-sub-green">▲ {stats['chps']['new']} New</span> &nbsp;|&nbsp; 
                    <span class="kpi-sub-red">▼ {stats['chps']['removed']} Removed</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
        # Charts Row 1: Demographics
        col_g1, col_a1, col_g2, col_a2 = st.columns(4)
        
        # Colors
        teal_scale = [ "#00acc1", "#b2ebf2"]
        pink_scale = [ "#e91e63", "#f8bbd0"]
        
        with col_g1:
            st.markdown("**Ch.P.K. Gender**")
            fig = px.pie(df_gender[df_gender['Type']=="ChPK"], values='Count', names='Group', 
                         color_discrete_sequence=teal_scale, hole=0.4)
            fig.update_layout(margin=dict(t=0, b=0, l=0, r=0), height=150, showlegend=False)
            st.plotly_chart(fig, use_container_width=True)

        with col_a1:
            st.markdown("**Ch.P.K. Age Group**")
            fig = px.bar(df_age[df_age['Type']=="ChPK"], x='Age', y='Count', 
                         color_discrete_sequence=["#00acc1"])
            fig.update_layout(margin=dict(t=0, b=0, l=0, r=0), height=150, xaxis_title=None, yaxis_title=None)
            st.plotly_chart(fig, use_container_width=True)

        with col_g2:
            st.markdown("**Ch.P.S. Gender**")
            fig = px.pie(df_gender[df_gender['Type']=="ChPS"], values='Count', names='Group', 
                         color_discrete_sequence=pink_scale, hole=0.4)
            fig.update_layout(margin=dict(t=0, b=0, l=0, r=0), height=150, showlegend=False)
            st.plotly_chart(fig, use_container_width=True)

        with col_a2:
            st.markdown("**Ch.P.S. Age Group**")
            fig = px.bar(df_age[df_age['Type']=="ChPS"], x='Age', y='Count', 
                         color_discrete_sequence=["#e91e63"])
            fig.update_layout(margin=dict(t=0, b=0, l=0, r=0), height=150, xaxis_title=None, yaxis_title=None)
            st.plotly_chart(fig, use_container_width=True)
            
        # Charts Row 2: Causes of Death
        st.markdown("**Top 5 Causes of Death (5 สาเหตุการเสียชีวิตสูงสุด)**")
        fig_death = px.bar(df_death, x='Count', y='Cause', orientation='h', color='Count', color_continuous_scale='Teal')
        fig_death.update_layout(height=250, margin=dict(t=0, b=20, l=0, r=0))
        st.plotly_chart(fig_death, use_container_width=True)

        st.markdown("---")

        # === Section B: Finance & Budget ===
        st.subheader("💰 การนำส่งเงิน & งบการเงิน (Finance & Budget)")
        
        # Finance Cards
        f1, f2, f3 = st.columns(3)
        with f1:
            st.markdown("""
            <div class="kpi-card card-green">
                <div class="kpi-title">ยอดผู้เสียชีวิต (Death Count)</div>
                <div class="kpi-value">125</div>
                <div class="kpi-sub-green">Active Cases</div>
            </div>
            """, unsafe_allow_html=True)
        with f2:
            st.markdown("""
            <div class="kpi-card card-green">
                <div class="kpi-title">เงินค่าจัดการศพ (Funeral Aid)</div>
                <div class="kpi-value">฿2.5M</div>
                <div class="kpi-sub-green">Disbursed</div>
            </div>
            """, unsafe_allow_html=True)
        with f3:
            st.markdown("""
            <div class="kpi-card card-green">
                <div class="kpi-title">เงินสงเคราะห์ครอบครัว (Family Aid)</div>
                <div class="kpi-value">฿12.8M</div>
                <div class="kpi-sub-green">Processing</div>
            </div>
            """, unsafe_allow_html=True)

        # Finance Charts
        fc1, fc2 = st.columns([1, 2])
        
        with fc1:
            st.markdown("**Payment Status**")
            st.metric(label="Paid on Time", value="92%", delta="2%")
            st.metric(label="Overdue", value="8%", delta="-2%", delta_color="inverse")
            
        with fc2:
            st.markdown("**Payment Rate Trends 2568**")
            df_trend = get_finance_data()
            fig_trend = px.line(df_trend, x='Month', y='Rate', markers=True, line_shape='spline')
            fig_trend.update_traces(line_color='#00acc1', line_width=4)
            fig_trend.update_layout(height=250, yaxis_range=[0, 100])
            st.plotly_chart(fig_trend, use_container_width=True)

    # --- PAGE 2: LEGAL DASHBOARD ---
    elif page == "Legal Dashboard":
        st.markdown("""
        <div class="header-box">
            <h1 class="header-title">ระบบงานนิติการ (Legal Dashboard)</h1>
        </div>
        """, unsafe_allow_html=True)
        
        df_cases, df_workload = get_legal_data()
        
        # KPIs
        l1, l2, l3, l4 = st.columns(4)
        l1.metric("Total Cases", "89")
        l2.metric("Pending", "12", delta="-2", delta_color="inverse")
        l3.metric("Done", "77", delta="2")
        l4.metric("Damages Value", "฿6.7M")
        
        st.markdown("---")
        
        # Charts
        lc1, lc2 = st.columns(2)
        with lc1:
            st.markdown("**Workload by Group**")
            fig_wl = px.bar(df_workload, x="Type", y="Count", color="Type", color_discrete_sequence=px.colors.qualitative.Pastel)
            st.plotly_chart(fig_wl, use_container_width=True)
            
        with lc2:
            st.markdown("**Completion Rate**")
            fig_donut = px.pie(names=["Done", "Pending"], values=[77, 12], hole=0.6, color_discrete_sequence=["#28a745", "#ffc107"])
            st.plotly_chart(fig_donut, use_container_width=True)
            
        # Table
        st.markdown("**Recent Legal Cases**")
        st.dataframe(df_cases, use_container_width=True)

    # --- PAGE 3: ADMIN PANEL (Protected) ---
    elif page == "Admin Control Panel":
        if st.session_state['role'] != "Admin":
            st.error("Access Denied")
        else:
            st.markdown("## 🔒 Admin Control Panel")
            st.info("Manage Platform Users and Permissions")
            
            # Mock User Table
            st.markdown("### User Management")
            user_data = pd.DataFrame({
                "Username": ["admin", "user", "finance_mgr", "legal_lead"],
                "Role": ["Admin", "User", "User", "User"],
                "Last Login": ["Today", "Yesterday", "2 days ago", "Today"],
                "Status": ["Active", "Active", "Active", "Inactive"]
            })
            st.table(user_data)
            
            c1, c2 = st.columns(2)
            with c1: st.button("Add New User")
            with c2: st.button("Reset System Cache")
