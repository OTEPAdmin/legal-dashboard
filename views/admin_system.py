import streamlit as st
import pandas as pd
import os
import json
import plotly.express as px
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

    tab1, tab2, tab3 = st.tabs(["📢 ประกาศข่าวสาร", "📝 บันทึกการใช้งาน (Logs)", "📊 สถิติการใช้งาน (Analytics)"])

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
            if st.button("🗑️ ล้างประวัติ (Clear)", type="secondary", use_container_width=True):
                clear_logs()
                log_action(st.session_state.username, "Clear Logs", "Admin cleared all audit logs")
                st.success("ล้างประวัติเรียบร้อย!")
                st.rerun()

        df_logs = get_logs()
        
        if not df_logs.empty:
            st.dataframe(df_logs, use_container_width=True, hide_index=True)
            csv = df_logs.to_csv(index=False).encode('utf-8-sig')
            st.download_button("📥 ดาวน์โหลด Logs (.csv)", csv, "system_logs.csv", "text/csv")
        else:
            st.info("ยังไม่มีประวัติการใช้งาน")

    # --- TAB 3: ANALYTICS ---
    with tab3:
        st.subheader("📈 สถิติการเข้าใช้งาน (Usage Analytics)")
        df_logs = get_logs()

        if not df_logs.empty:
            df_views = df_logs[df_logs['Action'] == 'View Dashboard']

            if not df_views.empty:
                col_a, col_b = st.columns(2)

                # Chart 1: Most Visited Dashboards
                with col_a:
                    st.markdown("##### 🏆 หน้าจอที่ถูกใช้งานสูงสุด")
                    top_dash = df_views['Details'].value_counts().reset_index()
                    top_dash.columns = ['Dashboard', 'Visits']
                    
                    fig_dash = px.bar(top_dash, x='Visits', y='Dashboard', orientation='h', text='Visits',
                                      color='Visits', color_continuous_scale='Blues')
                    fig_dash.update_layout(yaxis=dict(autorange="reversed"), showlegend=False, height=350)
                    st.plotly_chart(fig_dash, use_container_width=True)

                # Chart 2: Most Active Users
                with col_b:
                    st.markdown("##### 👤 ผู้ใช้งานที่มีกิจกรรมสูงสุด")
                    top_users = df_views['User'].value_counts().reset_index()
                    top_users.columns = ['User', 'Visits']
                    
                    fig_users = px.bar(top_users, x='User', y='Visits', text='Visits',
                                       color='Visits', color_continuous_scale='Greens')
                    fig_users.update_layout(height=350)
                    st.plotly_chart(fig_users, use_container_width=True)
                
                # Table: Recent Activity
                st.markdown("##### 🕒 การเข้าใช้งานล่าสุด")
                st.dataframe(df_views[['Timestamp', 'User', 'Details']].head(10), use_container_width=True, hide_index=True)

            else:
                st.info("ยังไม่มีข้อมูลการเข้าชม Dashboard (No view data recorded yet)")
        else:
            st.info("ยังไม่มีข้อมูลในระบบ Log")
