import streamlit as st
import os
import base64
import datetime
import time
import pandas as pd
import io
import json # <--- ADD THIS
from utils.styles import load_css
from utils.data_loader import save_and_load_excel, load_from_disk
from utils import auth
from utils import email_service
from utils.logger import log_action # <--- ADD THIS
import extra_streamlit_components as stx

# Import Views
from views import eis, admin, user_management, audit, legal, hospital, strategy, finance, treasury, welfare, dorm, procurement, api_management, admin_system # <--- ADD THIS

# 1. CONFIGURATION
st.set_page_config(page_title="ระบบศูนย์ข้อมูลกลาง สกสค.", layout="wide", page_icon="🏛️")
load_css()
cookie_manager = stx.CookieManager()

# --- HELPER: SHOW ANNOUNCEMENT ---
def show_global_announcement():
    if os.path.exists("data/announcement.json"):
        try:
            with open("data/announcement.json", "r") as f:
                data = json.load(f)
                if data.get("message"):
                    if data['type'] == 'warning': st.warning(f"📢 {data['message']}")
                    elif data['type'] == 'error': st.error(f"📢 {data['message']}")
                    elif data['type'] == 'success': st.success(f"📢 {data['message']}")
                    else: st.info(f"📢 {data['message']}")
        except: pass

# ... (SESSION STATE CODE REMAINS THE SAME) ...
# 2. SESSION STATE
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.role = None
    st.session_state.username = ""
    st.session_state.allowed_views = [] 

if "login_stage" not in st.session_state: st.session_state.login_stage = "credentials" 
if "temp_user_data" not in st.session_state: st.session_state.temp_user_data = {}
if "otp_secret" not in st.session_state: st.session_state.otp_secret = ""
if "current_view" not in st.session_state: st.session_state.current_view = "สำนัก ช.พ.ค. - ช.พ.ส"

# ... (AUTO LOGIN CODE REMAINS THE SAME) ...
# --- AUTO LOGIN ---
if not st.session_state.logged_in:
    try:
        cookie_user = cookie_manager.get(cookie="user_session")
        if cookie_user:
            users = auth.load_users()
            if cookie_user in users:
                user_data = users[cookie_user]
                st.session_state.logged_in = True
                st.session_state.role = user_data["role"]
                st.session_state.username = user_data["name"]
                st.session_state.allowed_views = user_data.get("allowed_views", [])
                
                # LOG AUTO LOGIN
                log_action(user_data["name"], "Auto Login", "Via Cookie") 
                
                time.sleep(0.1)
                st.rerun()
    except Exception as e:
        print(f"Cookie read error: {e}")

# 3. ADMIN VIEWS
# 3.1 UPLOAD VIEW (Updated with Logging)
def show_upload_view():
    st.markdown("## 📂 อัปโหลดข้อมูล (Upload Data)")
    st.info("กรุณาอัปโหลดไฟล์ Excel (.xlsx) เพื่ออัปเดตข้อมูลในระบบ")

    if 'df_eis' not in st.session_state:
        if load_from_disk(): st.session_state['data_loaded'] = True

    uploaded_file = st.file_uploader("ลากและวางไฟล์ที่นี่ (Drag and drop file here)", type=["xlsx"])
    
    if uploaded_file:
        if 'last_loaded_file' not in st.session_state or st.session_state.last_loaded_file != uploaded_file.name:
            with st.spinner("กำลังประมวลผลข้อมูล..."):
                if save_and_load_excel(uploaded_file):
                    st.session_state.last_loaded_file = uploaded_file.name
                    st.session_state['data_loaded'] = True
                    
                    # LOG UPLOAD
                    log_action(st.session_state.username, "Upload Data", f"File: {uploaded_file.name}")
                    
                    st.success("✅ บันทึกข้อมูลเรียบร้อยแล้ว!")
                    time.sleep(1.5)
                    st.rerun()
    
    # ... (Rest of Upload View remains same) ...
    if st.session_state.get('data_loaded', False):
        st.success(f"สถานะข้อมูล: ✅ พร้อมใช้งาน (Source: {st.session_state.get('last_loaded_file', 'Saved File')})")
    else:
        st.warning("สถานะข้อมูล: ⚠️ ยังไม่มีข้อมูลในระบบ")

    st.write("---")
    st.markdown("### 🔄 แก้ไขปัญหา (Troubleshooting)")
    st.caption("หากข้อมูลกราฟไม่ขึ้น หรือแสดง Error ว่า Missing Column ให้กดปุ่มนี้เพื่อบังคับโหลดข้อมูลใหม่")
    
    if st.button("🔄 บังคับโหลดข้อมูลใหม่ (Force Refresh)", type="primary"):
        with st.spinner("กำลังล้างค่าและโหลดข้อมูลใหม่..."):
            st.cache_data.clear()
            keys_to_clear = ['df_eis', 'df_eis_extra', 'df_procure', 'df_strategy', 'df_finance', 'df_treasury', 'df_welfare', 'df_dorm', 'df_hospital', 'df_legal', 'df_audit', 'df_admin', 'data_loaded']
            for k in keys_to_clear:
                if k in st.session_state: del st.session_state[k]

            if load_from_disk():
                st.session_state['data_loaded'] = True
                
                # LOG REFRESH
                log_action(st.session_state.username, "Force Refresh", "Cleared Cache")
                
                st.success("✅ โหลดข้อมูลใหม่สำเร็จ!")
                time.sleep(1)
                st.rerun()
            else:
                st.error("❌ ไม่พบไฟล์ข้อมูลในระบบ")

