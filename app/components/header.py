import streamlit as st
from config import COLORS

def render_header():
    """Render header dengan tema cerah"""
    
    st.markdown('<div class="app-header">', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col1:
        st.markdown(f"""
        <div style="text-align: center;">
            <div style="font-size: 3rem; color: {COLORS['primary']}; margin-bottom: 0.5rem;">🌿</div>
            <div style="color: {COLORS['primary']}; font-weight: 600; font-size: 0.9rem;">
                CHLORIS AI
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div style="text-align: center;">
            <h1 style="color: {COLORS['primary']} !important; margin-bottom: 0.25rem !important;">
                Sistem Deteksi Penyakit Tanaman
            </h1>
            <p style="color: {COLORS['text_medium']}; margin-top: 0;">
                Powered by Computer Vision & Machine Learning
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div style="text-align: right;">
            <div style="font-size: 0.9rem; color: {COLORS['text_medium']};">
                <div style="margin-bottom: 0.25rem;">
                    <span style="color: {COLORS['text_light']};">Confidence:</span>
                    <span style="color: {COLORS['primary']}; font-weight: 600;">
                        {st.session_state.confidence_threshold:.0%}
                    </span>
                </div>
                <div>
                    <span style="color: {COLORS['text_light']};">Status:</span>
                    <span style="color: {COLORS['success']}; font-weight: 600;">Online</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)