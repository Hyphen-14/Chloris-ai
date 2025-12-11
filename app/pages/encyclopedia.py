import streamlit as st
import json
import os
from pathlib import Path
from config import COLORS

def load_disease_data():
    """Memuat data penyakit dari file JSON"""
    try:
        # Mencoba mencari file di beberapa kemungkinan lokasi
        possible_paths = [
            Path("data/diseases/penyakit.json"),
            Path("app/data/diseases/penyakit.json"),
            Path("penyakit.json") # Jika ada di root
        ]
        
        json_path = None
        for path in possible_paths:
            if path.exists():
                json_path = path
                break
        
        if json_path:
            with open(json_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        else:
            st.error("File database penyakit (penyakit.json) tidak ditemukan!")
            return {}
            
    except Exception as e:
        st.error(f"Gagal memuat database: {e}")
        return {}

def render_encyclopedia_page():
    """Render halaman encyclopedia dengan Data Real"""
    
    # --- HEADER BOX ---
    st.markdown(f"""
    <div class="page-header-box">
        <h2 style="color: {COLORS['text_main']}; margin-top: 0;">📚 Encyclopedia Tanaman</h2>
        <p style="color: {COLORS['text_body']}; margin-bottom: 0;">
            Katalog lengkap penyakit tanaman, gejala, dan solusi penanganannya.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Load Data
    data_penyakit = load_disease_data()
    
    # --- SEARCH BAR ---
    st.markdown(f"""
    <div style="background: {COLORS['card_bg']}; padding: 15px; border-radius: 12px; border: 1px solid {COLORS['border']}; margin-bottom: 20px;">
        <h5 style="color: {COLORS['text_main']}; margin: 0 0 10px 0;">🔍 Cari Penyakit</h5>
    """, unsafe_allow_html=True)
    
    col_search, col_filter = st.columns([3, 1])
    with col_search:
        search_query = st.text_input("Cari nama penyakit...", placeholder="Contoh: Mosaic, Blight...", label_visibility="collapsed")
    with col_filter:
        filter_risk = st.selectbox("Filter Risiko", ["Semua", "High", "Medium", "Low"], label_visibility="collapsed")
    
    st.markdown("</div>", unsafe_allow_html=True)

    # --- FILTER LOGIC ---
    filtered_items = {}
    for key, info in data_penyakit.items():
        # Filter Search Text
        match_name = search_query.lower() in info['nama_id'].lower() or search_query.lower() in key.lower()
        
        # Filter Risk Level
        match_risk = True
        if filter_risk != "Semua":
            if info.get('tingkat_bahaya') != filter_risk:
                match_risk = False
        
        if match_name and match_risk:
            filtered_items[key] = info

    # --- TAMPILAN GRID ---
    if not filtered_items:
        st.info("Tidak ada penyakit yang cocok dengan pencarian Anda.")
    else:
        # Menampilkan jumlah hasil
        st.markdown(f"<p style='color: {COLORS['text_light']}; font-size: 0.9rem;'>Menampilkan {len(filtered_items)} hasil:</p>", unsafe_allow_html=True)
        
        # Grid 3 Kolom
        cols = st.columns(3)
        
        for idx, (key, info) in enumerate(filtered_items.items()):
            col = cols[idx % 3] # Distribusi ke 3 kolom
            
            with col:
                # Tentukan warna badge berdasarkan tingkat bahaya
                risk = info.get('tingkat_bahaya', 'Unknown')
                if risk == 'High':
                    risk_color = COLORS['error']
                    risk_bg = "#FFEBEE"
                elif risk == 'Medium':
                    risk_color = COLORS['warning']
                    risk_bg = "#FFF3E0"
                else:
                    risk_color = COLORS['success']
                    risk_bg = "#E8F5E9"

                # Container Card
                with st.container():
                    st.markdown(f"""
                    <div style="
                        background: {COLORS['white']}; 
                        border: 1px solid {COLORS['border']}; 
                        border-radius: 12px; 
                        padding: 15px; 
                        margin-bottom: 20px;
                        height: 100%;
                        box-shadow: 0 2px 5px rgba(0,0,0,0.03);
                        transition: transform 0.2s;
                    ">
                        <div style="display: flex; justify-content: space-between; align-items: start; margin-bottom: 10px;">
                            <div style="font-size: 2rem;">🌿</div>
                            <div style="background: {risk_bg}; color: {risk_color}; padding: 4px 10px; border-radius: 20px; font-size: 0.7rem; font-weight: 700; border: 1px solid {risk_color}30;">
                                {risk.upper()}
                            </div>
                        </div>
                        <h4 style="color: {COLORS['text_main']}; margin: 0 0 5px 0; font-size: 1.1rem; height: 3.5rem; overflow: hidden; display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical;">
                            {info['nama_id']}
                        </h4>
                        <div style="height: 1px; background: {COLORS['border']}; margin: 10px 0;"></div>
                    """, unsafe_allow_html=True)
                    
                    # Gunakan Expander untuk Detail agar rapi
                    with st.expander("Lihat Solusi & Detail"):
                        st.markdown(f"**Tingkat Bahaya:** {risk}")
                        st.markdown("**💡 Solusi:**")
                        for solusi in info.get('solusi', []):
                            st.markdown(f"- {solusi}")
                            
                    st.markdown("</div>", unsafe_allow_html=True)