import streamlit as st
import base64
import os

# Point to the new assets folder
LOGO_FILENAME = "assets/image_11b1c9.jpg"

def load_css():
    st.markdown("""
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Kanit:wght@300;400;500;700&display=swap');

            /* Global Font Force */
            html, body, [class*="css"], .stMarkdown, .stButton, .stTextField, 
            .stNumberInput, .stSelectbox, .stMetric, .stRadio, .stSidebar, 
            label, div, span, p, h1, h2, h3, h4, h5, h6 {
                font-family: 'Kanit', sans-serif !important;
            }

            /* Login & Layout Styles */
            .login-box { background-color: white; padding: 40px; border-radius: 10px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); max-width: 400px; width: 100%; margin: 0 auto; border-top: 5px solid #E91E63; }
            .header-container { display: flex; justify-content: space-between; align-items: center; background-color: #F5F5F5; padding: 15px; border-radius: 5px; margin-bottom: 20px; border-left: 5px solid #607D8B; }

            /* Card Styles */
            .card-cpk { background-color: white; border-radius: 10px; padding: 15px; box-shadow: 0 2px 5px rgba(0,0,0,0.05); text-align: center; height: 100%; border-top: 6px solid #00ACC1; }
            .card-cps { background-color: white; border-radius: 10px; padding: 15px; box-shadow: 0 2px 5px rgba(0,0,0,0.05); text-align: center; height: 100%; border-top: 6px solid #8E24AA; }
            .rev-card-bg { background-color: #f8f9fa; border-radius: 10px; padding: 15px; border: 1px solid #ddd; text-align: center; height: 100%; }

            /* Text Styles */
            .stat-value, .rev-value { font-size: 28px; font-weight: bold; margin: 0; color: #333; }
            .stat-label, .rev-title { color: grey; font-size: 14px; }

            @media (max-width: 768px) {
                .header-container { flex-direction: column; text-align: center; gap: 10px; }
                .login-box { padding: 20px; width: 90%; }
            }
        </style>
    """, unsafe_allow_html=True)

def render_header(title, border_color="#607D8B"):
    logo_html = ""
    if os.path.exists(LOGO_FILENAME):
        try:
            with open(LOGO_FILENAME, "rb") as f:
                data = f.read()
                encoded = base64.b64encode(data).decode()
            logo_html = f'<img src="data:image/jpeg;base64,{encoded}" style="height: 60px; max-width: 100%;">'
        except:
            logo_html = ""
    st.markdown(f"""
        <div class="header-container" style="border-left: 5px solid {border_color};">
            <h2 style="margin:0; color:#333;">{title}</h2>
            <div>{logo_html}</div>
        </div>
    """, unsafe_allow_html=True)
