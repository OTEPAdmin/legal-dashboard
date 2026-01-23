import streamlit as st
import pandas as pd
import os
import json
import plotly.express as px
from utils.logger import get_logs, log_action, clear_logs
from utils.config_manager import load_visibility_settings, save_visibility_settings # <--- IMPORT NEW UTILS

ANNOUNCEMENT_FILE = "data/announcement.json"

# ... (Previous helper functions remain the same) ...
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

    tab1, tab2, tab3, tab4 = st.tabs(["📢 ประกาศข่าวสาร", "📝 บันทึกการใช้งาน", "📊 สถิติ", "👁️ จัดการการแสดงผล (Visibility)"])

    # ... (TAB 1, TAB 2, TAB 3 code remains exactly the same) ...
    # Copy existing code for tabs 1-3 here if replacing file, 
    # OR just append Tab 4 below if editing manually.
    
    # --- TAB 1: ANNOUNCEMENT ---
    with tab1:
        st.subheader("ตั้งค่าประกาศข้อความ (Global Banner)")
        current = get_announcement()
        default_msg = current['message'] if current else ""
        default_type = current['type'] if current else "info"

        with st.form("announce_form"):
            msg_input = st.text_input("ข้อความประกาศ", value=default_msg)
            type_input = st.selectbox("ประเภทกล่องข้อความ", ["info", "warning", "error", "success"], index=["info", "warning", "error", "success"].index(default_type))
            if st.form_submit_button("💾 บันทึกประกาศ"):
                save_announcement(msg_input, type_input)
                log_action(st.session_state.username, "Update Announcement", f"Set: {msg_input}")
                st.success("บันทึกเรียบร้อย!")
                st.rerun()

    # --- TAB 2: LOGS ---
    with tab2:
        if st.button("🗑️ ล้างประวัติ (Clear)"):
            clear_logs()
            st.rerun()
        st.dataframe(get_logs(), use_container_width=True)

    # --- TAB 3: ANALYTICS ---
    with tab3:
        st.write("📊 (Analytics View from previous step)")
    
    # --- TAB 4: VISIBILITY (NEW) ---
    with tab4:
        st.subheader("👁️ ซ่อน/แสดง Dashboard และกราฟ")
        st.info("Admins จะมองเห็นทุกหน้าเสมอ (แต่จะมีสัญลักษณ์ 🚫) ส่วน User ทั่วไปจะไม่เห็นหน้าที่ถูกซ่อน")

        # Load Current Settings
        settings = load_visibility_settings()
        
        # 1. DASHBOARD VISIBILITY
        st.markdown("##### 📂 เลือก Dashboard ที่ต้องการเผยแพร่")
        
        # List of all known dashboards (Hardcoded list to ensure they appear even if not in config yet)
        all_dashboards = [
            "สำนัก ช.พ.ค. - ช.พ.ส", "สำนักการคลัง - กลุ่มการเงิน", "สำนักการคลัง - กลุ่มการพัสดุและอาคารสถานที่",
            "สำนักการคลัง - กลุ่มบัญชี", "สำนักนโยบาย และยุทธศาสตร์", "โรงพยาบาลครู",
            "สำนักสวัสดิการ", "หอพัก สกสค.", "สำนักอำนวยการ", "หน่วยตรวจสอบภายใน", "สำนักนิติการ"
        ]

        with st.form("viz_dash_form"):
            col_a, col_b = st.columns(2)
            updated_dashboards = settings["dashboards"].copy()
            
            for i, name in enumerate(all_dashboards):
                # Default to True (Visible) if not set
                is_checked = updated_dashboards.get(name, True)
                col = col_a if i % 2 == 0 else col_b
                # Toggle
                new_state = col.toggle(f"{name}", value=is_checked)
                updated_dashboards[name] = new_state
            
            st.write("---")
            st.markdown("##### 📊 เลือกกราฟ/ส่วนย่อย (Graph Sections)")
            
            updated_features = settings["features"].copy()
            feat_map = {
                "EIS_Executive_Summary": "บทสรุปผู้บริหาร (EIS)",
                "EIS_Demographics": "ข้อมูลสมาชิก (EIS)",
                "EIS_Death_Stats": "สาเหตุการเสียชีวิต (EIS)",
                "EIS_Financials": "การเงิน & นำส่ง (EIS)"
            }
            
            for key, label in feat_map.items():
                is_checked = updated_features.get(key, True)
                new_state = st.toggle(f"{label}", value=is_checked)
                updated_features[key] = new_state

            if st.form_submit_button("💾 บันทึกการตั้งค่า (Save Visibility)"):
                settings["dashboards"] = updated_dashboards
                settings["features"] = updated_features
                save_visibility_settings(settings)
                log_action(st.session_state.username, "Update Visibility", "Changed show/hide settings")
                st.success("บันทึกเรียบร้อย! (Settings Saved)")
                time.sleep(1)
                st.rerun()
