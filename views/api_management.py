import streamlit as st
import json
import os
import uuid
import datetime
from utils.styles import render_header

KEYS_FILE = "api_keys.json"

def load_keys():
    if not os.path.exists(KEYS_FILE):
        return {}
    with open(KEYS_FILE, "r") as f:
        return json.load(f)

def save_keys(keys):
    with open(KEYS_FILE, "w") as f:
        json.dump(keys, f, indent=4)

def generate_new_key(name):
    keys = load_keys()
    new_api_key = f"otep-{uuid.uuid4().hex[:16]}"
    keys[new_api_key] = {
        "name": name,
        "created_at": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "status": "active"
    }
    save_keys(keys)
    return new_api_key

def revoke_key(api_key):
    keys = load_keys()
    if api_key in keys:
        del keys[api_key]
        save_keys(keys)

def show_view():
    render_header("🔌 API Management (จัดการการเชื่อมต่อ)", border_color="#607D8B")

    st.info("หน้านี้สำหรับสร้าง API Key เพื่อให้ระบบภายนอก (Mobile App, Web, ERP) สามารถดึงข้อมูลจาก Dashboard ไปใช้งานได้")

    st.markdown("### ➕ สร้าง API Key ใหม่ (Generate Key)")
    
    # --- SECTION 1: CREATE KEY (No Expander) ---
    c1, c2 = st.columns([3, 1])
    with c1:
        system_name = st.text_input("ชื่อระบบที่เชื่อมต่อ (System Name)", placeholder="e.g. Mobile App, ERP, Website")
    with c2:
        st.write("") 
        st.write("") 
        if st.button("Generate Key", type="primary", use_container_width=True):
            if system_name:
                new_key = generate_new_key(system_name)
                st.success(f"✅ สร้างสำเร็จ! กรุณาคัดลอก Key นี้ทันที: `{new_key}`")
                st.rerun()
            else:
                st.warning("กรุณาระบุชื่อระบบ")

    st.write("---")

    # --- SECTION 2: ACTIVE KEYS ---
    st.subheader("🔑 Active API Keys")
    keys = load_keys()

    if not keys:
        st.caption("No active API keys.")
    else:
        # Header
        c1, c2, c3, c4 = st.columns([3, 3, 2, 1])
        c1.markdown("**System Name**")
        c2.markdown("**API Key**")
        c3.markdown("**Created**")
        c4.markdown("**Action**")
        
        for k, v in keys.items():
            c1, c2, c3, c4 = st.columns([3, 3, 2, 1])
            c1.write(v['name'])
            c2.code(k)
            c3.write(v['created_at'])
            if c4.button("Revoke", key=k):
                revoke_key(k)
                st.rerun()

    st.write("---")
    
    # --- SECTION 3: API DOCS ---
    st.subheader("📘 วิธีการใช้งาน (Documentation)")
    st.markdown("""
    **Endpoint Base URL:** `http://YOUR-SERVER-IP:8000`
    
    **Header Required:**
    - `X-API-KEY`: *<Your-Generated-Key>*
    
    **Example Python Code:**
    """)
    
    example_code = """import requests

url = "http://localhost:8000/api/v1/eis"
headers = {
    "X-API-KEY": "Put-Your-Key-Here"
}

response = requests.get(url, headers=headers)
print(response.json())
"""
    st.code(example_code, language="python")
