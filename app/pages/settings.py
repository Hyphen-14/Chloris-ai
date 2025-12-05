import streamlit as st
from config import COLORS

def render_settings_page():
    st.markdown('<div class="custom-card">', unsafe_allow_html=True)
    st.markdown('<div class="card-title">⚙️ Pengaturan Sistem</div>', unsafe_allow_html=True)
    
    st.markdown(f"""
    <div style="color: {COLORS['text_medium']}; margin-bottom: 1.5rem;">
        Konfigurasi sistem dan preferensi aplikasi.
    </div>
    """, unsafe_allow_html=True)
    
    # Tabs for different settings
    tab1, tab2, tab3 = st.tabs(["🏗️ Sistem", "🔧 Model", "👤 Akun"])
    
    with tab1:
        st.markdown("#### Pengaturan Sistem")
        
        col1, col2 = st.columns(2)
        with col1:
            st.checkbox("Notifikasi Email", value=True)
            st.checkbox("Auto-save hasil", value=True)
            st.checkbox("Tampilkan bounding box", value=True)
        
        with col2:
            st.selectbox("Bahasa", ["Indonesia", "English", "中文"])
            st.selectbox("Tema", ["Hijau Muda", "Gelap", "Biru"])
            st.slider("Ukuran font", 12, 18, 14)
    
    with tab2:
        st.markdown("#### Pengaturan Model")
        
        col1, col2 = st.columns(2)
        with col1:
            default_threshold = st.slider("Default Confidence", 0.0, 1.0, 0.55, 0.05)
            st.session_state.default_confidence = default_threshold
            
            overlap = st.slider("Overlap Threshold", 0.0, 1.0, 0.5, 0.05)
            st.session_state.overlap_threshold = overlap
        
        with col2:
            model_version = st.selectbox("Versi Model", ["v2 (latest)", "v1", "beta"])
            st.checkbox("Auto-update model", value=False)
            st.checkbox("Gunakan GPU", value=False, disabled=True)
        
        st.button("💾 Simpan Pengaturan Model", type="primary")
    
    with tab3:
        st.markdown("#### Pengaturan Akun")
        
        col1, col2 = st.columns(2)
        with col1:
            st.text_input("Nama", value="Petani AI")
            st.text_input("Email", value="petani@example.com")
            st.text_input("Lokasi", value="Indonesia")
        
        with col2:
            st.selectbox("Jenis Tanaman", ["Campuran", "Sayuran", "Buah", "Hias"])
            st.number_input("Luas Lahan (m²)", min_value=1, value=100)
            st.selectbox("Pengalaman", ["Pemula", "Menengah", "Ahli"])
        
        st.button("💾 Perbarui Profil", type="primary")
    
    st.markdown("---")
    
    # System info
    st.markdown("#### ℹ️ Informasi Sistem")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Versi Aplikasi:** 3.0.0")
        st.markdown("**Streamlit:** 1.28.0")
        st.markdown("**Python:** 3.9+")
    
    with col2:
        st.markdown("**Model:** YOLOv8")
        st.markdown("**Dataset:** PlantVillage")
        st.markdown("**Status:** Online")
    
    st.button("🔄 Periksa Pembaruan", type="secondary")
    
    st.markdown('</div>', unsafe_allow_html=True)