# app/main.py
import os
import sys
import streamlit as st
from pathlib import Path
from dotenv import load_dotenv

# Tambahkan path untuk import module
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

# Load environment variables dan CSS
load_dotenv()

from styles import load_css
from components.sidebar import create_sidebar

# Load CSS
load_css()

def main():
    """Main app CHLORIS AI dengan styling premium"""
    
    # Inisialisasi session state untuk debug mode
    if 'debug_mode' not in st.session_state:
        st.session_state.debug_mode = False
    
    # Pilih halaman dari sidebar
    selected_page = create_sidebar()
    
    # Header untuk setiap halaman
    if selected_page == "Scanner Tanaman":
        st.markdown("<h1 style='text-align: center; color: #A8E890;'>🌿 PLANT SCANNER PRO</h1>", 
                   unsafe_allow_html=True)
        
        # Check API key sebelum load scanner
        api_key = os.getenv("ROBOFLOW_API_KEY")
        if not api_key or api_key == "your_actual_api_key_here":
            st.error("""
            ## ❌ API KEY BELUM DIKONFIGURASI
            
            **Langkah setup:**
            1. Buat file `.env` di folder utama
            2. Tambahkan: `ROBOFLOW_API_KEY=kunci_anda_disini`
            3. Restart aplikasi
            """)
            
            with st.expander("🔧 Advanced Setup", expanded=False):
                st.code("""
# Isi file .env dengan:
ROBOFLOW_API_KEY=your_actual_key_here
                """)
                
                manual_key = st.text_input("Atau masukkan API key manual:", type="password")
                if manual_key:
                    os.environ["ROBOFLOW_API_KEY"] = manual_key
                    st.success("✅ API key disimpan! Refresh halaman.")
                    st.rerun()
        else:
            try:
                from pages.scanner import show_scanner_page
                show_scanner_page()
            except ImportError as e:
                st.error(f"❌ Tidak dapat memuat modul scanner: {e}")
                st.info("Pastikan file `pages/scanner.py` ada dan dapat diimport")
    
    elif selected_page == "Ensiklopedia":
        # Header dengan gradient effect
        st.markdown("""
        <div style='text-align: center; padding: 20px; background: linear-gradient(90deg, #0a0f0d, #1a2f23); border-radius: 15px; margin-bottom: 30px;'>
            <h1 style='color: #A8E890; margin-bottom: 10px;'>📚 ENCYCLOPEDIA PHYTOS</h1>
            <p style='color: #d1e7dd;'>Database Lengkap Penyakit Tanaman AI-Powered</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Tampilkan database penyakit
        try:
            from pages.scanner import _load_disease_database
            disease_db = _load_disease_database()
            
            # Stats card
            col1, col2, col3 = st.columns(3)
            with col1:
                st.markdown("""
                <div class='glass-card' style='text-align: center;'>
                    <div style='font-size: 32px; color: #A8E890;'>📊</div>
                    <div style='font-weight: bold;'>{}</div>
                    <div style='font-size: 12px; color: #a3b1a8;'>DISEASES</div>
                </div>
                """.format(len(disease_db)), unsafe_allow_html=True)
            
            with col2:
                st.markdown("""
                <div class='glass-card' style='text-align: center;'>
                    <div style='font-size: 32px; color: #4A6B5A;'>🌿</div>
                    <div style='font-weight: bold;'>5</div>
                    <div style='font-size: 12px; color: #a3b1a8;'>PLANT TYPES</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col3:
                st.markdown("""
                <div class='glass-card' style='text-align: center;'>
                    <div style='font-size: 32px; color: #FFB7B2;'>⚕️</div>
                    <div style='font-weight: bold;'>20+</div>
                    <div style='font-size: 12px; color: #a3b1a8;'>TREATMENTS</div>
                </div>
                """, unsafe_allow_html=True)
            
            # Search dan filter
            st.markdown("### 🔍 Disease Database")
            
            search_col, filter_col = st.columns([3, 1])
            with search_col:
                search_term = st.text_input("", placeholder="🔎 Search diseases...")
            
            with filter_col:
                severity_filter = st.selectbox("Severity", ["All", "Low", "Medium", "High"])
            
            # Display diseases
            st.markdown("---")
            
            for disease_id, info in disease_db.items():
                if search_term and search_term.lower() not in disease_id.lower() and search_term.lower() not in info['nama_id'].lower():
                    continue
                
                if severity_filter != "All" and severity_filter.lower() != info['tingkat_bahaya'].lower():
                    continue
                
                # Color coding for severity
                severity_color = {
                    "low": "#4CAF50",
                    "medium": "#FF9800",
                    "high": "#F44336"
                }.get(info['tingkat_bahaya'].lower(), "#FF9800")
                
                with st.container():
                    st.markdown(f"""
                    <div class='glass-card'>
                        <div style='display: flex; justify-content: space-between; align-items: center;'>
                            <h3 style='color: #A8E890; margin: 0;'>{info['nama_id']}</h3>
                            <span style='background: {severity_color}20; color: {severity_color}; padding: 5px 15px; border-radius: 20px; font-size: 12px; border: 1px solid {severity_color}50;'>
                                {info['tingkat_bahaya'].upper()}
                            </span>
                        </div>
                        <p style='color: #888; font-size: 12px; margin-top: 5px;'>ID: <code>{disease_id}</code></p>
                        
                        <div style='margin-top: 15px;'>
                            <p style='color: #d1e7dd; font-weight: 600;'>💡 Treatment Solutions:</p>
                            <ul style='color: #a3b1a8; margin-left: 20px;'>
                    """, unsafe_allow_html=True)
                    
                    for solution in info['solusi']:
                        st.markdown(f"<li>{solution}</li>", unsafe_allow_html=True)
                    
                    st.markdown("</ul></div></div>", unsafe_allow_html=True)
            
        except Exception as e:
            st.error(f"❌ Gagal memuat database: {e}")
            st.info("Pastikan file `data/diseases/penyakit.json` ada")
    
    elif selected_page == "Laporan":
        # Premium header
        st.markdown("""
        <div style='text-align: center; padding: 20px; background: linear-gradient(90deg, #0a0f0d, #1a2f23); border-radius: 15px; margin-bottom: 30px;'>
            <h1 style='color: #A8E890; margin-bottom: 10px;'>📊 LUMINOUS ANALYTICS</h1>
            <p style='color: #d1e7dd;'>Advanced Plant Health Intelligence & Reporting</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Analytics cards
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown("""
            <div class='metric-box'>
                <div class='metric-value'>0</div>
                <div class='metric-label'>TOTAL SCANS</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class='metric-box'>
                <div class='metric-value' style='color: #4CAF50;'>0</div>
                <div class='metric-label'>HEALTHY PLANTS</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
            <div class='metric-box'>
                <div class='metric-value' style='color: #FF9800;'>0</div>
                <div class='metric-label'>DISEASED PLANTS</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown("""
            <div class='metric-box'>
                <div class='metric-value' style='color: #FFB7B2;'>0%</div>
                <div class='metric-label'>AI ACCURACY</div>
            </div>
            """, unsafe_allow_html=True)
        
        # Chart placeholders
        st.markdown("### 📈 Detection Trends")
        col_chart1, col_chart2 = st.columns(2)
        
        with col_chart1:
            st.markdown("""
            <div class='glass-card' style='text-align: center; height: 300px; display: flex; align-items: center; justify-content: center;'>
                <div>
                    <div style='font-size: 48px; color: #4A6B5A;'>📊</div>
                    <p style='color: #a3b1a8;'>Disease Distribution Chart</p>
                    <p style='color: #888; font-size: 12px;'>(Coming Soon)</p>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with col_chart2:
            st.markdown("""
            <div class='glass-card' style='text-align: center; height: 300px; display: flex; align-items: center; justify-content: center;'>
                <div>
                    <div style='font-size: 48px; color: #4A6B5A;'>📅</div>
                    <p style='color: #a3b1a8;'>Monthly Detection Trends</p>
                    <p style='color: #888; font-size: 12px;'>(Coming Soon)</p>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        # Recent detections table
        st.markdown("### 🕐 Recent Detections")
        st.markdown("""
        <div class='glass-card'>
            <table style='width: 100%; color: #d1e7dd; border-collapse: collapse;'>
                <thead>
                    <tr style='border-bottom: 1px solid rgba(168, 232, 144, 0.2);'>
                        <th style='padding: 10px; text-align: left;'>Date</th>
                        <th style='padding: 10px; text-align: left;'>Plant</th>
                        <th style='padding: 10px; text-align: left;'>Status</th>
                        <th style='padding: 10px; text-align: left;'>Confidence</th>
                    </tr>
                </thead>
                <tbody>
                    <tr style='border-bottom: 1px solid rgba(255,255,255,0.05);'>
                        <td style='padding: 10px;'>No data available</td>
                        <td style='padding: 10px;'>-</td>
                        <td style='padding: 10px; color: #888;'>-</td>
                        <td style='padding: 10px; color: #888;'>-</td>
                    </tr>
                </tbody>
            </table>
        </div>
        """, unsafe_allow_html=True)
        
        # Export options
        st.markdown("---")
        col_export1, col_export2, col_export3 = st.columns(3)
        
        with col_export1:
            if st.button("📥 Export CSV", use_container_width=True):
                st.info("Export feature coming soon")
        
        with col_export2:
            if st.button("📊 Generate Report", use_container_width=True):
                st.info("Report generation coming soon")
        
        with col_export3:
            if st.button("🔄 Refresh Data", use_container_width=True):
                st.rerun()
    
    elif selected_page == "Pengaturan":
        # Premium header
        st.markdown("""
        <div style='text-align: center; padding: 20px; background: linear-gradient(90deg, #0a0f0d, #1a2f23); border-radius: 15px; margin-bottom: 30px;'>
            <h1 style='color: #A8E890; margin-bottom: 10px;'>⚙️ SYSTEM CONFIGURATION</h1>
            <p style='color: #d1e7dd;'>Advanced Settings & System Diagnostics</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Tabs
        tab1, tab2, tab3, tab4 = st.tabs(["🔑 API Settings", "🤖 AI Model", "⚙️ System", "ℹ️ About"])
        
        with tab1:
            st.markdown("### API Configuration")
            
            # Current API key status
            api_key = os.getenv("ROBOFLOW_API_KEY", "Not set")
            if api_key and api_key != "your_actual_api_key_here":
                st.success(f"""
                **Status:** ✅ Connected
                **API Key:** `{api_key[:8]}...{api_key[-4:]}`
                """)
            else:
                st.error("**Status:** ❌ Not Configured")
            
            # Manual API key input
            with st.form("api_key_form"):
                st.markdown("#### Manual API Key Setup")
                new_key = st.text_input("Enter Roboflow API Key", type="password", 
                                      placeholder="rf_xxxxxxxxxxxxxxxxxxxxxxxx")
                
                col_submit, col_clear = st.columns(2)
                with col_submit:
                    submit = st.form_submit_button("💾 Save to Session", use_container_width=True)
                
                with col_clear:
                    if st.form_submit_button("🗑️ Clear", use_container_width=True, type="secondary"):
                        os.environ["ROBOFLOW_API_KEY"] = ""
                        st.rerun()
                
                if submit and new_key:
                    os.environ["ROBOFLOW_API_KEY"] = new_key
                    st.success("✅ API Key saved to session! Refresh to apply.")
                    st.rerun()
            
            st.markdown("---")
            st.markdown("""
            **💡 How to get API Key:**
            1. Login to [Roboflow](https://app.roboflow.com)
            2. Click profile picture → Account Settings
            3. Copy API Key from "Roboflow API Key" section
            """)
        
        with tab2:
            st.markdown("### AI Model Configuration")
            
            # Model info card
            st.markdown("""
            <div class='glass-card'>
                <h3 style='color: #A8E890;'>🌿 Crop Disease Identification Model</h3>
                <div style='display: grid; grid-template-columns: 1fr 1fr; gap: 15px; margin-top: 15px;'>
                    <div>
                        <p style='color: #a3b1a8; font-size: 12px;'>MODEL NAME</p>
                        <p style='color: #d1e7dd; font-weight: bold;'>crop-disease-identification-dniia</p>
                    </div>
                    <div>
                        <p style='color: #a3b1a8; font-size: 12px;'>VERSION</p>
                        <p style='color: #d1e7dd; font-weight: bold;'>2</p>
                    </div>
                    <div>
                        <p style='color: #a3b1a8; font-size: 12px;'>TYPE</p>
                        <p style='color: #d1e7dd; font-weight: bold;'>Instance Segmentation</p>
                    </div>
                    <div>
                        <p style='color: #a3b1a8; font-size: 12px;'>CLASSES</p>
                        <p style='color: #d1e7dd; font-weight: bold;'>29</p>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Performance settings
            st.markdown("#### ⚡ Performance Settings")
            perf_col1, perf_col2 = st.columns(2)
            
            with perf_col1:
                inference_speed = st.select_slider(
                    "Inference Speed",
                    options=["Slow", "Medium", "Fast", "Ultra"],
                    value="Medium"
                )
            
            with perf_col2:
                model_precision = st.select_slider(
                    "Model Precision",
                    options=["Low", "Medium", "High", "Ultra"],
                    value="High"
                )
            
            if st.button("🔄 Apply Model Settings", use_container_width=True):
                st.success(f"✅ Applied: {inference_speed} speed, {model_precision} precision")
        
        with tab3:
            st.markdown("### System Settings")
            
            # Debug toggle
            debug_state = st.toggle(
                "🐛 Debug Mode", 
                value=st.session_state.get('debug_mode', False),
                help="Enable detailed logging and debugging information"
            )
            st.session_state.debug_mode = debug_state
            
            if debug_state:
                st.success("Debug mode: **ENABLED**")
            else:
                st.info("Debug mode: **DISABLED**")
            
            # System controls
            st.markdown("#### 🛠️ System Controls")
            
            control_col1, control_col2, control_col3 = st.columns(3)
            
            with control_col1:
                if st.button("🔄 Clear Cache", use_container_width=True):
                    st.cache_data.clear()
                    st.success("Cache cleared!")
            
            with control_col2:
                if st.button("📊 Reset Stats", use_container_width=True):
                    st.info("Stats reset (demo only)")
            
            with control_col3:
                if st.button("⚙️ Reset Settings", use_container_width=True):
                    st.session_state.clear()
                    st.rerun()
            
            # System info
            st.markdown("#### 🖥️ System Information")
            st.markdown(f"""
            <div class='glass-card'>
                <div style='font-family: monospace; color: #a3b1a8;'>
                    <div><span style='color: #A8E890;'>Platform:</span> {sys.platform}</div>
                    <div><span style='color: #A8E890;'>Python:</span> {sys.version.split()[0]}</div>
                    <div><span style='color: #A8E890;'>Streamlit:</span> {st.__version__}</div>
                    <div><span style='color: #A8E890;'>Working Dir:</span> {os.getcwd()}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with tab4:
            st.markdown("### About CHLORIS AI")
            
            st.markdown("""
            <div class='glass-card'>
                <h3 style='color: #A8E890;'>🌿 CHLORIS AI - Luminous AI System</h3>
                <p style='color: #d1e7dd; margin-top: 15px;'>
                    Advanced plant disease detection system powered by AI and computer vision. 
                    Utilizing Roboflow's instance segmentation model for precise plant health analysis.
                </p>
                
                <div style='margin-top: 20px;'>
                    <p style='color: #a3b1a8; font-size: 12px;'>VERSION</p>
                    <p style='color: #d1e7dd; font-weight: bold;'>v1.0.0 Alpha</p>
                </div>
                
                <div style='margin-top: 15px;'>
                    <p style='color: #a3b1a8; font-size: 12px;'>TECHNOLOGY STACK</p>
                    <div style='display: flex; gap: 10px; margin-top: 10px;'>
                        <span style='background: rgba(168, 232, 144, 0.1); color: #A8E890; padding: 5px 10px; border-radius: 5px; font-size: 12px;'>Streamlit</span>
                        <span style='background: rgba(168, 232, 144, 0.1); color: #A8E890; padding: 5px 10px; border-radius: 5px; font-size: 12px;'>Roboflow</span>
                        <span style='background: rgba(168, 232, 144, 0.1); color: #A8E890; padding: 5px 10px; border-radius: 5px; font-size: 12px;'>OpenCV</span>
                        <span style='background: rgba(168, 232, 144, 0.1); color: #A8E890; padding: 5px 10px; border-radius: 5px; font-size: 12px;'>Python</span>
                    </div>
                </div>
                
                <div style='margin-top: 20px;'>
                    <p style='color: #a3b1a8; font-size: 12px;'>LICENSE</p>
                    <p style='color: #d1e7dd;'>MIT License • © 2024 CHLORIS AI</p>
                </div>
            </div>
            """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()