# ... (DOWNLOAD VIEW REMAINS SAME) ...
# 3.2 DOWNLOAD VIEW
def show_download_view():
    st.markdown("## 📥 ดาวน์โหลดข้อมูล (Download Data)")
    st.info("เลือกชุดข้อมูลที่ต้องการดาวน์โหลดเป็นไฟล์ CSV หรือ Excel")

    dataset_map = {
        "EIS Data (Member Stats)": "df_eis",
        "EIS Extra (Death/Finance)": "df_eis_extra",
        "Strategy Data (นโยบาย/แผน)": "df_strategy",
        "Procurement Data (พัสดุ)": "df_procure",
        "Finance Data (บัญชี)": "df_finance",
        "Treasury Data (การเงิน)": "df_treasury",
        "Welfare Data (สวัสดิการ)": "df_welfare",
        "Dorm Data (หอพัก)": "df_dorm",
        "Hospital Data (รพ.ครู)": "df_hospital",
        "Legal Data (นิติการ)": "df_legal",
        "Audit Data (ตรวจสอบภายใน)": "df_audit",
        "Admin Data (อำนวยการ)": "df_admin"
    }

    selected_dataset_name = st.selectbox("เลือกชุดข้อมูล (Select Dataset)", list(dataset_map.keys()))
    session_key = dataset_map[selected_dataset_name]

    if session_key in st.session_state and isinstance(st.session_state[session_key], pd.DataFrame) and not st.session_state[session_key].empty:
        df = st.session_state[session_key]
        st.write(f"**ตัวอย่างข้อมูล ({len(df)} แถว):**")
        st.dataframe(df.head(5), use_container_width=True)
        col1, col2 = st.columns(2)
        with col1:
            csv = df.to_csv(index=False).encode('utf-8-sig')
            if st.download_button("📄 ดาวน์โหลดเป็น CSV", csv, f"{session_key}.csv", "text/csv", use_container_width=True):
                 log_action(st.session_state.username, "Download CSV", session_key)
        with col2:
            try:
                buffer = io.BytesIO()
                with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
                    df.to_excel(writer, index=False, sheet_name='Sheet1')
                if st.download_button("📊 ดาวน์โหลดเป็น Excel", buffer, f"{session_key}.xlsx", "application/vnd.ms-excel", use_container_width=True):
                    log_action(st.session_state.username, "Download Excel", session_key)
            except Exception as e:
                 st.error(f"Excel Error: {e} (Try installing xlsxwriter)")
    else:
        st.warning(f"⚠️ ไม่พบข้อมูลสำหรับชุดข้อมูลนี้ ({session_key}) กรุณาอัปโหลดไฟล์ก่อน")

