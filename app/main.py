import streamlit as st
import sys
from pathlib import Path

# Tambahkan path ke sys.path
sys.path.append(str(Path(__file__).parent))

# Import konfigurasi tema - tidak boleh ada circular import
from config import CSS_THEME, COLORS

# Import komponen - pastikan tidak mengimpor dari pages di sini
from components.sidebar import render_sidebar
from components.header import render_header

# Import halaman akan dilakukan di dalam main() untuk menghindari circular import
# JANGAN import di sini untuk sementara

# Konfigurasi halaman
st.set_page_config(
    page_title="CHLORIS - Plant Disease AI",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Terapkan CSS tema
st.markdown(CSS_THEME, unsafe_allow_html=True)

# Inisialisasi session state
if 'confidence_threshold' not in st.session_state:
    st.session_state.confidence_threshold = 0.55
if 'overlap_threshold' not in st.session_state:
    st.session_state.overlap_threshold = 0.5

def main():
    """Aplikasi utama CHLORIS"""
    
    # Import halaman di sini untuk menghindari circular import
    try:
        from pages.scanner import render_scanner_page
        from pages.encyclopedia import render_encyclopedia_page
        from pages.reports import render_reports_page
        from pages.settings import render_settings_page
    except ImportError as e:
        st.error(f"Error importing pages: {e}")
        return
    
    # Render sidebar dan dapatkan halaman yang dipilih
    selected_page = render_sidebar()
    
    # Render header
    render_header()
    
    # Render konten berdasarkan halaman yang dipilih
    if selected_page == "Scanner Tanaman":
        render_scanner_page()
    elif selected_page == "Encyclopedia":
        render_encyclopedia_page()
    elif selected_page == "Laporan":
        render_reports_page()
    elif selected_page == "Pengaturan":
        render_settings_page()
    
    # Render footer
    render_footer()

def render_footer():
    """Render footer aplikasi"""
    st.markdown(f"""
    <div class="app-footer">
        <div style="text-align: center; padding: 1.5rem 0;">
            <div style="font-weight: 600; color: {COLORS['primary']}; margin-bottom: 0.5rem;">
                🌿 CHLORIS AI - Plant Disease Detection System
            </div>
            <div style="color: {COLORS['text_medium']}; font-size: 0.9rem;">
                Version 3.0.0 | Powered by Roboflow & Computer Vision
            </div>
            <div style="color: {COLORS['text_light']}; font-size: 0.8rem; margin-top: 0.5rem;">
                © 2024 Luxinous AI Research | Model: crop-disease-identification-dniia/2
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()