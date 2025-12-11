import streamlit as st
from config import COLORS

def render_header():
    """Render header dengan Teknik Safe-String (Anti-Blackbox)"""
    
    # HTML ditulis rapat tanpa spasi/indentasi di awal tag
    header_html = f"""<div class="header-box"><div style="display: flex; align-items: center; justify-content: space-between;"><div style="display: flex; align-items: center; gap: 15px;"><div style="font-size: 2.5rem;">🌿</div><div><h1 style="color: #333333 !important; margin: 0 !important; font-size: 1.8rem !important; font-weight: 800;">CHLORIS AI</h1><p style="color: #555555 !important; margin: 0 !important; font-size: 0.9rem;">Plant Disease Detection System</p></div></div><div style="text-align: right; background: rgba(255,255,255,0.5); padding: 8px 15px; border-radius: 10px; border: 1px solid {COLORS['primary']}30;"><div style="font-size: 0.8rem; color: #555555;">Confidence Threshold</div><div style="font-size: 1.2rem; font-weight: 700; color: {COLORS['primary']};">{st.session_state.confidence_threshold:.0%}</div></div></div></div>"""
    
    st.markdown(header_html, unsafe_allow_html=True)