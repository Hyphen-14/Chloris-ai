import streamlit as st
import cv2
import time
import numpy as np
import json
from datetime import datetime
from pathlib import Path
import tempfile
import os
from dotenv import load_dotenv
import uuid

# Load environment variables
load_dotenv()

def show_scanner_page():
    """Scanner dengan mapping penyakit"""
    if 'widget_counter' not in st.session_state:
        st.session_state.widget_counter = 0

# Di setiap widget:
    st.session_state.widget_counter += 1
    confidence = st.slider(
    "Confidence Threshold",
    min_value=0.1,
    max_value=0.9,
    value=0.3,
    step=0.1,
    key=f"confidence_{st.session_state.widget_counter}"  # Key unik
)
    # Cek API key
    if not _check_api_key():
        return
    
    st.markdown("<h1 style='text-align: center; color: #A8E890;'>🌿 PLANT DISEASE DIAGNOSIS</h1>", 
                unsafe_allow_html=True)
    
    # Tambahkan test button di sidebar (hanya untuk debugging)
    if st.session_state.get('debug_mode', False):
        with st.sidebar:
            if st.button("🧪 Run Mapping Test"):
                test_disease_mapping()
    
    _show_system_info()
    _initialize_session_state()
    
    # Mode selection
    mode = st.radio(
        "Pilih Mode:",
        ["📷 Camera Real-time", "📁 Upload Image"],
        horizontal=True
    )
    
    _show_settings_panel()
    
    col_main, col_analytics = st.columns([2, 1])
    
    with col_main:
        if "Camera" in mode:
            _show_camera_mode_with_settings()
        else:
            _show_upload_mode_with_settings()
    
    with col_analytics:
        _show_analytics_section()
    
    # Footer dengan info database
    st.markdown("---")
    st.caption(f"🌱 **Plant Disease Database:** {len(_load_disease_database())} penyakit tercatat")
    
    # ✅ FIX 1: PANGGIL SETTINGS PANEL
def _show_settings_panel():
    """Show settings panel di sidebar - FIXED dengan key unik"""
    with st.sidebar:
        st.markdown("### ⚙️ Detection Settings")
        
        # Confidence threshold dengan KEY UNIK
        confidence = st.slider(
            "Confidence Threshold",
            min_value=0.1,
            max_value=0.9,
            value=st.session_state.get('confidence_threshold', 0.3),
            step=0.1,
            help="Threshold minimum untuk deteksi (semakin rendah, semakin sensitif)",
            key="scanner_confidence_slider"  # ✅ TAMBAHKAN KEY UNIK
        )
        st.session_state.confidence_threshold = confidence
        
        # Overlap threshold dengan KEY UNIK
        overlap = st.slider(
            "Overlap Threshold (IOU)",
            min_value=0.1,
            max_value=0.9,
            value=st.session_state.get('overlap_threshold', 0.5),
            step=0.1,
            help="Threshold untuk Non-Maximum Suppression (semakin tinggi, semakin sedikit overlap)",
            key="scanner_overlap_slider"  # ✅ TAMBAHKAN KEY UNIK
        )
        st.session_state.overlap_threshold = overlap
        
        # Inference interval dengan KEY UNIK
        interval = st.slider(
            "Inference Interval (detik)",
            min_value=1,
            max_value=10,
            value=st.session_state.get('inference_interval', 3),
            step=1,
            help="Interval antara analisis frame (untuk performance)",
            key="scanner_interval_slider"  # ✅ TAMBAHKAN KEY UNIK
        )
        st.session_state.inference_interval = interval
        
        st.markdown("---")
        
        # Debug mode dengan KEY UNIK
        debug_mode = st.checkbox(
            "🐛 Debug Mode", 
            value=st.session_state.get('debug_mode', False),
            key="scanner_debug_checkbox"  # ✅ TAMBAHKAN KEY UNIK
        )
        st.session_state.debug_mode = debug_mode
        
        st.markdown("---")
        
        # Model info
        st.markdown("**Model Info:**")
        st.code("crop-disease-identification-dniia/2")
        
        # Status
        if st.session_state.get('camera_active', False):
            st.success("🔴 Camera LIVE")
        else:
            st.info("📷 Camera Ready")

