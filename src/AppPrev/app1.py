import streamlit as st
import cv2
import numpy as np
import time
from streamlit_option_menu import option_menu

# --- 1. KONFIGURASI HALAMAN (Wajib Paling Atas) ---
st.set_page_config(
    page_title="Chloris AI Command Center",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. CSS INJECTION (RAHASIA TAMPILAN KEREN) ---
# Kita paksa Streamlit pakai gaya kita sendiri (Dark Mode & Neon)
st.markdown("""
    <style>
        /* Import Font Keren (Orbitron untuk kesan Sci-Fi) */
        @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Roboto:wght@300;400&display=swap');

        /* Background Utama Gelap Elegan */
        .stApp {
            background-color: #050505;
            background-image: radial-gradient(circle at 50% 50%, #112211 0%, #050505 100%);
        }

        /* Judul Neon */
        h1, h2, h3 {
            font-family: 'Orbitron', sans-serif;
            color: #00FFA3 !important;
            text-shadow: 0 0 10px #00FFA3;
        }
        
        p, div, label, span {
            font-family: 'Roboto', sans-serif;
            color: #E0E0E0;
        }

        /* KARTU GLASSMORPHISM (Efek Kaca Transparan) */
        .glass-card {
            background: rgba(255, 255, 255, 0.05);
            backdrop-filter: blur(10px);
            -webkit-backdrop-filter: blur(10px);
            border-radius: 15px;
            border: 1px solid rgba(255, 255, 255, 0.1);
            padding: 20px;
            margin-bottom: 20px;
            box-shadow: 0 4px 30px rgba(0, 0, 0, 0.5);
        }

        /* Kotak Metrik Kustom */
        .metric-box {
            text-align: center;
            padding: 10px;
            border-radius: 10px;
            background: rgba(0, 255, 163, 0.1);
            border: 1px solid #00FFA3;
            margin-bottom: 10px;
        }
        .metric-value {
            font-family: 'Orbitron', sans-serif;
            font-size: 24px;
            font-weight: bold;
            color: #fff;
        }
        .metric-label {
            font-size: 12px;
            color: #aaa;
        }

        /* Sidebar Styling */
        section[data-testid="stSidebar"] {
            background-color: #0a0a0a;
            border-right: 1px solid #222;
        }
        
        /* Tombol Keren */
        .stButton button {
            background: linear-gradient(45deg, #00FFA3, #008F5B);
            color: black;
            font-weight: bold;
            border: none;
            border-radius: 5px;
            transition: 0.3s;
            width: 100%;
        }
        .stButton button:hover {
            transform: scale(1.05);
            box-shadow: 0 0 15px #00FFA3;
            color: white;
        }
    </style>
""", unsafe_allow_html=True)

# --- 3. NAVIGASI SIDEBAR ---
with st.sidebar:
    # Logo Text Custom
    st.markdown("<h1 style='text-align: center; margin-bottom: 0;'>CHLORIS</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size: 12px; color: #00FFA3; letter-spacing: 2px;'>AI SYSTEM ONLINE</p>", unsafe_allow_html=True)
    st.markdown("---")
    
    selected = option_menu(
        menu_title=None,
        options=["Dashboard Scanner", "Database Penyakit", "Laporan", "Settings"],
        icons=["qr-code-scan", "database", "file-earmark-text", "gear"],
        menu_icon="cast",
        default_index=0,
        styles={
            "container": {"padding": "0!important", "background-color": "transparent"},
            "icon": {"color": "#00FFA3", "font-size": "18px"}, 
            "nav-link": {"font-size": "14px", "text-align": "left", "margin":"5px", "--hover-color": "#222"},
            "nav-link-selected": {"background-color": "#00FFA3", "color": "black", "font-weight": "bold"},
        }
    )
    
    st.markdown("---")
    st.caption("SYSTEM STATUS")
    st.success("🟢 GPU: RTX 4060 (Active)")
    st.success("🟢 Connection: Stable")

# --- 4. FUNGSI GAMBAR ESTETIK (TECHY BOX) ---
def draw_tech_box(img, pt1, pt2, color=(0, 255, 163), thickness=2):
    """Fungsi bikin kotak deteksi yang aesthetic (hanya sudut-sudutnya)"""
    x1, y1 = pt1
    x2, y2 = pt2
    l = 30 # Panjang garis sudut
    
    # Sudut Kiri Atas
    cv2.line(img, (x1, y1), (x1 + l, y1), color, thickness)
    cv2.line(img, (x1, y1), (x1, y1 + l), color, thickness)
    # Sudut Kanan Atas
    cv2.line(img, (x2, y1), (x2 - l, y1), color, thickness)
    cv2.line(img, (x2, y1), (x2, y1 + l), color, thickness)
    # Sudut Kiri Bawah
    cv2.line(img, (x1, y2), (x1 + l, y2), color, thickness)
    cv2.line(img, (x1, y2), (x1, y2 - l), color, thickness)
    # Sudut Kanan Bawah
    cv2.line(img, (x2, y2), (x2 - l, y2), color, thickness)
    cv2.line(img, (x2, y2), (x2, y2 - l), color, thickness)
    return img

def show_scanner():
    # Header Halaman
    st.markdown("## 📡 Live Diagnostic Feed")
    st.markdown("Real-time plant disease detection protocol initiated.")
    
    col_video, col_stats = st.columns([2.5, 1.2])

    with col_stats:
        # --- PANEL KANAN (STATISTIK) ---
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("### 📊 Analysis Metrics")
        
        # Dummy Metrics (Placeholder Animasi)
        m1, m2 = st.columns(2)
        with m1:
            st.markdown("""
                <div class="metric-box">
                    <div class="metric-value">88.4%</div>
                    <div class="metric-label">CONFIDENCE</div>
                </div>
            """, unsafe_allow_html=True)
        with m2:
            st.markdown("""
                <div class="metric-box" style="border-color: #FF4B4B; background: rgba(255, 75, 75, 0.1);">
                    <div class="metric-value" style="color: #FF4B4B;">HIGH</div>
                    <div class="metric-label">SEVERITY</div>
                </div>
            """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("### 🧬 Detected Pathogen")
        st.warning("⚠️ **Pucciniales (Leaf Rust)**")
        st.caption("Fungal disease affecting leaves.")
        
        st.markdown("### 🛠️ Action Plan")
        with st.expander("Lihat Rekomendasi AI", expanded=True):
            st.markdown("""
            1. **Isolasi:** Pisahkan tanaman sakit dari yang sehat.
            2. **Fungisida:** Semprot fungisida berbahan aktif Azoxystrobin.
            3. **Lingkungan:** Kurangi kelembapan udara sekitar.
            """)
        st.markdown('</div>', unsafe_allow_html=True)

    with col_video:
        # --- PANEL KIRI (VIDEO) ---
        st.markdown('<div class="glass-card" style="padding: 10px;">', unsafe_allow_html=True)
        
        # Toggle Switch Modern
        run = st.toggle('🔴 ACTIVATE OPTICAL SENSOR', value=True)
        
        frame_window = st.image([])
        
        # Inisialisasi Kamera
        cam = cv2.VideoCapture(0) 
        
        while run:
            ret, frame = cam.read()
            if not ret:
                st.error("Camera Offline or Not Found.")
                break
            
            # --- ZONA MOCKING AI (VISUAL EFEK) ---
            # 1. Efek Gelap Sedikit (Vignette/Tech Feel)
            rows, cols, _ = frame.shape
            # (Optional: Bisa tambah efek overlay di sini)

            # 2. Gambar Kotak Techy (Bukan kotak biasa)
            # Koordinat pura-pura (Nanti diganti hasil AI beneran)
            box_start = (150, 100)
            box_end = (490, 380)
            
            draw_tech_box(frame, box_start, box_end)
            
            # 3. Label Techy
            cv2.putText(frame, "TARGET: LEAF_RUST [CONF: 0.88]", (box_start[0], box_start[1]-10), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 163), 2)
            
            # 4. Animasi Garis Scan (Naik Turun)
            t = time.time()
            scan_y = int(box_start[1] + (np.sin(t * 3) + 1) / 2 * (box_end[1] - box_start[1]))
            cv2.line(frame, (box_start[0], scan_y), (box_end[0], scan_y), (0, 255, 163), 2)
            # -------------------------------------

            # Convert warna BGR ke RGB buat Streamlit
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            # Tampilkan
            frame_window.image(frame, channels="RGB", use_container_width=True)
        
        cam.release()
        st.markdown('</div>', unsafe_allow_html=True)


# --- 5. MAIN ROUTING ---
if selected == "Dashboard Scanner":
    show_scanner()
elif selected == "Database Penyakit":
    st.title("📚 Database Pathogen")
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Dataset", "2,450", "+120")
    col2.metric("Kelas Penyakit", "15", "Active")
    col3.metric("Last Update", "Today", "10:00 AM")
elif selected == "Settings":
    st.title("⚙️ System Configuration")
    st.text_input("Camera ID", "0")
    st.slider("Confidence Threshold", 0.0, 1.0, 0.5)
    st.checkbox("Enable Dark Mode", True, disabled=True)