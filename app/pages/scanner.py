import streamlit as st
import tempfile
import os
from PIL import Image
from config import COLORS
from components.image_utils import draw_bounding_boxes, create_detection_summary
from utils import perform_detection, analyze_detection_results

def render_scanner_page():
    """Render halaman scanner tanaman dengan tema cerah"""
    
    # Tab untuk pilihan input
    tab1, tab2 = st.tabs(["📷 Ambil Foto Langsung", "📁 Upload dari Komputer"])
    
    with tab1:
        render_camera_tab()
    
    with tab2:
        render_upload_tab()

def render_camera_tab():
    """Render tab kamera"""
    
    st.markdown('<div class="custom-card card-upload">', unsafe_allow_html=True)
    st.markdown('<div class="card-title">📷 Foto Langsung dengan Kamera</div>', unsafe_allow_html=True)
    
    st.markdown(f"""
    <div style="color: {COLORS['text_medium']}; margin-bottom: 1.5rem;">
        Ambil foto tanaman secara langsung menggunakan kamera perangkat Anda.
        Pastikan pencahayaan cukup dan fokus pada area daun yang ingin diperiksa.
    </div>
    """, unsafe_allow_html=True)
    
    # Kamera input
    camera_input = st.camera_input(
        "Klik ikon kamera untuk mengambil foto",
        help="Jarak optimal: 30-50cm dari tanaman. Fokus pada daun."
    )
    
    if camera_input:
        with st.spinner("🔍 Menganalisis kesehatan tanaman..."):
            # Simpan file sementara
            with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as tmp_file:
                tmp_file.write(camera_input.read())
                image_path = tmp_file.name
            
            # Proses deteksi
            process_and_display_results(image_path, camera_input, "camera_capture.jpg")
            
            # Bersihkan file temp
            os.unlink(image_path)
    
    st.markdown('</div>', unsafe_allow_html=True)