def _check_api_key():
    """Check if API key is available"""
    api_key = os.getenv("ROBOFLOW_API_KEY")
    
    if not api_key or api_key == "your_actual_api_key_here":
        st.error("""
        ❌ **ROBOFLOW API KEY TIDAK DITEMUKAN**
        
        **Langkah penyelesaian:**
        
        1. **Dapatkan API Key:**
           - Login ke [Roboflow](https://app.roboflow.com)
           - Klik profile picture → Account Settings
           - Copy API Key dari bagian "Roboflow API Key"
        
        2. **Setup API Key:**
           - Buat file `.env` di folder project
           - Tambahkan: `ROBOFLOW_API_KEY=your_actual_key_here`
           - Ganti `your_actual_key_here` dengan API key Anda
        
        3. **Restart aplikasi**
        """)
        
        with st.expander("🔧 Advanced Setup", expanded=False):
            st.code("""
# Cara alternatif - langsung set di kode (tidak disarankan untuk production)
import os
os.environ["ROBOFLOW_API_KEY"] = "your_key_here"
            """)
            
            manual_key = st.text_input("Atau masukkan API key manual:", type="password")
            if manual_key:
                os.environ["ROBOFLOW_API_KEY"] = manual_key
                st.success("✅ API key disimpan! Refresh halaman.")
                st.rerun()
        
        return False
    
    # Tampilkan status API key di sidebar
    with st.sidebar:
        st.success(f"✅ API Key: {api_key[:8]}...{api_key[-4:]}")
    
    return True

# ✅ FIX 3: HAPUS DUPLIKAT - HANYA 1 DEFINISI
def _show_settings_panel():
    """Show settings panel di sidebar"""
    with st.sidebar:
        st.markdown("### ⚙️ Detection Settings")
        
        # Confidence threshold
        confidence = st.slider(
            "Confidence Threshold",
            min_value=0.1,
            max_value=0.9,
            value=0.3,
            step=0.1,
            help="Threshold minimum untuk deteksi (semakin rendah, semakin sensitif)"
        )
        st.session_state.confidence_threshold = confidence
        
        # Overlap threshold
        overlap = st.slider(
            "Overlap Threshold (IOU)",
            min_value=0.1,
            max_value=0.9,
            value=0.5,
            step=0.1,
            help="Threshold untuk Non-Maximum Suppression (semakin tinggi, semakin sedikit overlap)"
        )
        st.session_state.overlap_threshold = overlap
        
        # Inference interval
        interval = st.slider(
            "Inference Interval (detik)",
            min_value=1,
            max_value=10,
            value=3,
            step=1,
            help="Interval antara analisis frame (untuk performance)"
        )
        st.session_state.inference_interval = interval
        
        st.markdown("---")
        
        # Debug mode
        debug_mode = st.checkbox("🐛 Debug Mode", value=False)
        st.session_state.debug_mode = debug_mode
        
        st.markdown("---")
        
        # Model info
        st.markdown("**Model Info:**")
        st.code("crop-disease-identification-dniia/2")
        
        # Status
        if st.session_state.get('camera_active', False):
            st.success("🔴 Camera LIVE")
        else:
            st.info("📷 Camera Ready")

def _show_camera_mode_with_settings():
    """Camera mode dengan settings - FIXED dengan key unik"""
    st.markdown("### 📷 Real-time Camera Detection")
    
    with st.container():
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        
        # Status dan toggle
        col_status, col_toggle = st.columns([2, 1])
        
        with col_status:
            if st.session_state.get('camera_active', False):
                st.success("✅ **Camera LIVE - Sedang menganalisis**")
            else:
                st.info("🎯 **Camera Ready - Toggle untuk memulai**")
        
        with col_toggle:
            camera_active = st.toggle(
                "🎥 Live Camera", 
                value=st.session_state.get('camera_active', False),
                key="camera_toggle_unique"  # ✅ GANTI KEY UNIK
            )
            st.session_state.camera_active = camera_active
        
        # Settings display
        if st.session_state.get('camera_active', False):
            st.info(f"""
            **Settings Aktif:**
            - Confidence: `{st.session_state.get('confidence_threshold', 0.3)}`
            - Overlap: `{st.session_state.get('overlap_threshold', 0.5)}`  
            - Interval: `{st.session_state.get('inference_interval', 3)}s`
            """)
        
        # Camera feed
        if st.session_state.get('camera_active', False):
            _run_camera_with_settings()
        else:
            _show_camera_placeholder()
        
        st.markdown('</div>', unsafe_allow_html=True)

