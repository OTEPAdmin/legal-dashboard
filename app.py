# ... (Previous code in app.py remains the same until the MAIN ROUTER section) ...

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
        "🛠️ ตั้งค่าระบบ (System)": admin_system.show_view,
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
            log_action(st.session_state.username, "Logout", "User Initiated")
            st.session_state.logged_in = False
            st.session_state.role = None
            st.session_state.allowed_views = []
            st.session_state.login_stage = "credentials" 
            try: cookie_manager.delete("user_session")
            except: pass
            time.sleep(0.1) 
            st.rerun()

    elif st.sidebar.button("🚪 ออกจากระบบ (Log off)", use_container_width=True):
        log_action(st.session_state.username, "Logout", "User Initiated")
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

    # --- ANALYTICS TRACKING ---
    # Log only when the view changes to avoid spamming logs
    if 'last_view_logged' not in st.session_state:
        st.session_state.last_view_logged = None

    if st.session_state.current_view != st.session_state.last_view_logged:
        log_action(st.session_state.username, "View Dashboard", st.session_state.current_view)
        st.session_state.last_view_logged = st.session_state.current_view
    # --------------------------

    if st.session_state.current_view in available_dashboards:
        available_dashboards[st.session_state.current_view]()
    elif st.session_state.current_view in admin_map and st.session_state.role == "Admin":
        admin_map[st.session_state.current_view]()
    else:
        if available_dashboards:
            st.session_state.current_view = list(available_dashboards.keys())[0]
            st.rerun()