# 4. LOGIN PAGE (Updated with Logging)
def login_page():
    # ... (Logo Code Remains Same) ...
    st.markdown("<br><br>", unsafe_allow_html=True)
    LOGO_FILENAME = "image_11b1c9.jpg"
    logo_path = "assets/" + LOGO_FILENAME
    if not os.path.exists(logo_path): logo_path = LOGO_FILENAME

    if os.path.exists(logo_path):
        try:
            with open(logo_path, "rb") as f:
                encoded = base64.b64encode(f.read()).decode()
            st.markdown(f"""<div style="display: flex; justify-content: center; align-items: center; margin-bottom: 10px;"><img src="data:image/jpeg;base64,{encoded}" style="width: 150px; max-width: 80%; border-radius: 50%;"></div>""", unsafe_allow_html=True)
        except Exception as e: st.error(f"Error loading logo: {e}")
    else: st.markdown("<h1 style='text-align:center; font-size: 80px;'>🏛️</h1>", unsafe_allow_html=True)
    
    st.markdown("""<h1 style='text-align: center; margin-bottom: 0px; font-weight: bold;'>ยินดีต้อนรับ</h1><h3 style='text-align: center; margin-top: 5px; margin-bottom: 30px; font-weight: normal;'>ระบบศูนย์ข้อมูลกลาง สกสค.</h3>""", unsafe_allow_html=True)
    
    c1, c2, c3 = st.columns([1, 1.2, 1])
    with c2:
        if st.session_state.login_stage == "credentials":
            st.caption("⚠️ **กรุณาเข้าสู่ระบบด้วยรหัสผ่าน**")
            user = st.text_input("ชื่อผู้ใช้ (Username)")
            pw = st.text_input("รหัสผ่าน (Password)", type="password")
            remember = st.checkbox("จำรหัสผ่านไว้ 10 วัน (Remember me)")
            
            if st.button("ถัดไป (Next)", use_container_width=True):
                user_data = auth.check_credentials(user, pw)
                if user_data:
                    otp = email_service.generate_otp()
                    user_email = user_data.get('email', '')
                    if not user_email or "@" not in user_email:
                        st.error("❌ บัญชีนี้ยังไม่ได้ระบุอีเมล กรุณาติดต่อ Admin")
                    else:
                        email_service.send_otp_email(user_email, otp)
                        st.info(f"🔑 **TEST MODE OTP:** {otp}") 
                        st.session_state.temp_user_data = user_data
                        st.session_state.temp_user_data['remember'] = remember
                        st.session_state.otp_secret = otp
                        st.session_state.login_stage = "otp"
                        time.sleep(5) 
                        st.rerun()
                else: 
                    st.error("❌ ชื่อผู้ใช้หรือรหัสผ่านไม่ถูกต้อง")
                    log_action(user, "Login Failed", "Bad Credentials") # LOG FAILED LOGIN

        elif st.session_state.login_stage == "otp":
            st.warning(f"🔑 **TEST CODE:** {st.session_state.otp_secret}")
            st.info(f"📧 กรุณากรอกรหัส 6 หลักที่ส่งไปยัง {st.session_state.temp_user_data.get('email')}")
            otp_input = st.text_input("รหัส OTP", max_chars=6)
            c_back, c_conf = st.columns(2)
            with c_back:
                if st.button("ย้อนกลับ", use_container_width=True):
                    st.session_state.login_stage = "credentials"
                    st.rerun()
            with c_conf:
                if st.button("ยืนยัน (Verify)", type="primary", use_container_width=True):
                    if otp_input == st.session_state.otp_secret:
                        user_data = st.session_state.temp_user_data
                        st.session_state.logged_in = True
                        st.session_state.role = user_data["role"]
                        st.session_state.username = user_data["name"]
                        st.session_state.allowed_views = user_data.get("allowed_views", [])
                        
                        # LOG SUCCESS LOGIN
                        log_action(user_data["name"], "Login Success", "Via OTP")
                        
                        if user_data.get('remember'):
                            expires = datetime.datetime.now() + datetime.timedelta(days=10)
                            cookie_manager.set("user_session", user_data['username'], expires_at=expires)
                        st.session_state.login_stage = "credentials"
                        st.session_state.otp_secret = ""
                        st.rerun()
                    else: st.error("❌ รหัส OTP ไม่ถูกต้อง")