def _run_camera_with_settings():
    """Run camera dengan settings"""
    cap = cv2.VideoCapture(0)
    
    # Fallback ke camera index 1 jika 0 tidak work
    if not cap.isOpened():
        cap = cv2.VideoCapture(1)
    
    if not cap.isOpened():
        st.error("❌ Tidak dapat mengakses camera!")
        st.session_state.camera_active = False
        return
    
    # Apply camera settings
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    cap.set(cv2.CAP_PROP_FPS, 20)
    
    # Placeholders
    video_placeholder = st.empty()
    status_placeholder = st.empty()
    stats_placeholder = st.empty()
    
    frame_count = 0
    last_inference_time = 0
    detection_count = 0
    
    try:
        while st.session_state.get('camera_active', False):
            ret, frame = cap.read()
            if not ret:
                status_placeholder.error("❌ Gagal membaca frame")
                break
            
            frame_count += 1
            
            # Convert untuk display
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            # Display frame
            video_placeholder.image(
                frame_rgb, 
                caption=f"🎥 Live Frame {frame_count}",
                width="stretch"
            )
            
            # Run inference berdasarkan interval settings
            current_time = time.time()
            inference_interval = st.session_state.get('inference_interval', 3)
            
            if current_time - last_inference_time > inference_interval:
                status_placeholder.info("🔍 Menganalisis frame...")
                
                try:
                    # Get settings
                    confidence = st.session_state.get('confidence_threshold', 0.3)
                    overlap = st.session_state.get('overlap_threshold', 0.5)
                    
                    # Run inference dengan settings
                    detection_info = _sdk_inference_with_settings(frame, confidence, overlap)
                    
                    if detection_info:
                        _update_detection_state(detection_info)
                        detection_count += 1
                        status_placeholder.success(f"✅ Terdeteksi: {detection_info['nama_id']}")
                    else:
                        status_placeholder.warning("⚠️ Tidak terdeteksi")
                        
                except Exception as e:
                    status_placeholder.error(f"❌ Analisis gagal: {e}")
                
                last_inference_time = current_time
            
            # Update stats
            stats_placeholder.info(f"""
            **📊 Stats:**
            - Frames: `{frame_count}`
            - Detections: `{detection_count}`
            - Confidence: `{st.session_state.get('confidence_threshold', 0.3)}`
            - Next analysis: `{max(0, inference_interval - (current_time - last_inference_time)):.1f}s`
            """)
            
            time.sleep(0.03)  # Smooth video
            
    except Exception as e:
        st.error(f"❌ Camera error: {e}")
    finally:
        # Cleanup
        cap.release()
        video_placeholder.empty()
        status_placeholder.empty()
        stats_placeholder.empty()

