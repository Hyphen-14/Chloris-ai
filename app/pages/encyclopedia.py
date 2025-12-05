import streamlit as st
from config import COLORS

def render_encyclopedia_page():
    st.markdown('<div class="custom-card">', unsafe_allow_html=True)
    st.markdown('<div class="card-title">📚 Encyclopedia Tanaman</div>', unsafe_allow_html=True)
    
    st.markdown(f"""
    <div style="color: {COLORS['text_medium']}; margin-bottom: 1.5rem;">
        Database pengetahuan tentang berbagai jenis tanaman dan penyakit yang umum ditemui.
    </div>
    """, unsafe_allow_html=True)
    
    # Search bar
    search_query = st.text_input("🔍 Cari tanaman atau penyakit...", placeholder="Contoh: Tomat, Blight, Cabai")
    
    # Categories
    st.markdown("### Kategori")
    
    cols = st.columns(4)
    categories = [
        ("🍅", "Tanaman Buah", "Tomat, Cabai, Terong"),
        ("🥔", "Tanaman Umbi", "Kentang, Wortel, Bawang"),
        ("🌾", "Tanaman Pangan", "Padi, Jagung, Gandum"),
        ("🌿", "Tanaman Hias", "Mawar, Anggrek, Melati")
    ]
    
    for col, (icon, title, desc) in zip(cols, categories):
        with col:
            st.markdown(f"""
            <div style="background: {COLORS['primary_light']}; 
                        border-radius: 10px; 
                        padding: 1rem; 
                        text-align: center;
                        margin-bottom: 1rem;">
                <div style="font-size: 2rem;">{icon}</div>
                <div style="font-weight: 600; margin-bottom: 0.25rem;">{title}</div>
                <div style="color: {COLORS['text_medium']}; font-size: 0.85rem;">{desc}</div>
            </div>
            """, unsafe_allow_html=True)
    
    # Placeholder content
    st.info("""
    **Fitur Encyclopedia sedang dalam pengembangan aktif.** 
    
    Fitur yang akan datang:
    - Database lengkap 100+ jenis tanaman
    - 500+ penyakit tanaman dengan gambar
    - Solusi pengobatan detail
    - Pencegahan dan perawatan
    """)
    
    st.markdown('</div>', unsafe_allow_html=True)