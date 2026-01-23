import streamlit as st
import pandas as pd
import time
from utils import auth
from utils.styles import render_header

def show_view():
    render_header("👤 User Management (จัดการผู้ใช้งาน)", border_color="#FF9800")

    users = auth.load_users()

    DASHBOARD_OPTIONS = [
        "บทสรุปผู้บริหาร", "สำนักการคลัง", "กองคลัง-พัสดุ", "ภาพรวมฐานะการเงิน",
        "กลุ่มนโยบายและยุทธศาสตร์", "โรงพยาบาล", "สวัสดิการ", "หอพัก สกสค.",
        "สำนักอำนวยการ", "สำนักตรวจสอบภายใน", "สำนักนิติการ"
    ]

    tab1, tab2, tab3, tab4 = st.tabs(["📋 รายชื่อผู้ใช้", "➕ เพิ่มผู้ใช้ใหม่", "✏️ แก้ไขสิทธิ์ (Edit)", "🔑 เปลี่ยนรหัสผ่าน"])

    # --- TAB 1: USER LIST ---
    with tab1:
        data = []
        for u, details in users.items():
            views_str = "All" if details['role'] in ['Admin', 'Superuser'] else ", ".join(details.get('allowed_views', []))
            data.append({
                "Username": u,
                "Name": details['name'],
                "Role": details['role'],
                "Email": details.get('email', '-'),
                "Assigned Dashboards": views_str
            })
        
        st.dataframe(pd.DataFrame(data), use_container_width=True, hide_index=True)

        st.write("---")
        c1, c2 = st.columns([3, 1])
        with c1:
            user_to_del = st.selectbox("เลือกผู้ใช้ที่ต้องการลบ", list(users.keys()))
        with c2:
            st.write("") 
            st.write("") 
            if st.button("ลบผู้ใช้ (Delete)", type="primary"):
                success, msg = auth.delete_user(user_to_del)
                if success:
                    st.success(msg)
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error(msg)

    # --- TAB 2: ADD NEW USER ---
    with tab2:
        st.markdown("#### สร้างบัญชีใหม่")
        col1, col2 = st.columns(2)
        with col1:
            new_user = st.text_input("Username (ชื่อผู้ใช้)", placeholder="e.g. staff01")
            new_name = st.text_input("Display Name (ชื่อที่แสดง)", placeholder="e.g. Somchai Jai-dee")
            new_email = st.text_input("Email (อีเมล)", placeholder="user@example.com")
        with col2:
            new_pass = st.text_input("Password (รหัสผ่าน)", type="password")
            new_role = st.selectbox("Role (สิทธิ์)", ["User", "Superuser", "Admin"])
        
        selected_views = []
        if new_role == "User":
            st.markdown("**Select Assigned Dashboards:**")
            selected_views = st.multiselect("Dashboards", DASHBOARD_OPTIONS, default=DASHBOARD_OPTIONS[:1])
        
        if st.button("บันทึก (Create Account)"):
            if new_user and new_pass and new_name and new_email:
                success, msg = auth.add_user(new_user, new_pass, new_role, new_name, new_email, selected_views)
                if success:
                    st.success(f"✅ บันทึกสำเร็จ: {msg}")
                    time.sleep(1.5)
                    st.rerun()
                else:
                    st.warning(msg)
            else:
                st.warning("⚠️ กรุณากรอกข้อมูลให้ครบถ้วน")

    # --- TAB 3: EDIT EXISTING USER (NEW!) ---
    with tab3:
        st.markdown("#### แก้ไขข้อมูลและสิทธิ์การเข้าถึง")
        
        # Select User to Edit
        edit_user_key = st.selectbox("เลือกผู้ใช้ที่ต้องการแก้ไข", list(users.keys()), key="edit_user_select")
        
        if edit_user_key:
            current_data = users[edit_user_key]
            
            # Pre-fill Form
            with st.form("edit_user_form"):
                e_c1, e_c2 = st.columns(2)
                with e_c1:
                    # Username is read-only usually, or just display it
                    st.text_input("Username", value=edit_user_key, disabled=True)
                    e_name = st.text_input("Display Name", value=current_data.get("name", ""))
                    e_email = st.text_input("Email", value=current_data.get("email", ""))
                
                with e_c2:
                    # Role Selection
                    roles = ["User", "Superuser", "Admin"]
                    current_role_idx = roles.index(current_data["role"]) if current_data["role"] in roles else 0
                    e_role = st.selectbox("Role", roles, index=current_role_idx)
                
                # Dashboards (Only show if Role is User)
                e_views = []
                if e_role == "User":
                    current_views = current_data.get("allowed_views", [])
                    # Filter only valid options incase options changed
                    valid_defaults = [v for v in current_views if v in DASHBOARD_OPTIONS]
                    st.markdown("**Assigned Dashboards:**")
                    e_views = st.multiselect("Dashboards", DASHBOARD_OPTIONS, default=valid_defaults)
                
                submitted = st.form_submit_button("บันทึกการแก้ไข (Update User)")
                
                if submitted:
                    success, msg = auth.update_user_details(edit_user_key, e_role, e_name, e_email, e_views)
                    if success:
                        st.success(msg)
                        time.sleep(1.5)
                        st.rerun()
                    else:
                        st.error(msg)

    # --- TAB 4: CHANGE PASSWORD ---
    with tab4:
        st.markdown("#### เปลี่ยนรหัสผ่าน")
        col1, col2 = st.columns(2)
        with col1:
            target_user = st.selectbox("เลือกผู้ใช้", list(users.keys()), key="pwd_user_select")
        with col2:
            new_pwd = st.text_input("รหัสผ่านใหม่", type="password", key="pwd_new")
        
        if st.button("อัปเดตรหัสผ่าน"):
            if new_pwd:
                success, msg = auth.update_password(target_user, new_pwd)
                if success:
                    st.success(msg)
                else:
                    st.error(msg)
            else:
                st.warning("⚠️ กรุณากรอกรหัสผ่านใหม่")