def _sdk_inference_with_settings(frame, confidence_threshold, overlap_threshold):
    """FIXED: Instance Segmentation Model"""
    try:
        from roboflow import Roboflow
        
        api_key = os.getenv("ROBOFLOW_API_KEY")
        rf = Roboflow(api_key=api_key)
        project = rf.workspace("xof").project("crop-disease-identification-dniia")
        model = project.version(2).model
        
        # Resize untuk instance segmentation
        target_size = st.session_state.get('processing_size', 640)
        frame_resized = cv2.resize(frame, (target_size, target_size))
        
        # Save
        temp_path = "temp_instance_seg.jpg"
        cv2.imwrite(temp_path, frame_resized)
        
        # ✅ FIX: Hanya confidence, NO OVERLAP
        results = model.predict(
            temp_path,
            confidence=int(confidence_threshold * 100)  # Integer 0-100
        ).json()
        
        # Cleanup
        if os.path.exists(temp_path):
            os.remove(temp_path)
        
        # 🐛 DEBUG
        if st.session_state.get('debug_mode', True):  # Always show debug
            with st.sidebar.expander("🔍 INSTANCE SEG RESULTS", expanded=True):
                st.json(results)
        
        # Extract predictions
        predictions = []
        if isinstance(results, dict):
            if 'predictions' in results:
                predictions = results['predictions']
            elif 'prediction' in results:
                predictions = results['prediction']
        
        if not predictions:
            return None
        
        # Get best
        best_pred = max(predictions, key=lambda x: x.get('confidence', 0))
        best_class = best_pred.get('class', 'unknown').replace('_', ' ').title()
        best_conf = best_pred.get('confidence', 0)
        
        if best_conf > 1:
            best_conf = best_conf / 100.0
        
        return {
            'confidence': best_conf,
            'nama_id': best_class,
            'tingkat_bahaya': 'Medium',
            'solusi': ['Analisis instance segmentation berhasil']
        }
        
    except Exception as e:
        st.error(f"Instance Seg Error: {str(e)}")
        return None

def _show_upload_mode_with_settings():
    """Upload mode dengan settings - FIXED dengan key unik"""
    st.markdown("### 📁 Upload Image Analysis")
    
    with st.container():
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        
        st.success("✅ **Upload Mode**")
        
        # Upload section
        uploaded_file = st.file_uploader(
            "Pilih gambar tanaman:",
            type=['jpg', 'jpeg', 'png', 'bmp'],
            help="Upload gambar daun/tanaman untuk dianalisis",
            key="scanner_upload_file"  # ✅ TAMBAHKAN KEY UNIK
        )
        
        if uploaded_file is not None:
            # Display preview
            st.image(uploaded_file, caption="📸 Gambar Preview", width="stretch")
            
            # Analysis settings untuk upload
            st.markdown("#### ⚙️ Analysis Settings")
            col_conf, col_overlap = st.columns(2)
            
            with col_conf:
                upload_confidence = st.slider(
                    "Confidence",
                    0.1, 0.9, 0.3, 0.1,
                    key="upload_confidence_slider"  # ✅ SUDAH ADA KEY
                )
            
            with col_overlap:
                upload_overlap = st.slider(
                    "Overlap",
                    0.1, 0.9, 0.5, 0.1,
                    key="upload_overlap_slider"  # ✅ SUDAH ADA KEY
                )
            
            # Analyze button dengan KEY UNIK
            if st.button("🔍 ANALYZE IMAGE", type="primary", width="stretch", key="upload_analyze_button"):
                with st.spinner("🔄 Menganalisis dengan AI..."):
                    detection_info = _process_upload_with_settings(
                        uploaded_file, upload_confidence, upload_overlap
                    )
                    _update_detection_state(detection_info)
                
                # Show results
                if detection_info:
                    st.success(f"✅ **{detection_info['nama_id']}** terdeteksi!")
                    st.metric("Confidence", f"{detection_info['confidence']:.1%}")
                else:
                    st.warning("⚠️ Tidak terdeteksi penyakit tanaman")
                    
                    # Suggestion
                    st.info("""
                    **💡 Tips untuk deteksi lebih baik:**
                    - Gunakan confidence threshold lebih rendah
                    - Pastikan gambar fokus pada daun/tanaman
                    - Coba gambar dengan pencahayaan lebih baik
                    """)
        
        else:
            _show_upload_placeholder()
        
        st.markdown('</div>', unsafe_allow_html=True)

def _process_upload_with_settings(uploaded_file, confidence, overlap):
    """Process upload dengan settings"""
    try:
        # Convert uploaded file to numpy array
        file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
        image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
        
        # 🎯 DEBUG: Tampilkan info gambar
        if st.session_state.get('debug_mode', False):
            st.sidebar.write(f"Image shape: {image.shape}")
            st.sidebar.write(f"Image dtype: {image.dtype}")
        
        # Run inference
        detection_info = _sdk_inference_with_settings(image, confidence, overlap)
        
        return detection_info
        
    except Exception as e:
        st.error(f"❌ Upload processing error: {e}")
        import traceback
        st.code(traceback.format_exc())
        return None
        
    except Exception as e:
        st.error(f"❌ Upload processing error: {e}")
        return None

