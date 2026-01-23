import streamlit as st
import pandas as pd
import os
import json
from utils.logger import get_logs, log_action, clear_logs

ANNOUNCEMENT_FILE = "data/announcement.json"

def save_announcement(message, type_):
    with open(ANNOUNCEMENT_FILE, "w") as f:
        json.dump({"message": message, "type": type_}, f)

def get_announcement():
    if os.path.exists(ANNOUNCEMENT_FILE):
        with open(ANNOUNCEMENT_FILE, "r") as f:
            return json.load(f)
    return None

def show_view():
    st.title("🛠️ ตั้งค่าระบบ & บันทึกการใช้งาน (System Config)")

    tab1, tab2 = st.tabs(["📢 ประกาศข่าวสาร (Announcement)", "📝 บันทึกการใช้งาน (Audit Logs)"])

    # --- TAB 1: ANNOUNCEMENT ---
    with tab1:
        st.subheader("ตั้งค่าประกาศข้อความ (Global Banner)")
        st.info("ข้อความนี้จะแสดงที่ส่วนบนสุดของหน้าจอผู้ใช้งานทุกคน")
        
        current = get_announcement()
        default_msg = current['message'] if current else ""
        default_type = current['type'] if current else "info"

        with st.form("announce_form"):
            msg_input = st.text_input("ข้อความประกาศ", value=default_msg)
            type_input = st.selectbox("ประเภทกล่องข้อความ", ["info", "warning", "error", "success"], index=["info", "warning", "error", "success"].index(default_type))
            
            c1, c2 = st.columns(2)
            submitted = c1.form_submit_button("💾 บันทึกประกาศ")
            cleared = c2.form_submit_button("🗑️ ลบประกาศ")

            if submitted:
                save_announcement(msg_input, type_input)
                log_action(st.session_state.username, "Update Announcement", f"Set: {msg_input}")
                st.success("บันทึกเรียบร้อย!")
                st.rerun()
            
            if cleared:
                if os.path.exists(ANNOUNCEMENT_FILE):
                    os.remove(ANNOUNCEMENT_FILE)
                    log_action(st.session_state.username, "Clear Announcement", "Removed banner")
                    st.success("ลบประกาศแล้ว!")
                    st.rerun()

    # --- TAB 2: AUDIT LOGS ---
    with tab2:
        c_head, c_btn = st.columns([5, 1])
        with c_head:
            st.subheader("ประวัติการใช้งานระบบ")
        with c_btn:
             # CLEAR LOGS BUTTON
            if st.button("🗑️ ล้างประวัติ (Clear)", type="secondary", use_container_width=True):
                clear_logs()
                # Create a new log entry immediately after clearing
                log_action(st.session_state.username, "Clear Logs", "Admin cleared all audit logs")
                st.success("ล้างประวัติเรียบร้อย!")
                st.rerun()

        df_logs = get_logs()
        
        if not df_logs.empty:
            st.dataframe(df_logs, use_container_width=True, hide_index=True)
            
            # Export
            csv = df_logs.to_csv(index=False).encode('utf-8-sig')
            st.download_button("📥 ดาวน์โหลด Logs (.csv)", csv, "system_logs.csv", "text/csv")
        else:
            st.info("ยังไม่มีประวัติการใช้งาน")