def render_upload_tab():
    """Render tab upload gambar"""
    
    st.markdown('<div class="custom-card card-upload">', unsafe_allow_html=True)
    st.markdown('<div class="card-title">📁 Upload Gambar Tanaman</div>', unsafe_allow_html=True)
    
    # Area upload
    uploaded_file = st.file_uploader(
        "**Seret dan lepas file gambar ke sini atau klik untuk memilih**",
        type=['jpg', 'jpeg', 'png'],
        help="Format: JPG, JPEG, PNG | Ukuran maks: 10MB",
        label_visibility="collapsed"
    )
    
    if uploaded_file:
        # Buka gambar
        image = Image.open(uploaded_file)
        
        # Tampilkan preview dan info
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**🖼️ Gambar Preview:**")
            st.image(image, use_column_width=True)
        
        with col2:
            st.markdown("**📋 Informasi File:**")
            st.markdown(f"""
            <div style="background: {COLORS['light_gray']}; 
                        padding: 1rem; 
                        border-radius: 8px;
                        border-left: 4px solid {COLORS['info']};">
                <div style="margin-bottom: 0.5rem;">
                    <strong>Nama File:</strong><br>
                    <span style="color: {COLORS['text_medium']};">{uploaded_file.name}</span>
                </div>
                <div style="margin-bottom: 0.5rem;">
                    <strong>Ukuran:</strong><br>
                    <span style="color: {COLORS['text_medium']};">{uploaded_file.size / 1024:.1f} KB</span>
                </div>
                <div style="margin-bottom: 0.5rem;">
                    <strong>Format:</strong><br>
                    <span style="color: {COLORS['text_medium']};">{uploaded_file.type.split('/')[-1].upper()}</span>
                </div>
                <div>
                    <strong>Confidence Threshold:</strong><br>
                    <span style="color: {COLORS['primary']}; font-weight: 600;">
                        {st.session_state.confidence_threshold:.0%}
                    </span>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        # Tombol analisis
        if st.button("🚀 Mulai Analisis AI", type="primary", use_container_width=True):
            with st.spinner("🔄 Menjalankan deteksi penyakit..."):
                # Simpan file sementara
                with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as tmp_file:
                    image.save(tmp_file.name, 'JPEG')
                    image_path = tmp_file.name
                
                # Proses deteksi
                process_and_display_results(image_path, image, uploaded_file.name)
                
                # Bersihkan file temp
                os.unlink(image_path)
    else:
        # Placeholder upload area
        st.markdown(f"""
        <div class="upload-area">
            <div style="font-size: 3.5rem; color: {COLORS['primary']}; margin-bottom: 1rem;">📁</div>
            <div style="font-size: 1.1rem; font-weight: 600; color: {COLORS['text_dark']}; margin-bottom: 0.5rem;">
                Upload Gambar Tanaman
            </div>
            <div style="color: {COLORS['text_medium']}; margin-bottom: 1.5rem;">
                Seret file gambar ke area ini atau klik untuk memilih dari komputer
            </div>
            <div style="color: {COLORS['text_light']}; font-size: 0.9rem; background: {COLORS['white']}; 
                    padding: 0.75rem; border-radius: 6px; display: inline-block;">
                📏 Format: JPG, JPEG, PNG<br>
                💾 Ukuran maks: 10MB per file
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Contoh gambar yang bisa dianalisis
        st.markdown("### 📸 Contoh Gambar yang Bisa Dianalisis")
        
        examples = [
            ("Daun Cabai Sehat", "cabai_healthy.jpg", "🍅", COLORS['success']),
            ("Daun Tomat Sakit", "tomato_blight.jpg", "🌶️", COLORS['warning']),
            ("Daun Kentang", "potato_leaf.jpg", "🥔", COLORS['info']),
            ("Daun Tanaman Hias", "ornamental.jpg", "🌿", COLORS['secondary'])
        ]
        
        cols = st.columns(4)
        for col, (title, filename, icon, color) in zip(cols, examples):
            with col:
                st.markdown(f"""
                <div style="background: {color}15; 
                            border: 1px solid {color}30;
                            border-radius: 10px; 
                            padding: 1rem; 
                            text-align: center;
                            height: 100%;">
                    <div style="font-size: 2rem; margin-bottom: 0.5rem;">{icon}</div>
                    <div style="font-weight: 600; color: {COLORS['text_dark']}; margin-bottom: 0.25rem;">
                        {title}
                    </div>
                    <div style="color: {COLORS['text_medium']}; font-size: 0.85rem;">
                        {filename}
                    </div>
                </div>
                """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

def process_and_display_results(image_path, original_image, filename):
    """Proses gambar dan tampilkan hasil"""
    
    # Status model
    using_real_model = bool(st.session_state.get('roboflow_api_key'))
    
    with st.spinner("🔄 Menjalankan deteksi AI..." if using_real_model else "🔄 Menjalankan simulasi..."):
        # Lakukan deteksi
        detection_results = perform_detection(
            image_path, 
            confidence_threshold=st.session_state.confidence_threshold,
            filename=filename
        )
        
        # Analisis hasil
        analysis = analyze_detection_results(detection_results, st.session_state.confidence_threshold)
        
        # Buat summary
        summary = create_detection_summary(detection_results['predictions'], st.session_state.confidence_threshold)
        
        # Tampilkan hasil
        display_detection_results(original_image, detection_results, analysis, summary, filename)

def display_detection_results(original_image, detection_results, analysis, summary, filename):
    """Tampilkan hasil deteksi"""
    
    # Header dengan status model
    model_badge = "🤖 Roboflow Model" if detection_results.get('is_real_model') else "🔄 Simulation Mode"
    badge_color = COLORS['success'] if detection_results.get('is_real_model') else COLORS['warning']
    
    st.markdown(f"""
    <div style="background: {badge_color}15; 
                border-left: 4px solid {badge_color};
                padding: 0.75rem;
                border-radius: 0 8px 8px 0;
                margin-bottom: 1.5rem;">
        <div style="display: flex; align-items: center; gap: 0.5rem;">
            <div style="font-weight: 600; color: {badge_color};">{model_badge}</div>
            <div style="color: {COLORS['text_medium']}; font-size: 0.9rem;">
                {analysis.get('model_used', 'Unknown')}
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Gambar dengan bounding box
    if isinstance(original_image, str):
        image_pil = Image.open(original_image)
    else:
        image_pil = original_image
    
    image_with_boxes = draw_bounding_boxes(
        image_pil,
        detection_results['predictions'],
        st.session_state.confidence_threshold
    )
    
    # Section 1: Visualisasi
    st.markdown("### 🖼️ Visualisasi Deteksi")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"""
        <div style="background: {COLORS['white']}; 
                    border-radius: 10px; 
                    padding: 1rem;
                    border: 1px solid {COLORS['gray']};">
            <div style="color: {COLORS['text_dark']}; font-weight: 600; margin-bottom: 0.75rem;">
                📸 Gambar Asli
            </div>
        """, unsafe_allow_html=True)
        st.image(original_image, use_column_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div style="background: {COLORS['white']}; 
                    border-radius: 10px; 
                    padding: 1rem;
                    border: 1px solid {COLORS['gray']};">
            <div style="color: {COLORS['text_dark']}; font-weight: 600; margin-bottom: 0.75rem;">
                🔍 Hasil Deteksi AI
            </div>
        """, unsafe_allow_html=True)
        st.image(image_with_boxes, use_column_width=True)
        
        # Legenda warna
        st.markdown(f"""
        <div style="background: {COLORS['light_gray']}; 
                    border-radius: 8px; 
                    padding: 0.75rem;
                    margin-top: 1rem;
                    font-size: 0.85rem;">
            <div style="color: {COLORS['text_dark']}; font-weight: 600; margin-bottom: 0.5rem;">
                🎨 Legenda Warna:
            </div>
            <div style="display: flex; align-items: center; gap: 0.5rem; margin-bottom: 0.25rem;">
                <div style="width: 15px; height: 15px; background: #4CAF50; border-radius: 3px;"></div>
                <span style="color: {COLORS['text_medium']};">Tanaman Sehat</span>
            </div>
            <div style="display: flex; align-items: center; gap: 0.5rem; margin-bottom: 0.25rem;">
                <div style="width: 15px; height: 15px; background: #f44336; border-radius: 3px;"></div>
                <span style="color: {COLORS['text_medium']};">Penyakit (High Confidence)</span>
            </div>
            <div style="display: flex; align-items: center; gap: 0.5rem;">
                <div style="width: 15px; height: 15px; background: #FF9800; border-radius: 3px;"></div>
                <span style="color: {COLORS['text_medium']};">Penyakit (Medium Confidence)</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
    
    # Section 2: Ringkasan Metrics (Card Kuning)
    st.markdown("### 📈 Ringkasan Metrics")
    
    cols = st.columns(4)
    metrics = [
        ("Skor Kesehatan", f"{analysis['health_score']}%", "❤️", 
         "card-metrics", analysis['health_score'] > 70),
        ("Risiko Penyakit", analysis['disease_risk'], "⚠️", 
         "card-metrics", analysis['disease_risk'] == "Rendah"),
        ("Confidence", f"{analysis['avg_confidence']}%", "📊", 
         "card-metrics", analysis['avg_confidence'] > 70),
        ("Objek Terdeteksi", f"{summary['filtered_detections']}", "🔍", 
         "card-metrics", summary['filtered_detections'] > 0)
    ]
    
    for col, (label, value, icon, card_class, is_good) in zip(cols, metrics):
        with col:
            color = COLORS['success'] if is_good else COLORS['text_dark']
            st.markdown(f"""
            <div class="custom-card {card_class}">
                <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 0.5rem;">
                    <div style="font-size: 1.5rem;">{icon}</div>
                    <div style="font-size: 0.85rem; color: {COLORS['text_medium']};">{label}</div>
                </div>
                <div style="font-size: 1.8rem; font-weight: 700; color: {color};">
                    {value}
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    # Section 3: Diagnosis (Card Hijau/Biru)
    st.markdown("### 🩺 Diagnosis")
    
    card_class = "card-diagnosis" if analysis['is_healthy'] else "card-recommendation"
    border_color = COLORS['success'] if analysis['is_healthy'] else COLORS['warning']
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"""
        <div class="custom-card {card_class}">
            <div style="color: {border_color}; font-weight: 600; margin-bottom: 0.75rem; display: flex; align-items: center; gap: 0.5rem;">
                {'✅' if analysis['is_healthy'] else '⚠️'} Hasil Diagnosis
            </div>
            <div style="font-size: 1.1rem; font-weight: 600; color: {COLORS['text_dark']}; margin-bottom: 0.5rem;">
                {analysis['diagnosis']}
            </div>
            <div style="color: {COLORS['text_medium']}; line-height: 1.6;">
                {analysis['detailed_diagnosis']}
            </div>
            <div style="margin-top: 1rem; padding-top: 0.75rem; border-top: 1px solid {COLORS['gray']};">
                <div style="color: {COLORS['text_light']}; font-size: 0.9rem;">
                    Confidence Level: <span style="color: {border_color}; font-weight: 600;">{analysis['confidence_level']}</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        # Deteksi spesifik
        if summary.get('primary_disease'):
            st.markdown(f"""
            <div class="custom-card card-diagnosis">
                <div style="color: {COLORS['warning']}; font-weight: 600; margin-bottom: 0.75rem; display: flex; align-items: center; gap: 0.5rem;">
                ⚠️ Penyakit Terdeteksi
                </div>
                <div style="font-weight: 600; color: {COLORS['text_dark']}; margin-bottom: 0.5rem;">
                    {summary['primary_disease']}
                </div>
                <div style="color: {COLORS['text_medium']};">
                    Confidence: <strong>{analysis['avg_confidence']}%</strong><br>
                    Objek terdeteksi: <strong>{summary['unhealthy_count']}</strong>
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="custom-card card-diagnosis">
                <div style="color: {COLORS['success']}; font-weight: 600; margin-bottom: 0.75rem; display: flex; align-items: center; gap: 0.5rem;">
                ✅ Status Tanaman
                </div>
                <div style="font-weight: 600; color: {COLORS['text_dark']}; margin-bottom: 0.5rem;">
                    Tanaman Sehat
                </div>
                <div style="color: {COLORS['text_medium']};">
                    Tidak terdeteksi penyakit signifikan<br>
                    Objek sehat: <strong>{summary.get('healthy_count', 0)}</strong>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    # Section 4: Rekomendasi (Card Biru)
    st.markdown("### 💡 Rekomendasi Perawatan")
    
    st.markdown(f"""
    <div class="custom-card card-recommendation">
        <div style="color: {COLORS['info']}; font-weight: 600; margin-bottom: 1rem; display: flex; align-items: center; gap: 0.5rem;">
        🛠️ Langkah-langkah yang Disarankan
        </div>
    """, unsafe_allow_html=True)
    
    for i, rec in enumerate(analysis['recommendations'], 1):
        icon = "✅" if analysis['is_healthy'] else "🔸"
        st.markdown(f"""
        <div style="display: flex; align-items: start; gap: 0.75rem; margin-bottom: 0.75rem; padding: 0.75rem; background: {COLORS['white']}; border-radius: 8px;">
            <div style="flex-shrink: 0; width: 24px; height: 24px; background: {COLORS['info']}; color: {COLORS['white']}; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 0.9rem;">
                {i}
            </div>
            <div style="color: {COLORS['text_dark']}; flex: 1;">
                {rec}
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Section 5: Informasi Teknis (Collapsible)
    with st.expander("🔧 Lihat Informasi Teknis Deteksi"):
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**📊 Statistik Deteksi:**")
            st.write(f"- Total prediksi: {summary.get('total_detections', 0)}")
            st.write(f"- Filtered predictions: {summary.get('filtered_detections', 0)}")
            st.write(f"- Healthy objects: {summary.get('healthy_count', 0)}")
            st.write(f"- Unhealthy objects: {summary.get('unhealthy_count', 0)}")
            st.write(f"- Average confidence: {summary.get('avg_confidence', 0):.1%}")
        
        with col2:
            st.markdown("**⚙️ Pengaturan Analisis:**")
            st.write(f"- Confidence threshold: {st.session_state.confidence_threshold:.0%}")
            st.write(f"- Model: YOLOv8 Plant Disease")
            st.write(f"- Plant type: {analysis.get('plant_type', 'Unknown')}")
            st.write(f"- File analyzed: {filename}")
        
        # Raw data
        st.markdown("**📄 Raw Detection Data:**")
        st.json({
            "filename": filename,
            "plant_type": analysis.get('plant_type', 'Unknown'),
            "health_score": analysis.get('health_score', 0),
            "disease_risk": analysis.get('disease_risk', 'Unknown'),
            "predictions_count": summary.get('filtered_detections', 0),
            "model_used": analysis.get('model_used', 'Unknown')
        })