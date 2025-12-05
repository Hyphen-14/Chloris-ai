import streamlit as st
from config import COLORS
from utils import set_roboflow_api_key  # Perbaikan import

def render_sidebar():
    """Render sidebar dengan tema hijau muda dan input API key"""
    
    with st.sidebar:
        # Logo dan header sidebar
        st.markdown(f"""
        <div style="text-align: center; margin-bottom: 1.5rem;">
            <div style="font-size: 2.5rem; color: {COLORS['primary']};">🌿</div>
            <div style="font-size: 1.5rem; font-weight: 700; color: {COLORS['primary']};">
                CHLORIS AI
            </div>
            <div style="color: {COLORS['text_medium']}; font-size: 0.9rem;">
                Plant Disease Detection
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Navigation
        st.markdown(f"""
        <div style="color: {COLORS['text_dark']}; font-weight: 600; margin-bottom: 1rem;">
            🧭 Navigation
        </div>
        """, unsafe_allow_html=True)
        
        menu_options = {
            "Scanner Tanaman": "🔍",
            "Encyclopedia": "📚",
            "Laporan": "📊",
            "Pengaturan": "⚙️"
        }
        
        selected = st.radio(
            "Pilih Menu:",
            list(menu_options.keys()),
            format_func=lambda x: f"{menu_options[x]} {x}",
            label_visibility="collapsed"
        )
        
        st.markdown("---")
        
        # API Key Configuration
        st.markdown(f"""
        <div style="color: {COLORS['text_dark']}; font-weight: 600; margin-bottom: 1rem;">
            🔑 Roboflow API Key
        </div>
        """, unsafe_allow_html=True)
        
        api_key = st.text_input(
            "Masukkan API Key:",
            type="password",
            value=st.session_state.get('roboflow_api_key', ''),
            help="Dapatkan API key dari Roboflow Dashboard",
            label_visibility="collapsed"
        )
        
        if api_key and api_key != st.session_state.get('roboflow_api_key'):
            try:
                set_roboflow_api_key(api_key)
                st.success("✅ API key berhasil disimpan!")
            except Exception as e:
                st.error(f"Error: {str(e)}")
        
        # Status API Key
        if st.session_state.get('roboflow_api_key'):
            st.markdown(f"""
            <div style="background: {COLORS['success']}15; 
                        color: {COLORS['success']};
                        padding: 0.5rem; 
                        border-radius: 6px;
                        border: 1px solid {COLORS['success']}30;
                        font-size: 0.85rem;
                        margin-top: 0.5rem;">
                ✅ API Key: Terkonfigurasi
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div style="background: {COLORS['warning']}15; 
                        color: {COLORS['warning']};
                        padding: 0.5rem; 
                        border-radius: 6px;
                        border: 1px solid {COLORS['warning']}30;
                        font-size: 0.85rem;
                        margin-top: 0.5rem;">
                ⚠️ API Key: Belum dikonfigurasi
            </div>
            """, unsafe_allow_html=True)
        
        # Link untuk mendapatkan API key
        st.markdown(f"""
        <div style="margin-top: 0.5rem; text-align: center;">
            <a href="https://app.roboflow.com/xof/crop-disease-identification-dniia" 
               target="_blank"
               style="color: {COLORS['primary']}; 
                      text-decoration: none;
                      font-size: 0.8rem;">
               Dapatkan API Key →
            </a>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Confidence Settings
        st.markdown(f"""
        <div style="color: {COLORS['text_dark']}; font-weight: 600; margin-bottom: 1rem;">
            ⚙️ Confidence Settings
        </div>
        """, unsafe_allow_html=True)
        
        confidence = st.slider(
            "Confidence Threshold:",
            min_value=0.0,
            max_value=1.0,
            value=st.session_state.confidence_threshold,
            step=0.05,
            format="%.2f",
            label_visibility="collapsed"
        )
        st.session_state.confidence_threshold = confidence
        
        st.markdown(f"""
        <div style="background: {COLORS['white']}; 
                    padding: 0.75rem; 
                    border-radius: 8px; 
                    border: 1px solid {COLORS['primary_light']};
                    margin-top: 0.5rem;">
            <div style="color: {COLORS['text_light']}; font-size: 0.9rem;">Current Threshold:</div>
            <div style="color: {COLORS['primary']}; font-size: 1.25rem; font-weight: 700;">
                {confidence:.0%}
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Model Information
        st.markdown(f"""
        <div style="color: {COLORS['text_dark']}; font-weight: 600; margin-bottom: 1rem;">
            🤖 Model Information
        </div>
        """, unsafe_allow_html=True)
        
        model_status = "✅ Active" if st.session_state.get('roboflow_api_key') else "⚠️ Simulation"
        model_color = COLORS['success'] if st.session_state.get('roboflow_api_key') else COLORS['warning']
        
        st.markdown(f"""
        <div style="color: {COLORS['text_medium']}; font-size: 0.9rem;">
            <strong>Status:</strong> <span style="color: {model_color}">{model_status}</span><br>
            <strong>Model:</strong> YOLOv8<br>
            <strong>Classes:</strong> 38 penyakit<br>
            <strong>Workspace:</strong> xof
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Quick Tips
        st.markdown(f"""
        <div style="color: {COLORS['text_dark']}; font-weight: 600; margin-bottom: 0.5rem;">
            💡 Tips Penggunaan
        </div>
        <div style="color: {COLORS['text_medium']}; font-size: 0.85rem;">
            • Upload gambar daun yang jelas<br>
            • Confidence optimal: 60-80%<br>
            • Untuk hasil akurat, gunakan API key<br>
            • File support: JPG, PNG, JPEG
        </div>
        """, unsafe_allow_html=True)
    
    return selected