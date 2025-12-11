import streamlit as st
from config import COLORS
from utils import set_roboflow_api_key

def render_sidebar():
    """Render sidebar dengan tema Light / Garden Theme"""
    
    with st.sidebar:
        # Logo dan header sidebar
        st.markdown(f"""
        <div style="text-align: center; margin-bottom: 2rem; margin-top: 1rem;">
            <div style="
                background: {COLORS['secondary']}; 
                width: 80px; 
                height: 80px; 
                border-radius: 50%; 
                display: flex; 
                align-items: center; 
                justify-content: center; 
                margin: 0 auto 1rem auto;">
                <span style="font-size: 2.5rem;">🌿</span>
            </div>
            <div style="font-size: 1.5rem; font-weight: 800; color: {COLORS['text_main']}; letter-spacing: -0.5px;">
                CHLORIS AI
            </div>
            <div style="color: {COLORS['text_light']}; font-size: 0.85rem; font-weight: 500;">
                Plant Disease Detection
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Navigation
        st.markdown(f"""
        <div style="color: {COLORS['text_light']}; font-size: 0.75rem; font-weight: 700; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 0.8rem;">
            Main Menu
        </div>
        """, unsafe_allow_html=True)
        
        menu_options = {
            "Scanner Tanaman": "🔍",
            "Encyclopedia": "📚",
            "Laporan": "📊",
            "Pengaturan": "⚙️"
        }
        
        # Custom CSS injection khusus untuk sidebar radio button agar terlihat seperti pill/tombol
        st.markdown(f"""
        <style>
            div.row-widget.stRadio > div {{
                background-color: transparent;
            }}
            div.row-widget.stRadio > div[role="radiogroup"] > label {{
                background-color: transparent;
                border: 1px solid transparent;
                padding: 10px;
                border-radius: 10px;
                transition: all 0.3s;
            }}
            div.row-widget.stRadio > div[role="radiogroup"] > label:hover {{
                background-color: {COLORS['secondary']};
                color: {COLORS['primary']};
            }}
        </style>
        """, unsafe_allow_html=True)

        selected = st.radio(
            "Pilih Menu:",
            list(menu_options.keys()),
            format_func=lambda x: f"{menu_options[x]}  {x}",
            label_visibility="collapsed"
        )
        
        st.markdown("---")
        
        # API Key Section (Card Style)
        st.markdown(f"""
        <div style="background: {COLORS['background']}; padding: 15px; border-radius: 12px; border: 1px solid {COLORS['border']};">
            <div style="color: {COLORS['text_main']}; font-weight: 600; font-size: 0.9rem; margin-bottom: 0.5rem;">
                🔑 Roboflow API
            </div>
        """, unsafe_allow_html=True)
        
        api_key = st.text_input(
            "API Key",
            type="password",
            value=st.session_state.get('roboflow_api_key', ''),
            placeholder="Paste Key Here",
            label_visibility="collapsed"
        )
        
        if api_key and api_key != st.session_state.get('roboflow_api_key'):
            try:
                set_roboflow_api_key(api_key)
                st.success("Tersimpan!")
            except Exception as e:
                st.error("Gagal simpan")
        
        status_color = COLORS['success'] if st.session_state.get('roboflow_api_key') else COLORS['warning']
        status_text = "Connected" if st.session_state.get('roboflow_api_key') else "Not Configured"
        
        st.markdown(f"""
            <div style="display: flex; align-items: center; gap: 8px; margin-top: 8px;">
                <div style="width: 8px; height: 8px; border-radius: 50%; background-color: {status_color};"></div>
                <span style="font-size: 0.8rem; color: {COLORS['text_body']};">{status_text}</span>
            </div>
            <div style="margin-top: 8px; text-align: right;">
                 <a href="https://app.roboflow.com" target="_blank" style="font-size: 0.75rem; color: {COLORS['primary']}; text-decoration: none;">Get Key →</a>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Settings Preview
        st.markdown(f"""
        <div style="color: {COLORS['text_light']}; font-size: 0.75rem; font-weight: 700; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 0.8rem;">
            Quick Settings
        </div>
        """, unsafe_allow_html=True)
        
        confidence = st.slider(
            "Confidence",
            0.0, 1.0, 
            st.session_state.confidence_threshold,
            0.05
        )
        st.session_state.confidence_threshold = confidence
        
    return selected