# app/utils.py
import streamlit as st
import os
from app.config import SESSION_DEFAULTS

def initialize_session():
    """Initialize session state"""
    for key, value in SESSION_DEFAULTS.items():
        if key not in st.session_state:
            st.session_state[key] = value
    
    # Initialize API key from environment
    if 'roboflow_api_key' not in st.session_state:
        st.session_state.roboflow_api_key = os.getenv("ROBOFLOW_API_KEY", "")

def clear_session():
    """Clear session state"""
    keys = list(st.session_state.keys())
    for key in keys:
        del st.session_state[key]
    
    # Re-initialize
    initialize_session()

def validate_image_file(file):
    """Validate uploaded image file"""
    if file is None:
        return False, "No file uploaded"
    
    allowed_types = ['image/jpeg', 'image/png', 'image/bmp']
    max_size = 10 * 1024 * 1024  # 10MB
    
    if file.type not in allowed_types:
        return False, "File type not supported"
    
    if file.size > max_size:
        return False, "File size exceeds 10MB limit"
    
    return True, "File valid"