# 5. MAIN ROUTER & SIDEBAR
if not st.session_state.logged_in:
    login_page()
else:
    # --- SHOW ANNOUNCEMENT ---
    show_global_announcement()

    st.sidebar.title(f"👤 {st.session_state.username}")
    st.sidebar.caption(f"Role: {st.session_state.role}")
    st.sidebar.divider()

    # --- DEFINE MENUS ---
    dashboard_map = {
        "สำนัก ช.พ.ค. - ช.พ.ส": eis.show_view,
        "สำนักการคลัง - กลุ่มการเงิน": treasury.show_view,
        "สำนักการคลัง - กลุ่มการพัสดุและอาคารสถานที่": procurement.show_view,
        "สำนักการคลัง - กลุ่มบัญชี": finance.show_view,
        "สำนักนโยบาย และยุทธศาสตร์": strategy.show_view,
        "โรงพยาบาลครู": hospital.show_view,
        "สำนักสวัสดิการ": welfare.show_view,
        "หอพัก สกสค.": dorm.show_view,
        "สำนักอำนวยการ": admin.show_view,
        "หน่วยตรวจสอบภายใน": audit.show_view,
        "สำนักนิติการ": legal.show_view,
    }

    available_dashboards = {}
    if st.session_state.role in ["Admin", "Superuser"]:
        available_dashboards = dashboard_map
    else:
        for name, func in dashboard_map.items():
            if name in st.session_state.allowed_views:
                available_dashboards[name] = func

    admin_map = {
        "⚙️ จัดการผู้ใช้งาน (Users)": user_management.show_view,
        "🛠️ ตั้งค่าระบบ (System)": admin_system.show_view, # <--- NEW MENU
        "🔌 จัดการ API (API Keys)": api_management.show_view,
        "📂 อัปโหลดข้อมูล (Upload)": show_upload_view,
        "📥 ดาวน์โหลดข้อมูล (Download)": show_download_view
    }

    # --- RENDER SIDEBAR ---
    st.sidebar.markdown("### 📊 เมนู Dashboard")
    for name in available_dashboards.keys():
        if st.sidebar.button(name, use_container_width=True, type="primary" if st.session_state.current_view == name else "secondary"):
            st.session_state.current_view = name
            st.rerun()

    if st.session_state.role == "Admin":
        st.sidebar.markdown("---")
        st.sidebar.markdown("### ⚙️ เมนูการจัดการ")
        for name in admin_map.keys():
            if st.sidebar.button(name, use_container_width=True, type="primary" if st.session_state.current_view == name else "secondary"):
                st.session_state.current_view = name
                st.rerun()
        
        st.sidebar.markdown("---")
        if st.sidebar.button("🚪 ออกจากระบบ (Log off)", use_container_width=True, type="secondary"):
            log_action(st.session_state.username, "Logout", "User Initiated") # LOG LOGOUT
            st.session_state.logged_in = False
            st.session_state.role = None
            st.session_state.allowed_views = []
            st.session_state.login_stage = "credentials" 
            try: cookie_manager.delete("user_session")
            except: pass
            time.sleep(0.1) 
            st.rerun()

    elif st.sidebar.button("🚪 ออกจากระบบ (Log off)", use_container_width=True):
        log_action(st.session_state.username, "Logout", "User Initiated") # LOG LOGOUT
        st.session_state.logged_in = False
        st.session_state.role = None
        st.session_state.allowed_views = []
        st.session_state.login_stage = "credentials"
        try: cookie_manager.delete("user_session")
        except: pass
        time.sleep(0.1) 
        st.rerun()

    # --- RENDER MAIN CONTENT ---
    if 'df_eis' not in st.session_state: load_from_disk()

    if st.session_state.current_view in available_dashboards:
        available_dashboards[st.session_state.current_view]()
    elif st.session_state.current_view in admin_map and st.session_state.role == "Admin":
        admin_map[st.session_state.current_view]()
    else:
        if available_dashboards:
            st.session_state.current_view = list(available_dashboards.keys())[0]
            st.rerun()
