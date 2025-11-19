import streamlit as st
import cv2
import numpy as np
import time
import os
from datetime import datetime
from streamlit_option_menu import option_menu

# --- 1. KONFIGURASI HALAMAN ---
st.set_page_config(
    page_title="Chloris: Mystic Bloom",
    page_icon="🌸",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. CSS INJECTION (TEMA: MYSTIC ORCHID - UNGU GELAP & ROSE GOLD) ---
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@400;700&family=Quicksand:wght@300;400;600&display=swap');

        /* BACKGROUND: Deep Mystic Night (Ungu ke Hitam) */
        .stApp {
            background-color: #0F0518;
            background-image: radial-gradient(circle at 20% 30%, #2D1B4E 0%, #0F0518 70%);
            color: #E6E6FA; /* Lavender Text */
        }

        /* TYPOGRAPHY: Cinzel (Elegan & Magis) */
        h1, h2, h3 {
            font-family: 'Cinzel', serif;
            color: #FFD1DC !important; /* Pastel Pink */
            text-shadow: 0 0 15px rgba(255, 209, 220, 0.3);
            letter-spacing: 1px;
        }
        
        p, div, label, span {
            font-family: 'Quicksand', sans-serif;
            color: #D8BFD8; /* Thistle/Ungu Muda */
        }

        /* GLASS CARD (Kotak Kaca Ungu Transparan) */
        .glass-card {
            background: rgba(45, 27, 78, 0.4);
            backdrop-filter: blur(16px);
            border-radius: 24px;
            border: 1px solid rgba(255, 209, 220, 0.1); /* Border Pink Tipis */
            padding: 24px;
            margin-bottom: 20px;
            box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.6);
            transition: transform 0.3s ease, border-color 0.3s ease;
        }
        .glass-card:hover {
            transform: translateY(-5px);
            border-color: rgba(255, 209, 220, 0.4);
            box-shadow: 0 10px 40px rgba(216, 191, 216, 0.15); /* Glow Ungu */
        }

        /* INFO BOX (Top Bar) - Perbaikan Selector agar tidak kena elemen kosong */
        div[data-testid="stHorizontalBlock"] .info-box-container {
            background: rgba(255, 255, 255, 0.03);
            border-radius: 15px;
            padding: 12px;
            text-align: center;
            border: 1px solid rgba(255, 255, 255, 0.05);
            transition: 0.3s;
        }
        div[data-testid="stHorizontalBlock"] .info-box-container:hover {
            background: rgba(255, 182, 193, 0.1);
            border-color: #FFB7B2;
        }

        /* METRIC BOX (Statistik Feminim) */
        .metric-box {
            text-align: center;
            padding: 15px;
            border-radius: 20px;
            background: linear-gradient(135deg, rgba(255, 209, 220, 0.05), rgba(45, 27, 78, 0.3));
            border: 1px solid rgba(255, 192, 203, 0.2);
            margin-bottom: 10px;
        }
        .metric-value {
            font-family: 'Cinzel', serif;
            font-size: 28px;
            font-weight: bold;
            color: #FFB7B2; /* Rose Gold */
            text-shadow: 0 0 10px rgba(255, 183, 178, 0.5);
        }
        .metric-label {
            font-size: 12px; color: #E6E6FA; letter-spacing: 1px; text-transform: uppercase;
        }

        /* SIDEBAR */
        section[data-testid="stSidebar"] {
            background-color: #0a0310;
            border-right: 1px solid rgba(255, 209, 220, 0.05);
        }
        
        /* Fix Padding atas */
        .block-container { padding-top: 2rem; }
        
        /* TOMBOL (Gradient Pink-Ungu) */
        .stButton button {
            background: linear-gradient(45deg, #C06C84, #6C5B7B);
            color: #FFE4E1;
            font-family: 'Quicksand', sans-serif;
            font-weight: 700;
            border: none;
            border-radius: 15px;
            padding: 0.6rem 1.2rem;
            transition: 0.4s;
            box-shadow: 0 4px 15px rgba(192, 108, 132, 0.2);
        }
        .stButton button:hover {
            background: linear-gradient(45deg, #FF8C94, #A864A8);
            box-shadow: 0 0 25px rgba(255, 140, 148, 0.5); /* Pink Glow */
            transform: scale(1.02);
            color: white;
        }
        
        /* TOGGLE SWITCH (Warna Pink) */
        .stToggle label { color: #FFB7B2 !important; }
    </style>
""", unsafe_allow_html=True)

# --- 3. SIDEBAR ---
with st.sidebar:
    logo_path = "src\image\chloris_logo-removebg.png"
    if os.path.exists(logo_path):
        st.image(logo_path, width='stretch') # Fix parameter
    else:
        st.title("CHLORIS")

    st.markdown("<div style='text-align: center; margin-top: -10px; margin-bottom: 20px; color: #D8BFD8; font-size: 12px; letter-spacing: 3px; font-family: Cinzel;'>MYSTIC AI SYSTEM</div>", unsafe_allow_html=True)
    
    # Navigasi dengan warna Ungu/Pink
    selected = option_menu(
        menu_title=None,
        options=["Scanner Tanaman", "Ensiklopedia", "Laporan", "Pengaturan"],
        icons=["camera", "flower1", "clipboard-heart", "sliders"],
        menu_icon="cast",
        default_index=0,
        styles={
            "container": {"padding": "0!important", "background-color": "transparent"},
            "icon": {"color": "#FFB7B2", "font-size": "18px"},
            "nav-link": {"font-family": "Quicksand", "font-size": "15px", "text-align": "left", "margin":"5px", "--hover-color": "#2D1B4E", "color": "#E6E6FA"},
            "nav-link-selected": {"background-color": "rgba(255, 183, 178, 0.1)", "color": "#FFB7B2", "font-weight": "bold", "border-left": "3px solid #FFB7B2"},
        }
    )
    
    st.markdown("---")
    st.caption("SYSTEM STATUS")
    st.success("🟣 GPU: RTX 4060 [READY]")
    st.info("✨ Network: Secure")

# --- 4. FUNGSI GAMBAR GLOWING (PINK/UNGU EDITION) ---
def draw_mystic_box(img, pt1, pt2, color=(203, 192, 255), thickness=2): # Warna Pink/Ungu Pastel (BGR)
    x1, y1 = pt1
    x2, y2 = pt2
    r = 25 # Radius lebih besar biar elegan
    
    # Style Garis putus-putus atau double line elegan
    cv2.line(img, (x1, y1), (x1 + r, y1), color, thickness)
    cv2.line(img, (x1, y1), (x1, y1 + r), color, thickness)
    cv2.line(img, (x2, y1), (x2 - r, y1), color, thickness)
    cv2.line(img, (x2, y1), (x2, y1 + r), color, thickness)
    cv2.line(img, (x1, y2), (x1 + r, y2), color, thickness)
    cv2.line(img, (x1, y2), (x1, y2 - r), color, thickness)
    cv2.line(img, (x2, y2), (x2 - r, y2), color, thickness)
    cv2.line(img, (x2, y2), (x2, y2 - r), color, thickness)
    
    # Aksen Sudut Bercahaya (Putih)
    glow = (255, 255, 255)
    cv2.circle(img, (x1, y1), 2, glow, -1)
    cv2.circle(img, (x2, y1), 2, glow, -1)
    cv2.circle(img, (x1, y2), 2, glow, -1)
    cv2.circle(img, (x2, y2), 2, glow, -1)
    
    return img

def show_scanner_page():
    st.markdown("## 🌸 Mystic Night Scanner")
    
    # --- TOP BAR (CLEAN & RAPI dengan div class khusus) ---
    # Kita gunakan HTML murni untuk layout kotak info agar tidak kena style default Streamlit yang bikin kotak kosong
    
    col1, col2, col3 = st.columns(3)
    current_time = datetime.now().strftime("%H:%M WIB")

    with col1:
        st.markdown(f"""
            <div class="info-box-container">
                <span style="font-size: 11px; color: #FFB7B2; letter-spacing: 1px;">📍 LOKASI</span><br>
                <span style="font-weight: bold; font-size: 14px; color: #fff;">Greenhouse Utama</span>
            </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
            <div class="info-box-container">
                <span style="font-size: 11px; color: #E6E6FA; letter-spacing: 1px;">🕒 WAKTU</span><br>
                <span style="font-weight: bold; font-size: 14px; color: #fff;">{current_time}</span>
            </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown(f"""
            <div class="info-box-container">
                <span style="font-size: 11px; color: #FFB7B2; letter-spacing: 1px;">🌡️ SUHU</span><br>
                <span style="font-weight: bold; font-size: 14px; color: #fff;">24°C (Stabil)</span>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # --- AREA UTAMA ---
    col_vid, col_stat = st.columns([2, 1.2])
    
    with col_stat:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("### 🔮 Analisis Flora")
        
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("""
                <div class="metric-box">
                    <div class="metric-value">94%</div>
                    <div class="metric-label">AKURASI</div>
                </div>
            """, unsafe_allow_html=True)
        with c2:
            st.markdown("""
                <div class="metric-box" style="border-color: #FF6B6B; background: rgba(255, 107, 107, 0.1);">
                    <div class="metric-value" style="color: #FF6B6B; text-shadow: 0 0 10px rgba(255, 107, 107, 0.4);">TINGGI</div>
                    <div class="metric-label">RISIKO</div>
                </div>
            """, unsafe_allow_html=True)
            
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("#### 🥀 Terdeteksi:")
        st.warning("⚠️ **Karat Daun (Leaf Rust)**")
        
        with st.expander("✨ Saran Penyembuhan", expanded=True):
            st.write("1. Isolasi area yang terkena dampak.")
            st.write("2. Gunakan misting fungisida nabati.")
            st.write("3. Jaga kelembapan udara tetap stabil.")
        st.markdown('</div>', unsafe_allow_html=True)

    with col_vid:
        st.markdown('<div class="glass-card" style="padding: 10px;">', unsafe_allow_html=True)
        
        run_camera = st.toggle("🌸 Aktifkan Mata Dewi", value=True)
        
        image_placeholder = st.image([])
        cap = cv2.VideoCapture(0)
        
        while run_camera:
            ret, frame = cap.read()
            if not ret:
                st.error("Kamera tidak terdeteksi.")
                break
            
            # Efek Gelap + Sedikit Ungu (Mystic Filter)
            # Kita buat frame agak keunguan sedikit biar nyatu sama tema
            frame = cv2.convertScaleAbs(frame, alpha=0.85, beta=-10)
            
            # Mocking Logic
            h, w, _ = frame.shape
            start_point = (150, 100)
            end_point = (500, 400)
            
            # Warna Box: Pink Pastel (BGR: 203, 192, 255)
            draw_mystic_box(frame, start_point, end_point, color=(203, 192, 255), thickness=2)
            
            text = "Leaf Rust :: 94%"
            # Background Label: Ungu Gelap Transparan
            cv2.rectangle(frame, (start_point[0], start_point[1]-35), (start_point[0] + 220, start_point[1]-5), (45, 27, 78), -1)
            # Text: Putih
            cv2.putText(frame, text, (start_point[0]+10, start_point[1]-12), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
            
            # Animasi Garis Scan (Ungu Neon)
            t = time.time()
            scan_y = int(start_point[1] + (np.sin(t*1.5)+1)/2 * (end_point[1]-start_point[1]))
            cv2.line(frame, (start_point[0], scan_y), (end_point[0], scan_y), (255, 0, 255), 2) # Magenta Neon
            
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            # FIX: Menggunakan width='stretch'
            image_placeholder.image(frame, channels="RGB", width='stretch')
        
        cap.release()
        st.markdown('</div>', unsafe_allow_html=True)

# --- 5. ROUTING ---
if selected == "Scanner Tanaman":
    show_scanner_page()
elif selected == "Ensiklopedia":
    st.title("📚 Grimoire Tanaman")
    st.info("Modul Ensiklopedia sedang disiapkan.")
elif selected == "Laporan":
    st.title("📄 Jurnal Kesehatan")
    st.info("Modul Laporan sedang disiapkan.")
elif selected == "Pengaturan":
    st.title("⚙️ Konfigurasi Mantra")
    st.info("Modul Pengaturan sedang disiapkan.")