def _show_upload_placeholder():
    """Show upload placeholder"""
    st.info("📁 **Upload gambar tanaman untuk analisis**")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.image(
            "https://via.placeholder.com/150/1a2f23/A8E890?text=Daun\nSehat",
            caption="Daun Sehat"
        )
    
    with col2:
        st.image(
            "https://via.placeholder.com/150/1a2f23/A8E890?text=Daun\nSakit", 
            caption="Daun Sakit"
        )
    
    with col3:
        st.image(
            "https://via.placeholder.com/150/1a2f23/A8E890?text=Tanaman\nUtuh",
            caption="Tanaman Utuh"
        )
    
    st.markdown("""
    **📸 Contoh gambar yang bisa dianalisis:**
    - Daun dengan gejala penyakit
    - Tanaman dengan bercak/spot
    - Bagian tanaman yang tidak sehat
    - Perbandingan daun sehat & sakit
    """)

def _show_camera_placeholder():
    """Show camera placeholder"""
    st.info("🎯 **Toggle 'Live Camera' untuk memulai real-time detection**")
    
    # Camera illustration
    st.image(
        "https://via.placeholder.com/400x250/0a0f0d/A8E890?text=LIVE+CAMERA+READY%0A%0AToggle+Above+to+Start%0A%0A⚙️+Settings+in+Sidebar",
        width="stretch"
    )
    
    # Quick tips
    with st.expander("💡 Tips Camera Terbaik", expanded=False):
        st.markdown("""
        **Untuk hasil terbaik:**
        - 🎯 **Fokus** pada daun/tanaman
        - 💡 **Pencahayaan** cukup (tidak gelap/silau)
        - 📏 **Jarak** optimal 20-50 cm
        - 🌿 **Background** sederhana
        - ⚙️ **Adjust confidence** di sidebar jika perlu
        """)

def _map_to_disease_database(class_name, confidence):
    """Map dengan debug info"""
    disease_db = _load_disease_database()
    
    # Debug info
    if st.session_state.get('debug_mode', False):
        with st.sidebar.expander("🗺️ DEBUG MAPPING", expanded=True):
            st.write(f"Class dari model: '{class_name}'")
            st.write(f"Keys dalam database: {list(disease_db.keys())[:5]}...")
    
    # 1. Exact match
    if class_name in disease_db:
        info = disease_db[class_name].copy()
        info['confidence'] = confidence
        st.sidebar.success(f"✅ Exact match: {class_name}")
        return info
    
    # 2. Coba dengan formatting yang berbeda
    # Ganti underscore dengan dash atau sebaliknya
    variations = [
        class_name,
        class_name.replace('_', '-'),
        class_name.replace('-', '_'),
        class_name.replace(' ', '-'),
        class_name.replace(' ', '_')
    ]
    
    for var in variations:
        if var in disease_db:
            info = disease_db[var].copy()
            info['confidence'] = confidence
            st.sidebar.success(f"✅ Match dengan variasi: {var}")
            return info
    
    # 3. Cari partial match
    for key in disease_db.keys():
        if class_name.lower() in key.lower() or key.lower() in class_name.lower():
            info = disease_db[key].copy()
            info['confidence'] = confidence
            st.sidebar.warning(f"⚠️ Partial match: {class_name} -> {key}")
            return info
    
    # 4. Fallback
    st.sidebar.error(f"❌ No match found for: {class_name}")
    return {
        'confidence': confidence,
        'nama_id': class_name.replace('-', ' ').title(),
        'tingkat_bahaya': 'Medium',
        'solusi': ['Konsultasikan dengan ahli', 'Ambil foto lebih detail']
    }
