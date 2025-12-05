import streamlit as st
from config import COLORS

def render_reports_page():
    st.markdown('<div class="custom-card">', unsafe_allow_html=True)
    st.markdown('<div class="card-title">📊 Laporan & Analisis</div>', unsafe_allow_html=True)
    
    st.markdown(f"""
    <div style="color: {COLORS['text_medium']}; margin-bottom: 1.5rem;">
        Analisis statistik dan laporan hasil deteksi penyakit tanaman.
    </div>
    """, unsafe_allow_html=True)
    
    # Date range
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input("Dari Tanggal")
    with col2:
        end_date = st.date_input("Sampai Tanggal")
    
    # Report type
    report_type = st.radio(
        "Jenis Laporan:",
        ["📈 Ringkasan Statistik", "🌱 Analisis Tanaman", "🦠 Penyakit Terbanyak", "📅 Tren Bulanan"],
        horizontal=True
    )
    
    # Placeholder chart
    st.markdown(f"""
    <div style="background: {COLORS['light_gray']}; 
                border-radius: 10px; 
                padding: 2rem; 
                text-align: center;
                margin: 1.5rem 0;">
        <div style="font-size: 3rem; color: {COLORS['text_light']}; margin-bottom: 1rem;">📊</div>
        <div style="color: {COLORS['text_medium']};">
            Visualisasi data akan ditampilkan di sini
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Statistics
    st.markdown("### 📈 Statistik Singkat")
    
    cols = st.columns(4)
    stats = [
        ("Total Analisis", "42", "+12%"),
        ("Tanaman Sehat", "28", "67%"),
        ("Tanaman Sakit", "14", "33%"),
        ("Akurasi Model", "89%", "+3%")
    ]
    
    for col, (label, value, delta) in zip(cols, stats):
        with col:
            st.metric(label, value, delta)
    
    st.info("""
    **Fitur Laporan sedang dalam pengembangan.** 
    
    Fitur yang akan datang:
    - Grafik interaktif hasil analisis
    - Ekspor laporan ke PDF/Excel
    - Analisis tren penyakit
    - Rekomendasi berbasis data
    """)
    
    st.markdown('</div>', unsafe_allow_html=True)