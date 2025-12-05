import streamlit as st
import cv2
import numpy as np
import time
import os
from datetime import datetime
from streamlit_option_menu import option_menu

# --- 1. KONFIGURASI HALAMAN ---
st.set_page_config(
    page_title="Chloris: Night Bloom",
    page_icon="🌸",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. CSS INJECTION (DARK GLOWING THEME) ---
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700&family=Montserrat:wght@300;400;600&display=swap');

        /* BACKGROUND: Deep Jungle Night */
        .stApp {
            background-color: #0a0f0d;
            background-image: radial-gradient(circle at 50% 0%, #1a2f23 0%, #0a0f0d 80%);
            color: #e0f2f1;
        }

        /* TYPOGRAPHY */
        h1, h2, h3 {
            font-family: 'Playfair Display', serif;
            color: #A8E890 !important; /* Mint Neon */
            text-shadow: 0 0 10px rgba(168, 232, 144, 0.3);
        }
        p, div, label, span {
            font-family: 'Montserrat', sans-serif;
            color: #d1e7dd;
        }

        /* GLASS CARD (Kotak Kaca) */
        .glass-card {
            background: rgba(20, 30, 25, 0.6);
            backdrop-filter: blur(12px);
            border-radius: 20px;
            border: 1px solid rgba(168, 232, 144, 0.15);
            padding: 20px;
            margin-bottom: 20px;
            box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.5);
            transition: transform 0.3s ease, box-shadow 0.3s ease, border-color 0.3s;
        }
        .glass-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 0 25px rgba(168, 232, 144, 0.2);
            border-color: rgba(168, 232, 144, 0.6); /* Border menyala saat hover */
        }

        /* TOP INFO BAR (Kotak Kecil di Atas) */
        .info-box {
            background: rgba(255, 255, 255, 0.05);
            border-radius: 12px;
            padding: 10px;
            text-align: center;
            border: 1px solid rgba(255,255,255,0.1);
            transition: 0.3s;
        }
        .info-box:hover {
            background: rgba(168, 232, 144, 0.1);
            border-color: #A8E890;
        }

        /* METRIC BOX */
        .metric-box {
            text-align: center;
            padding: 15px;
            border-radius: 15px;
            background: linear-gradient(145deg, rgba(255, 255, 255, 0.05), rgba(255, 255, 255, 0.02));
            border: 1px solid rgba(255, 182, 193, 0.2);
            margin-bottom: 10px;
        }
        .metric-value {
            font-family: 'Montserrat', sans-serif;
            font-size: 26px;
            font-weight: bold;
            color: #FFB7B2;
            text-shadow: 0 0 8px rgba(255, 183, 178, 0.4);
        }
        .metric-label {
            font-size: 12px; color: #a3b1a8; letter-spacing: 1px; text-transform: uppercase;
        }

        /* SIDEBAR */
        section[data-testid="stSidebar"] {
            background-color: #050806;
            border-right: 1px solid rgba(168, 232, 144, 0.1);
        }
        
        /* TOMBOL */
        .stButton button {
            background: linear-gradient(90deg, #4A6B5A, #2F5242);
            color: #A8E890;
            font-weight: 600;
            border: 1px solid #4A6B5A;
            border-radius: 12px;
            padding: 0.5rem 1rem;
            transition: 0.3s;
        }
        .stButton button:hover {
            background: linear-gradient(90deg, #A8E890, #4A6B5A);
            color: #0a0f0d;
            box-shadow: 0 0 20px rgba(168, 232, 144, 0.6);
            border-color: #A8E890;
        }
    </style>
""", unsafe_allow_html=True)

# --- 3. SIDEBAR & LOGO (YANG DIPERBESAR) ---
with st.sidebar:
    logo_path = "src\image\chloris_logo-removebg.png"
    
    if os.path.exists(logo_path):
        # HAPUS KOLOM PEMBATAS AGAR LOGO BESAR
        st.image(logo_path, width='stretch') 
    else:
        st.title("CHLORIS")

    st.markdown("<div style='text-align: center; margin-top: -10px; margin-bottom: 20px; color: #888; font-size: 12px; letter-spacing: 2px;'>LUMINOUS AI SYSTEM</div>", unsafe_allow_html=True)
    
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

# --- 4. FUNGSI GAMBAR GLOWING ---
def draw_glowing_box(img, pt1, pt2, color=(144, 232, 168), thickness=2):
    x1, y1 = pt1
    x2, y2 = pt2
    r = 20 
    
    cv2.line(img, (x1, y1), (x1 + r, y1), color, thickness)
    cv2.line(img, (x1, y1), (x1, y1 + r), color, thickness)
    cv2.line(img, (x2, y1), (x2 - r, y1), color, thickness)
    cv2.line(img, (x2, y1), (x2, y1 + r), color, thickness)
    cv2.line(img, (x1, y2), (x1 + r, y2), color, thickness)
    cv2.line(img, (x1, y2), (x1, y2 - r), color, thickness)
    cv2.line(img, (x2, y2), (x2 - r, y2), color, thickness)
    cv2.line(img, (x2, y2), (x2, y2 - r), color, thickness)
    
    # Titik sudut bercahaya
    glow_color = (255, 255, 255)
    cv2.circle(img, (x1, y1), 3, glow_color, -1)
    cv2.circle(img, (x2, y1), 3, glow_color, -1)
    cv2.circle(img, (x1, y2), 3, glow_color, -1)
    cv2.circle(img, (x2, y2), 3, glow_color, -1)
    return img

def show_scanner_page():
    # Header
    st.markdown("## 🌿 Night Vision Scanner")
    
    # --- TOP BAR (Kotak yang tadinya kosong, sekarang kita isi) ---
    # Ini memanfaatkan "hover box" yang kamu suka tadi
    
    info1, info2, info3 = st.columns(3)
    with info1:
        st.markdown("""
        <div class="glass-card" style="padding: 10px; text-align: center; margin-bottom: 10px;">
            <span style="font-size: 12px; color: #A8E890;">📍 LOKASI</span><br>
            <span style="font-weight: bold;">Greenhouse A</span>
        </div>
        """, unsafe_allow_html=True)
    with info2:
        current_time = datetime.now().strftime("%H:%M WIB")
        st.markdown(f"""
        <div class="glass-card" style="padding: 10px; text-align: center; margin-bottom: 10px;">
            <span style="font-size: 12px; color: #FFB7B2;">🕒 WAKTU</span><br>
            <span style="font-weight: bold;">{current_time}</span>
        </div>
        """, unsafe_allow_html=True)
    with info3:
        st.markdown("""
        <div class="glass-card" style="padding: 10px; text-align: center; margin-bottom: 10px;">
            <span style="font-size: 12px; color: #A8E890;">🌡️ SUHU</span><br>
            <span style="font-weight: bold;">24°C (Optimal)</span>
        </div>
        """, unsafe_allow_html=True)
    
    # --- AREA UTAMA ---
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
            
            # Efek Gelap (Night Vision)
            frame = cv2.convertScaleAbs(frame, alpha=0.8, beta=0) 

            h, w, _ = frame.shape
            start_point = (150, 100)
            end_point = (500, 400)
            
            draw_glowing_box(frame, start_point, end_point, color=(144, 232, 168), thickness=2)
            
            text = "Leaf Rust :: 92%"
            cv2.rectangle(frame, (start_point[0], start_point[1]-30), (start_point[0] + 200, start_point[1]-5), (20, 30, 25), -1)
            cv2.putText(frame, text, (start_point[0]+10, start_point[1]-12), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (168, 232, 144), 1)
            
            t = time.time()
            scan_y = int(start_point[1] + (np.sin(t*2)+1)/2 * (end_point[1]-start_point[1]))
            cv2.line(frame, (start_point[0], scan_y), (end_point[0], scan_y), (178, 183, 255), 2)
            
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image_placeholder.image(frame, channels="RGB", width='stretch')
        
        cap.release()
        st.markdown('</div>', unsafe_allow_html=True)

# --- 5. ROUTING ---
if selected == "Scanner Tanaman":
    show_scanner_page()
elif selected == "Ensiklopedia":
    st.title("📚 Ensiklopedia Digital")
    st.info("Halaman dalam pengembangan.")
elif selected == "Laporan":
    st.title("📄 Laporan")
    st.info("Halaman dalam pengembangan.")
elif selected == "Pengaturan":
    st.title("⚙️ Pengaturan")
    st.info("Halaman dalam pengembangan.")