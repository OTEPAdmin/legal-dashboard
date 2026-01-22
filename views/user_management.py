import streamlit as st
import pandas as pd
from utils import auth
from utils.styles import render_header

def show_view():
    render_header("👤 User Management (จัดการผู้ใช้งาน)", border_color="#FF9800")

    # Load current users
    users = auth.load_users()

    # --- TABS ---
    tab1, tab2, tab3 = st.tabs(["📋 รายชื่อผู้ใช้ (User List)", "➕ เพิ่มผู้ใช้ใหม่ (Add User)", "🔑 เปลี่ยนรหัสผ่าน (Change Password)"])

    # TAB 1: LIST USERS
    with tab1:
        # Convert JSON to DataFrame for display
        data = []
        for u, details in users.items():
            data.append({
                "Username": u,
                "Name": details['name'],
                "Role": details['role']
            })
        
        df = pd.DataFrame(data)
        st.dataframe(df, use_container_width=True, hide_index=True)

        st.write("---")
        st.caption("🗑️ **Delete User**")
        c1, c2 = st.columns([3, 1])
        with c1:
            user_to_del = st.selectbox("เลือกผู้ใช้ที่ต้องการลบ (Select User to Delete)", list(users.keys()))
        with c2:
            st.write("") # Spacer
            st.write("") # Spacer
            if st.button("ลบผู้ใช้ (Delete)", type="primary"):
                success, msg = auth.delete_user(user_to_del)
                if success:
                    st.success(msg)
                    st.rerun()
                else:
                    st.error(msg)

    # TAB 2: ADD USER
    with tab2:
        st.markdown("#### สร้างบัญชีใหม่")
        col1, col2 = st.columns(2)
        with col1:
            new_user = st.text_input("Username (ชื่อผู้ใช้)", placeholder="e.g. staff01")
            new_name = st.text_input("Display Name (ชื่อที่แสดง)", placeholder="e.g. Somchai Jai-dee")
        with col2:
            new_pass = st.text_input("Password (รหัสผ่าน)", type="password")
            new_role = st.selectbox("Role (สิทธิ์)", ["User", "Admin"])
        
        if st.button("บันทึก (Create Account)"):
            if new_user and new_pass and new_name:
                success, msg = auth.add_user(new_user, new_pass, new_role, new_name)
                if success:
                    st.success(msg)
                    st.rerun() # Refresh to update list
                else:
                    st.warning(msg)
            else:
                st.warning("⚠️ กรุณากรอกข้อมูลให้ครบถ้วน")

    # TAB 3: CHANGE PASSWORD
    with tab3:
        st.markdown("#### เปลี่ยนรหัสผ่าน")
        col1, col2 = st.columns(2)
        with col1:
            target_user = st.selectbox("เลือกผู้ใช้ (Select User)", list(users.keys()), key="pwd_user_select")
        with col2:
            new_pwd = st.text_input("รหัสผ่านใหม่ (New Password)", type="password", key="pwd_new")
        
        if st.button("อัปเดตรหัสผ่าน (Update Password)"):
            if new_pwd:
                success, msg = auth.update_password(target_user, new_pwd)
                if success:
                    st.success(msg)
                else:
                    st.error(msg)
            else:
                st.warning("⚠️ กรุณากรอกรหัสผ่านใหม่")
