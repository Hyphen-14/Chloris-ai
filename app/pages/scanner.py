import streamlit as st
import tempfile
import os
import re  # Import RegEx untuk memperbaiki format teks
from PIL import Image
from config import COLORS
from utils import perform_detection, analyze_detection_results, create_detection_summary, save_scan_result

def render_scanner_page():
    """Render halaman scanner tanaman (Fixed: Recommendations & Bold Text)"""
    
    # 1. INIT STATE
    if 'scan_results' not in st.session_state:
        st.session_state['scan_results'] = None

    # 2. HEADER
    st.markdown(f"""
    <div class="page-header-box">
        <h2 style="color: {COLORS['text_main']}; margin-top: 0;">🔍 Scanner Tanaman</h2>
        <p style="color: {COLORS['text_body']}; margin-bottom: 0;">
            Diagnosa penyakit tanaman secara real-time.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.write("")
    
    # 3. TAB INPUT
    tab1, tab2 = st.tabs(["📸 Ambil Foto Langsung", "📁 Upload dari Komputer"])
    
    with tab1:
        st.write("")
        render_camera_tab()
    with tab2:
        st.write("")
        render_upload_tab()

    # 4. HASIL SCAN
    if st.session_state['scan_results']:
        display_results_from_state()

def render_camera_tab():
    st.markdown(f"""
    <div style="background-color: {COLORS['card_bg']}; padding: 20px; border-radius: 15px; border: 1px solid {COLORS['border']}; margin-bottom: 20px;">
        <h5 style="color: {COLORS['text_main']}; margin-top: 0;">📷 Kamera Aktif</h5>
    </div>
    """, unsafe_allow_html=True)
    
    camera_input = st.camera_input("Shutter")
    
    if camera_input:
        process_image(camera_input, "camera_capture.jpg", is_camera=True)

def render_upload_tab():
    st.markdown(f"""
    <div style="background-color: {COLORS['card_bg']}; padding: 20px; border-radius: 15px; border: 1px solid {COLORS['border']}; margin-bottom: 20px;">
        <h5 style="color: {COLORS['text_main']}; margin-top: 0;">📁 Upload File</h5>
    </div>
    """, unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader("Drop file", type=['jpg', 'jpeg', 'png'], label_visibility="collapsed")
    
    if uploaded_file:
        image = Image.open(uploaded_file)
        st.markdown("---")
        c1, c2 = st.columns([1, 2])
        with c1:
            st.markdown(f"<p style='color: {COLORS['text_main']}; font-weight: 600;'>🖼️ Preview:</p>", unsafe_allow_html=True)
            st.image(image, use_container_width=True)
        with c2:
            st.markdown(f"<p style='color: {COLORS['text_main']}; font-weight: 600;'>📋 Info:</p>", unsafe_allow_html=True)
            st.info(f"File: {uploaded_file.name}")
            
            if st.button("🚀 Analisis Sekarang", type="primary", use_container_width=True):
                process_image(uploaded_file, uploaded_file.name)

def process_image(image_input, filename, is_camera=False):
    with st.spinner("🔄 Menganalisis..."):
        try:
            if is_camera:
                image_pil = Image.open(image_input)
            else:
                image_pil = Image.open(image_input)
                
            with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as tmp_file:
                if image_pil.mode in ("RGBA", "P"): image_pil = image_pil.convert("RGB")
                image_pil.save(tmp_file.name)
                image_path = tmp_file.name
            
            detection_results = perform_detection(
                image_path, 
                confidence_threshold=st.session_state.confidence_threshold,
                filename=filename
            )
            analysis = analyze_detection_results(detection_results, st.session_state.confidence_threshold)
            summary = create_detection_summary(detection_results['predictions'], st.session_state.confidence_threshold)
            
            st.session_state['scan_results'] = {
                'image': image_pil,
                'filename': filename,
                'detection_results': detection_results,
                'analysis': analysis,
                'summary': summary
            }
            
            os.unlink(image_path)
        except Exception as e:
            st.error(f"Terjadi kesalahan: {e}")

def display_results_from_state():
    """Menampilkan hasil dengan Teks Rapi (Anti-Bintang)"""
    data = st.session_state['scan_results']
    original_image = data['image']
    analysis = data['analysis']
    summary = data['summary']
    detection_results = data['detection_results']
    filename = data['filename']
    
    from components.image_utils import draw_bounding_boxes

    st.markdown("---")
    st.markdown(f"<h3 style='color: {COLORS['text_main']}; text-align: center;'>📊 Hasil Analisis AI</h3>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    image_with_boxes = draw_bounding_boxes(
        original_image,
        detection_results['predictions'],
        st.session_state.confidence_threshold
    )
    
    with col1: st.image(original_image, caption="Asli", use_container_width=True)
    with col2: st.image(image_with_boxes, caption="Deteksi", use_container_width=True)

    # Status Bar
    display_name = analysis['diagnosis']
    status_bg = COLORS['success'] if analysis['is_healthy'] else COLORS['warning']
    status_msg = f"✅ {display_name}" if analysis['is_healthy'] else f"⚠️ TERDETEKSI: {display_name}"
    
    st.markdown(f"""
    <div style="margin: 20px 0; background-color: {status_bg}; color: white; padding: 15px; border-radius: 10px; text-align: center; font-weight: 700; font-size: 1.2rem;">
        {status_msg}
    </div>
    """, unsafe_allow_html=True)

    # Metrics
    m1, m2, m3, m4 = st.columns(4)
    metrics_data = [
        ("Kesehatan", f"{analysis['health_score']}%", analysis['health_score'] > 70),
        ("Risiko", analysis['disease_risk'], analysis['disease_risk'] == "Rendah"),
        ("Confidence", f"{analysis['avg_confidence']}%", True),
        ("Objek", str(summary['filtered_detections']), True)
    ]
    for col, (label, val, good) in zip([m1, m2, m3, m4], metrics_data):
        color = COLORS['success'] if good else COLORS['warning']
        with col:
            st.markdown(f"""
            <div style="background: {COLORS['white']}; padding: 10px; border-radius: 10px; border: 1px solid {COLORS['border']}; text-align: center;">
                <div style="font-size: 0.8rem; color: {COLORS['text_light']}">{label}</div>
                <div style="font-size: 1.2rem; font-weight: 700; color: {color}">{val}</div>
            </div>
            """, unsafe_allow_html=True)

    # --- ANALISIS DETAIL (FIX: BOLD TEXT) ---
    # Menggunakan Regex untuk mengubah **Teks** menjadi <b>Teks</b>
    clean_diagnosis = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', analysis['detailed_diagnosis'])
    
    st.markdown(f"""
    <div style="background: {COLORS['white']}; padding: 20px; border-radius: 15px; border: 1px solid {COLORS['border']}; margin-top: 20px;">
        <h4 style="color: {COLORS['text_main']}; margin-top: 0;">🩺 Analisis Detail</h4>
        <p style="color: {COLORS['text_body']}; font-size: 1rem; line-height: 1.6;">
            {clean_diagnosis}
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # --- REKOMENDASI (FIX: DITAMPILKAN SELALU) ---
    # Bagian ini sekarang muncul untuk SEMUA kondisi (Sehat/Sakit)
    if analysis.get('recommendations'):
        header_text = "💡 Tips Perawatan:" if analysis['is_healthy'] else "🛡️ Rekomendasi Penanganan:"
        header_color = COLORS['success'] if analysis['is_healthy'] else COLORS['text_main']
        
        st.markdown(f"<h5 style='color: {header_color}; margin-top: 20px; margin-bottom: 10px;'>{header_text}</h5>", unsafe_allow_html=True)
        
        for rec in analysis['recommendations']:
            # Bersihkan juga ** di dalam rekomendasi jika ada
            clean_rec = re.sub(r'\*\*(.*?)\*\*', r'**\1**', rec) # Biarkan markdown star untuk st.info
            
            if "Segera" in rec:
                st.error(clean_rec, icon="🚨")
            else:
                st.info(clean_rec, icon="✨" if analysis['is_healthy'] else "🛡️")

    # Tombol Simpan
    st.write("")
    col_save = st.columns(1)[0]
    with col_save:
        if st.button("💾 Simpan ke Riwayat", use_container_width=True, type="secondary"):
            success, msg = save_scan_result(
                image_pil=original_image,
                filename=filename,
                disease_name=display_name,
                confidence=analysis['avg_confidence'],
                risk_level=analysis['disease_risk']
            )
            if success:
                st.success(f"✅ {msg}")
                st.balloons()
            else:
                st.error(f"❌ {msg}")