def _update_detection_state(detection_info):
    """Update detection state dengan validasi"""
    if detection_info and isinstance(detection_info, dict):
        st.session_state.detection_confidence = detection_info.get('confidence', 0.0)
        st.session_state.detection_class = detection_info.get('nama_id', 'Unknown')
        st.session_state.detection_severity = detection_info.get('tingkat_bahaya', 'Medium')
        st.session_state.detection_solutions = detection_info.get('solusi', ['No solutions available'])
        st.session_state.last_detection_time = time.time()
        
        # Debug info
        if st.session_state.get('debug_mode', False):
            st.sidebar.success(f"📦 Updated state: {detection_info['nama_id']}")
    else:
        st.session_state.detection_confidence = 0.0
        st.session_state.detection_class = 'Tidak terdeteksi'
        st.session_state.detection_severity = 'Low'
        st.session_state.detection_solutions = ['Coba gambar berbeda', 'Ubah pengaturan confidence']
def _show_system_info():
    """Show system info"""
    col1, col2, col3 = st.columns(3)
    
    with col1:
        status = "LIVE" if st.session_state.get('camera_active', False) else "READY"
        color = "#FF6B6B" if status == "LIVE" else "#A8E890"
        st.markdown(f"""
        <div class="info-box">
            <div style="font-size: 11px; color: {color};">{status}</div>
            <div style="font-weight: bold;">CAMERA STATUS</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        current_time = datetime.now().strftime("%H:%M")
        st.markdown(f"""
        <div class="info-box">
            <div style="font-size: 11px; color: #FFB7B2;">WAKTU</div>
            <div style="font-weight: bold;">{current_time} WIB</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="info-box">
            <div style="font-size: 11px; color: #A8E890;">MODE</div>
            <div style="font-weight: bold;">PRO SETTINGS</div>
        </div>
        """, unsafe_allow_html=True)

def _initialize_session_state():
    """Initialize session state"""
    if 'scanner_init' not in st.session_state:
        st.session_state.update({
            'detection_confidence': 0.0,
            'detection_class': 'Pilih mode untuk memulai',
            'detection_severity': 'Low',
            'detection_solutions': ['Gunakan camera real-time atau upload gambar'],
            'camera_active': False,
            'confidence_threshold': 0.3,
            'overlap_threshold': 0.5,
            'inference_interval': 3,
            'debug_mode': False,
            'scanner_init': True
        })

def _show_analytics_section():
    """Show analytics section dengan informasi lengkap"""
    st.markdown("### 📊 Plant Health Analytics")
    
    with st.container():
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        
        # Detection Result (PALING PENTING)
        detection_class = st.session_state.detection_class
        confidence = st.session_state.detection_confidence
        
        st.markdown("#### 🧬 **DETECTION RESULT**")
        
        # Tampilkan dengan warna sesuai severity
        severity = st.session_state.detection_severity.lower()
        if 'sehat' in detection_class.lower() or 'healthy' in detection_class.lower():
            st.success(f"## 🌿 {detection_class}")
        elif severity in ['high', 'critical', 'tinggi']:
            st.error(f"## ⚠️ {detection_class}")
        elif severity in ['medium', 'sedang']:
            st.warning(f"## 🔸 {detection_class}")
        else:
            st.info(f"## ℹ️ {detection_class}")
        
        # Confidence Meter
        st.markdown(f"**Confidence:** `{confidence:.1%}`")
        st.progress(float(confidence))
        
        # Severity Badge
        severity_color = {
            'low': '#4CAF50',
            'medium': '#FF9800', 
            'high': '#F44336',
            'critical': '#D32F2F'
        }.get(st.session_state.detection_severity.lower(), '#FF9800')
        
        st.markdown(f"""
        <div style="background-color: {severity_color}20; padding: 10px; border-radius: 5px; border-left: 4px solid {severity_color}; margin: 10px 0;">
            <strong>🔄 Tingkat Bahaya:</strong> 
            <span style="color: {severity_color}; font-weight: bold;">
                {st.session_state.detection_severity.upper()}
            </span>
        </div>
        """, unsafe_allow_html=True)
        
        # Treatment Recommendations
        with st.expander("💡 **REKOMENDASI PENANGANAN**", expanded=True):
            solutions = st.session_state.detection_solutions
            if solutions and len(solutions) > 0:
                for i, solution in enumerate(solutions, 1):
                    st.markdown(f"**{i}.** {solution}")
            else:
                st.info("Belum ada rekomendasi spesifik. Konsultasikan dengan ahli tanaman.")
        
        # Quick Actions
        st.markdown("#### ⚡ **Quick Actions**")
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("📸 Ambil Foto Lagi", use_container_width=True):
                st.rerun()
        
        with col2:
            if st.button("⚙️ Atur Ulang Settings", use_container_width=True):
                st.session_state.confidence_threshold = 0.3
                st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)

def _load_disease_database():
    """Load disease database dari berbagai kemungkinan path"""
    possible_paths = [
        'data/diseases/penyakit.json',  # Path baru dari soal
        'diseases/penyakit.json',       # Path lama
        'penyakit.json',                # Root
        '../data/diseases/penyakit.json',  # Satu level atas
        './data/diseases/penyakit.json'    # Relatif
    ]
    
    for path in possible_paths:
        try:
            if os.path.exists(path):
                with open(path, 'r', encoding='utf-8') as f:
                    db = json.load(f)
                    st.sidebar.success(f"✅ Database loaded from: {path}")
                    return db
        except Exception as e:
            st.sidebar.warning(f"⚠️ Gagal load dari {path}: {e}")
            continue
    
    # Jika tidak ditemukan, buat dummy untuk testing
    st.sidebar.error("❌ Database penyakit tidak ditemukan!")
    
    # Return database dari contoh yang Anda berikan (hardcoded untuk testing)
    return {
        "bell pepper leaf-healthy": {
            "nama_id": "Daun Bell Pepper Sehat",
            "tingkat_bahaya": "Low",
            "solusi": [
                "Pertahankan perawatan rutin",
                "Jaga kelembaban tanah optimal",
                "Berikan pupuk seimbang"
            ]
        },
        "bell pepper leaf-unhealthy": {
            "nama_id": "Daun Bell Pepper Sakit",
            "tingkat_bahaya": "Medium",
            "solusi": [
                "Periksa gejala lebih detail",
                "Isolasi tanaman sementara",
                "Kurangi penyiraman berlebihan"
            ]
        },
        # ... tambahkan lainnya sesuai JSON Anda
        "unknown_disease": {
            "nama_id": "Penyakit Tidak Dikenal",
            "tingkat_bahaya": "Medium",
            "solusi": [
                "Konsultasikan dengan ahli tanaman",
                "Foto gejala dari berbagai angle",
                "Isolasi tanaman sementara",
                "Pantau perkembangan gejala"
            ]
        }
    }

def test_disease_mapping():
    """Test mapping untuk semua kelas di model"""
    test_cases = [
        "bell pepper leaf-healthy",
        "bell pepper leaf-unhealthy", 
        "cucumber leaf - healthy",
        "cucumber leaf - unhealthy",
        "cucumber-mosaic",
        "cucumber-powdery-mildew",
        "lettuce-bacterial leaf spot",
        "lettuce-downy mildew",
        "lettuce-healthy",
        "strawberry fruit-healthy",
        "strawberry leaf-healthy",
        "strawberry-angular leafspot",
        "tomato-early blight",
        "tomato-healthy"
    ]
    
    st.sidebar.markdown("### 🧪 Test Mapping")
    
    for test_class in test_cases:
        with st.sidebar.expander(f"Test: {test_class}", expanded=False):
            result = _map_to_disease_database(test_class, 0.85)
            st.write(f"**Nama:** {result['nama_id']}")
            st.write(f"**Severity:** {result['tingkat_bahaya']}")
            st.write(f"**Solusi:** {len(result['solusi'])} item")

def _get_unique_key(widget_name):
    """Generate unique key untuk widget"""
    # Gunakan kombinasi widget name + timestamp
    import time
    timestamp = int(time.time() * 1000) % 10000
    return f"scanner_{widget_name}_{timestamp}"

# Contoh penggunaan:
confidence = st.slider(
    "Confidence Threshold",
    min_value=0.1,
    max_value=0.9,
    value=0.3,
    step=0.1,
    key=_get_unique_key("confidence_slider")  # Generate key unik
)