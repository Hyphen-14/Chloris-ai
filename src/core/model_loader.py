# src/core/model_loader.py
import os
os.environ['CUDA_VISIBLE_DEVICES'] = '-1'  # Force CPU

from ultralytics import YOLO
import streamlit as st
from pathlib import Path

@st.cache_resource
def load_ai_model():
    """Load YOLO model dengan CPU fallback"""
    try:
        model_path = Path("data/models/best.pt")
        
        if not model_path.exists():
            st.error(f"❌ Model file not found: {model_path}")
            return None
            
        model = YOLO(str(model_path))
        model.overrides['device'] = 'cpu'
        
        # Warmup model
        import numpy as np
        dummy = np.random.randint(0, 255, (640, 640, 3), dtype=np.uint8)
        _ = model(dummy)
        
        st.success(f"✅ AI Model loaded! Classes: {list(model.names.values())}")
        return model
        
    except Exception as e:
        st.error(f"❌ Failed to load AI model: {str(e)}")
        return None

def get_model_classes(model):
    """Get class names from model"""
    return model.names if model else {}