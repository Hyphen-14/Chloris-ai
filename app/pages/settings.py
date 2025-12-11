import streamlit as st
from config import COLORS

def render_settings_page():
    """Render halaman pengaturan dengan UI Box"""
    
    # --- HEADER BOX ---
    st.markdown(f"""
    <div class="page-header-box">
        <h2 style="color: {COLORS['text_main']}; margin-top: 0;">⚙️ Pengaturan Sistem</h2>
        <p style="color: {COLORS['text_body']}; margin-bottom: 0;">
            Konfigurasi preferensi aplikasi dan parameter model AI.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Pengaturan Umum Container
    with st.expander("🛠️ Preferensi Umum", expanded=True):
        st.checkbox("Aktifkan Suara Notifikasi", value=True)
        st.checkbox("Simpan Riwayat Scan Otomatis", value=True)
        
    # Pengaturan Model Container
    with st.expander("🤖 Parameter Model AI", expanded=True):
        st.markdown(f"<div style='color: {COLORS['text_body']}'>Atur sensitivitas deteksi:</div>", unsafe_allow_html=True)
        
        conf = st.slider("Confidence Threshold", 0.0, 1.0, st.session_state.confidence_threshold)
        st.session_state.confidence_threshold = conf
        
        st.markdown(f"""
        <div style="background: {COLORS['secondary']}; padding: 10px; border-radius: 8px; margin-top: 10px; font-size: 0.9rem; color: {COLORS['text_body']};">
            💡 <strong>Tips:</strong> Nilai yang lebih tinggi mengurangi deteksi salah, tetapi mungkin melewatkan beberapa penyakit samar.
        </div>
        """, unsafe_allow_html=True)

    # Info Aplikasi
    st.markdown(f"""
    <div style="margin-top: 30px; text-align: center; color: {COLORS['text_light']}; font-size: 0.8rem;">
        CHLORIS AI v3.0.0<br>
        Build 2024.12.05
    </div>
    """, unsafe_allow_html=True)

    # MANAJEMEN DATA
    with st.expander("💾 Manajemen Data", expanded=False):
        st.markdown(f"<div style='color: {COLORS['text_body']}'>Kelola data riwayat scan Anda.</div>", unsafe_allow_html=True)
        
        col_info, col_btn = st.columns([3, 1])
        
        with col_info:
            st.warning("Menghapus riwayat akan menghilangkan semua log laporan dan foto yang tersimpan.")
            
        with col_btn:
            if st.button("🗑️ Hapus Semua Data", type="primary"):
                from utils import clear_history_data
                if clear_history_data():
                    st.success("Database berhasil di-reset!")
                    st.rerun()
                else:
                    st.error("Gagal menghapus data.")