import streamlit as st
import cv2
import numpy as np
import time
import os
import json
from datetime import datetime
from streamlit_option_menu import option_menu

# --- IMPORT MODUL KITA ---
from styles import load_css
from utils import draw_glowing_box

# --- 1. KONFIGURASI HALAMAN ---
st.set_page_config(
    page_title="Chloris: Night Bloom",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. LOAD DESIGN ---
load_css()

# --- 3. SIDEBAR ---
with st.sidebar:
    logo_path = "src\\chloris_logo-removebg.png"
    if os.path.exists(logo_path):
        # width='stretch' agar tidak ada warning deprecated
        st.image(logo_path, width='stretch') 
    else:
        st.title("CHLORIS")

    st.markdown("<div style='text-align: center; margin-top: -10px; margin-bottom: 20px; color: #888; font-size: 12px; letter-spacing: 2px;'>LUMINOUS AI SYSTEM</div>", unsafe_allow_html=True)
    
    # Menu kembali ke nuansa Hijau (Default style styles.py akan menangani ini, tapi kita sesuaikan iconnya)
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
    st.success("🟢 GPU: RTX 4060 [ONLINE]")
    st.info("📡 Network: Secure")

# --- 4. HALAMAN SCANNER ---
def show_scanner_page():
    st.markdown("## 🌿 Night Vision Scanner")
    
    with st.container():
        info1, info2, info3 = st.columns(3)
        with info1:
            st.markdown("""
            <div class="info-box">
                <span style="font-size: 11px; color: #A8E890; letter-spacing: 1px;">LOKASI</span><br>
                <span style="font-weight: bold; font-size: 14px;">Greenhouse A</span>
            </div>
            """, unsafe_allow_html=True)
        with info2:
            current_time = datetime.now().strftime("%H:%M WIB")
            st.markdown(f"""
            <div class="info-box">
                <span style="font-size: 11px; color: #FFB7B2; letter-spacing: 1px;">WAKTU</span><br>
                <span style="font-weight: bold; font-size: 14px;">{current_time}</span>
            </div>
            """, unsafe_allow_html=True)
        with info3:
            st.markdown("""
            <div class="info-box">
                <span style="font-size: 11px; color: #A8E890; letter-spacing: 1px;">SUHU</span><br>
                <span style="font-weight: bold; font-size: 14px;">24°C (Optimal)</span>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)

    col_vid, col_stat = st.columns([2, 1.2])
    
    with col_stat:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("### 📊 Analisis Real-time")
        
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("""
                <div class="metric-box">
                    <div class="metric-value">92%</div>
                    <div class="metric-label">CONFIDENCE</div>
                </div>
            """, unsafe_allow_html=True)
        with c2:
            st.markdown("""
                <div class="metric-box" style="border-color: #FF6B6B; background: rgba(255, 107, 107, 0.1);">
                    <div class="metric-value" style="color: #FF6B6B; text-shadow: 0 0 10px rgba(255, 107, 107, 0.4);">CRITICAL</div>
                    <div class="metric-label">SEVERITY</div>
                </div>
            """, unsafe_allow_html=True)
            
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("#### 🧬 Terdeteksi:")
        st.warning("⚠️ **Karat Daun (Leaf Rust)**")
        
        with st.expander("🍃 Saran Perawatan AI", expanded=True):
            st.write("1. Isolasi tanaman segera.")
            st.write("2. Kurangi kelembapan malam hari.")
            st.write("3. Aplikasi fungisida organik.")
        st.markdown('</div>', unsafe_allow_html=True)

    with col_vid:
        st.markdown('<div class="glass-card" style="padding: 10px;">', unsafe_allow_html=True)
        run_camera = st.toggle("🌸 Aktifkan Sensor", value=True)
        
        image_placeholder = st.image([])
        cap = cv2.VideoCapture(0)
        
        while run_camera:
            ret, frame = cap.read()
            if not ret:
                st.error("Kamera tidak terdeteksi.")
                break
            
            frame = cv2.convertScaleAbs(frame, alpha=0.8, beta=0) 

            h, w, _ = frame.shape
            start_point = (150, 100)
            end_point = (500, 400)
            
            # Warna Mint Green
            draw_glowing_box(frame, start_point, end_point, color=(144, 232, 168), thickness=2)
            
            text = "Leaf Rust :: 92%"
            cv2.rectangle(frame, (start_point[0], start_point[1]-30), (start_point[0] + 200, start_point[1]-5), (20, 30, 25), -1)
            cv2.putText(frame, text, (start_point[0]+10, start_point[1]-12), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (168, 232, 144), 1)
            
            t = time.time()
            scan_y = int(start_point[1] + (np.sin(t*2)+1)/2 * (end_point[1]-start_point[1]))
            cv2.line(frame, (start_point[0], scan_y), (end_point[0], scan_y), (178, 183, 255), 2)
            
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            # FIX: Gunakan width='stretch'
            image_placeholder.image(frame, channels="RGB", width='stretch')
        
        cap.release()
        st.markdown('</div>', unsafe_allow_html=True)


# --- 5. HALAMAN ENSIKLOPEDIA (PERBAIKAN UTAMA) ---
def show_encyclopedia_page():
    st.markdown("## 📚 Grimoire Penyakit Tanaman")
    st.markdown("Database lengkap pengetahuan tentang patogen dan penyembuhannya.")
    
    search = st.text_input("🔍 Cari penyakit...", placeholder="Contoh: Karat Daun")
    st.markdown("<br>", unsafe_allow_html=True)
    
    try:
        with open('data/penyakit.json', 'r') as f:
            database = json.load(f)
    except FileNotFoundError:
        st.error("Database 'data/penyakit.json' tidak ditemukan! Pastikan file sudah dibuat.")
        database = {}

    found = False
    for eng_name, info in database.items():
        if search.lower() in eng_name.lower() or search.lower() in info['nama_id'].lower():
            found = True
            
            # Logic Pewarnaan Status (Kembali ke Tema Asli)
            level = info.get('tingkat_bahaya', 'Medium') 
            
            if level == "Critical":
                badge_color = "#FF0000"
                badge_bg = "rgba(255, 0, 0, 0.15)"
                border_color = "#FF4500"
            elif level == "High":
                badge_color = "#FF5733"
                badge_bg = "rgba(255, 87, 51, 0.15)"
                border_color = "#C70039"
            elif level == "Medium":
                badge_color = "#FFC300"
                badge_bg = "rgba(255, 195, 0, 0.15)"
                border_color = "#FFD700"
            elif level == "Aman":
                badge_color = "#00FF7F"
                badge_bg = "rgba(0, 255, 127, 0.15)"
                border_color = "#32CD32"
            else:
                badge_color = "#A8E890"
                badge_bg = "rgba(168, 232, 144, 0.15)"
                border_color = "#A8E890"

            # --- PENAMBALAN KEBOCORAN ---
            # Kita buat string HTML dalam satu baris atau f-string bersih
            # untuk menghindari error parsing markdown.
            
            card_html = f"""
            <div class="glass-card" style="border-left: 4px solid {badge_color};">
                <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid rgba(255,255,255,0.1); padding-bottom: 10px; margin-bottom: 10px;">
                    <div>
                        <h3 style="margin: 0; color: #A8E890; font-family: 'Montserrat', sans-serif; font-size: 20px;">{info['nama_id']}</h3>
                        <span style="font-size: 14px; color: #888; font-style: italic;">{eng_name}</span>
                    </div>
                    <div style="text-align: right;">
                        <span style="
                            background: {badge_bg}; 
                            color: {badge_color}; 
                            padding: 5px 12px; 
                            border-radius: 12px; 
                            font-size: 11px; 
                            border: 1px solid {border_color}; 
                            font-weight: bold; 
                            letter-spacing: 1px;">
                            {level.upper()}
                        </span>
                    </div>
                </div>
                <div style="margin-bottom: 10px;">
                    <p style="font-style: italic; color: #d1e7dd; font-size: 14px; margin: 0;">🔬 Latin: {info['latin']}</p>
                </div>
                <div style="background: rgba(0,0,0,0.2); padding: 12px; border-radius: 10px; margin-top: 5px;">
                    <p style="margin:0; font-size: 14px; color: #e0f2f1;">
                        <span style="color: {badge_color}; font-weight: bold;">🥀 Gejala:</span> {info['gejala']}
                    </p>
                </div>
            </div>
            """
            
            # EKSEKUSI RENDER DENGAN AMAN
            st.markdown(card_html, unsafe_allow_html=True)
            
            # Bagian Expander tetap pakai Streamlit native agar aman
            with st.expander(f"💊 Lihat Resep Penyembuhan"):
                for i, step in enumerate(info['solusi'], 1):
                    st.markdown(f"""
                    <div style="margin-bottom: 5px; padding-left: 10px; border-left: 2px solid #A8E890;">
                        <span style="color: #FFB7B2; font-weight: bold;">{i}.</span> {step}
                    </div>
                    """, unsafe_allow_html=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
    
    if not found:
        st.info("Belum ada data penyakit yang cocok dengan pencarianmu.")

# --- 6. ROUTING HALAMAN ---
if selected == "Scanner Tanaman":
    show_scanner_page()
elif selected == "Ensiklopedia":
    show_encyclopedia_page()
elif selected == "Laporan":
    st.title("📄 Laporan")
    st.info("Halaman dalam pengembangan.")
elif selected == "Pengaturan":
    st.title("⚙️ Pengaturan")
    st.info("Halaman dalam pengembangan.")