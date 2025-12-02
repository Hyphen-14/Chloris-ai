# app/components/sidebar.py
import streamlit as st
import os
from streamlit_option_menu import option_menu

def create_sidebar():
    """Create the sidebar navigation"""
    with st.sidebar:
        # Logo
        logo_path = "app/assets/chloris_logo-removebg.png"
        if os.path.exists(logo_path):
            st.image(logo_path, width="stretch")
        else:
            st.title("🌿 CHLORIS AI")
        
        st.markdown("<div style='text-align: center; margin-top: -10px; margin-bottom: 20px; color: #888; font-size: 12px; letter-spacing: 2px;'>LUMINOUS AI SYSTEM</div>", unsafe_allow_html=True)
        
        # Navigation
        selected = option_menu(
            menu_title=None,
            options=["Scanner Tanaman", "Ensiklopedia", "Laporan", "Pengaturan"],
            icons=["camera", "flower1", "clipboard-heart", "sliders"],
            menu_icon="cast",
            default_index=0,
            styles={
                "container": {"padding": "0!important", "background-color": "transparent"},
                "icon": {"color": "#A8E890", "font-size": "18px"},
                "nav-link": {"font-size": "15px", "text-align": "left", "margin":"5px", "--hover-color": "#1a2f23", "color": "#d1e7dd"},
                "nav-link-selected": {"background-color": "rgba(168, 232, 144, 0.1)", "color": "#A8E890", "font-weight": "bold", "border-left": "3px solid #A8E890"},
            }
        )
        
        st.markdown("---")
        st.caption("SYSTEM DIAGNOSTICS")
        st.success("🟢 CPU: Intel i7 [ONLINE]")
        st.info("📡 AI Model: Ready")
        
        return selected