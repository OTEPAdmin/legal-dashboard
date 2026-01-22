import streamlit as st

def load_css():
    st.markdown("""
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Kanit:wght@300;400;500;700&display=swap');

            /* Apply Kanit font to standard text elements ONLY */
            html, body, [class*="css"], h1, h2, h3, h4, h5, h6, p, div, span, button, input, textarea, select {
                font-family: 'Kanit', sans-serif !important;
            }

            /* FIX: Ensure Material Icons (like expander arrows) use their correct font */
            .material-icons, [class*="material-icons"], [data-testid="stExpander"] svg, [data-testid="stExpander"] i {
                font-family: 'Material Icons' !important;
                font-weight: normal;
                font-style: normal;
                display: inline-block;
                text-transform: none;
                letter-spacing: normal;
                word-wrap: normal;
                white-space: nowrap;
                direction: ltr;
            }

            /* Metric Cards Styling */
            div[data-testid="metric-container"] {
                background-color: #FFFFFF;
                border: 1px solid #E0E0E0;
                padding: 15px;
                border-radius: 8px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.05);
            }
            
            /* Header Styling */
            header[data-testid="stHeader"] {
                background-color: #FFFFFF;
            }

            /* Button Styling */
            button[kind="primary"] {
                background-color: #00838F;
                border: none;
                transition: 0.3s;
            }
            button[kind="primary"]:hover {
                background-color: #006064;
            }

            /* Custom Expander Styling */
            .streamlit-expanderHeader {
                font-size: 16px;
                font-weight: 500;
                color: #333;
            }
            
        </style>
    """, unsafe_allow_html=True)

def render_header(title, border_color="#00BCD4"):
    st.markdown(f"""
    <div style="
        padding: 15px 20px; 
        background-color: white; 
        border-radius: 10px; 
        border-left: 6px solid {border_color};
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        margin-bottom: 20px;
        display: flex;
        align-items: center;
    ">
        <h2 style="margin:0; padding:0; color:#333; font-family:'Kanit';">{title}</h2>
    </div>
    """, unsafe_allow_html=True)
