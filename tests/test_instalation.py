# test_installation.py
import streamlit as st
import os
from dotenv import load_dotenv

load_dotenv()

def test_installation():
    st.title("🔧 Test Installation")
    
    # Test basic packages
    try:
        import cv2
        st.success("✅ OpenCV terinstall")
    except ImportError:
        st.error("❌ OpenCV tidak terinstall")
    
    try:
        import inference
        st.success("✅ Inference terinstall")
    except ImportError:
        st.error("❌ Inference tidak terinstall")
    
    try:
        import supervision
        st.success("✅ Supervision terinstall")
    except ImportError:
        st.error("❌ Supervision tidak terinstall")
    
    # Test API Key
    api_key = os.getenv("ROBOFLOW_API_KEY")
    if api_key and api_key != "your_actual_api_key_here":
        st.success(f"✅ API Key: {api_key[:8]}...{api_key[-4:]}")
    else:
        st.error("❌ API Key tidak ditemukan")
    
    # Test model loading
    if st.button("Test Model Loading"):
        try:
            from inference import get_model
            model = get_model(model_id="crop-disease-identification-dnila/2")
            st.success("✅ Model berhasil diload!")
        except Exception as e:
            st.error(f"❌ Gagal load model: {e}")

if __name__ == "__main__":
    test_installation()