import streamlit as st
from inference_sdk import InferenceHTTPClient
from PIL import Image
import numpy as np

# --- KONFIGURASI MODEL ROBOFLOW ---
# Ganti ini sesuai detail model kamu di Roboflow Universe
API_URL = "https://detect.roboflow.com"
MODEL_ID = "crop-disease-identification-dniia/2"  # ID Model dari project kamu

def perform_detection(image_path, confidence_threshold=0.4, filename="image.jpg"):
    """
    Melakukan deteksi objek menggunakan Roboflow API (Real).
    Jika API Key tidak ada, akan kembali ke mode Simulasi (Dummy).
    """
    api_key = st.session_state.get('roboflow_api_key')
    
    # --- JIKA API KEY TIDAK ADA -> MODE SIMULASI ---
    if not api_key:
        return simulate_detection(image_path, confidence_threshold)

    # --- JIKA ADA API KEY -> MODE REAL ---
    try:
        # Inisialisasi Client Roboflow
        CLIENT = InferenceHTTPClient(
            api_url=API_URL,
            api_key=api_key
        )
        
        # Kirim Gambar ke Server Roboflow
        # result akan berupa JSON berisi prediksi bounding box
        result = CLIENT.infer(image_path, model_id=MODEL_ID)
        
        predictions = []
        
        # Format hasil agar sesuai dengan standar aplikasi kita
        if 'predictions' in result:
            for p in result['predictions']:
                # Filter berdasarkan confidence
                if p['confidence'] >= confidence_threshold:
                    predictions.append({
                        'x': p['x'],
                        'y': p['y'],
                        'width': p['width'],
                        'height': p['height'],
                        'class': p['class'],
                        'confidence': p['confidence']
                    })
        
        return {
            'predictions': predictions,
            'image': image_path,
            'is_real_model': True # Flag penanda ini model asli
        }

    except Exception as e:
        st.error(f"Gagal menghubungi Roboflow: {e}")
        # Jika gagal koneksi, fallback ke simulasi agar app tidak crash
        return simulate_detection(image_path, confidence_threshold)

def simulate_detection(image_path, confidence_threshold):
    """
    Mode Simulasi (Dummy) untuk testing tanpa API Key.
    Akan selalu mendeteksi 'Simulated Disease' secara acak.
    """
    import random
    
    # Buat prediksi palsu di tengah gambar
    img = Image.open(image_path)
    w, h = img.size
    
    predictions = []
    
    # Pura-pura mendeteksi sesuatu
    if random.random() > 0.3: # 70% chance terdeteksi
        predictions.append({
            'x': w / 2,
            'y': h / 2,
            'width': w / 3,
            'height': h / 3,
            'class': "Bell Pepper Leaf-Unhealthy", # Class dummy
            'confidence': 0.85 + (random.random() * 0.1)
        })

    return {
        'predictions': predictions,
        'image': image_path,
        'is_real_model': False # Flag penanda ini simulasi
    }