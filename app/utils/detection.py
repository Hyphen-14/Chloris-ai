# app/utils/detection.py
import numpy as np
import random
from pathlib import Path
import os
import streamlit as st
from config import COLORS
from .roboflow_integration import get_roboflow_client

def detect_with_real_model(image_path, confidence_threshold, filename=None):
    """Deteksi menggunakan model Roboflow yang sebenarnya"""
    client = get_roboflow_client()
    
    if not client.is_configured():
        return None
    
    try:
        # Lakukan prediksi dengan model
        result = client.predict(
            image_path, 
            confidence=confidence_threshold,
            overlap=0.5
        )
        
        if result:
            result['filename'] = filename or Path(image_path).name
            result['is_real_model'] = True
            return result
    
    except Exception as e:
        st.warning(f"Model Roboflow gagal: {str(e)}. Menggunakan simulasi...")
    
    return None

def simulate_detection_based_on_filename(filename):
    """Simulasi deteksi berdasarkan nama file (fallback)"""
    filename_lower = filename.lower() if filename else ""
    
    # Mapping nama file ke penyakit
    disease_mapping = {
        'bell': 'Bell Pepper Bacterial Spot',
        'pepper': 'Bell Pepper Bacterial Spot',
        'tomato': 'Tomato Early Blight',
        'potato': 'Potato Late Blight',
        'apple': 'Apple Scab',
        'grape': 'Grape Black Rot',
        'corn': 'Corn Common Rust',
        'citrus': 'Orange Citrus Greening',
        'strawberry': 'Strawberry Leaf Scorch',
    }
    
    # Cari tanaman berdasarkan nama file
    plant_type = "Bell Pepper"
    disease = "Bacterial Spot"
    
    for key, value in disease_mapping.items():
        if key in filename_lower:
            if "pepper" in value:
                plant_type = "Bell Pepper"
                disease = value.replace("Bell Pepper ", "")
            elif "tomato" in value:
                plant_type = "Tomato"
                disease = value.replace("Tomato ", "")
            elif "potato" in value:
                plant_type = "Potato"
                disease = value.replace("Potato ", "")
            break
    
    # Tentukan apakah sehat atau sakit
    is_healthy = any(word in filename_lower for word in ['healthy', 'sehat', 'normal'])
    
    if is_healthy:
        predictions = [
            {
                "x": 40.5,
                "y": 50.2,
                "width": 25.8,
                "height": 32.1,
                "confidence": 0.92,
                "class": f"{plant_type} Healthy",
            }
        ]
    else:
        predictions = [
            {
                "x": 30.5,
                "y": 45.2,
                "width": 25.8,
                "height": 32.1,
                "confidence": 0.85,
                "class": f"{plant_type} {disease}",
            },
            {
                "x": 65.3,
                "y": 60.8,
                "width": 22.5,
                "height": 28.3,
                "confidence": 0.78,
                "class": f"{plant_type} {disease}",
            }
        ]
    
    return {
        "predictions": predictions,
        "image": {"width": 800, "height": 600},
        "objects_detected": len(predictions),
        "plant_type": plant_type,
        "disease_detected": "None" if is_healthy else disease,
        "avg_confidence": np.mean([p["confidence"] for p in predictions]),
        "filename": filename,
        "is_real_model": False
    }

def perform_detection(image_path, confidence_threshold=0.55, filename=None):
    """
    Lakukan deteksi dengan prioritas:
    1. Model Roboflow (jika API key ada)
    2. Simulasi berdasarkan nama file
    """
    
    # Coba dengan model Roboflow terlebih dahulu
    real_result = detect_with_real_model(image_path, confidence_threshold, filename)
    
    if real_result and real_result.get('is_real_model'):
        return real_result
    
    # Fallback ke simulasi berdasarkan nama file
    return simulate_detection_based_on_filename(filename)

def analyze_detection_results(detection_results, confidence_threshold):
    """Analisis hasil deteksi (disesuaikan untuk model real)"""
    
    predictions = detection_results["predictions"]
    filtered_predictions = [p for p in predictions if p['confidence'] >= confidence_threshold]
    
    if not filtered_predictions:
        return {
            "health_score": 95,
            "disease_risk": "Sangat Rendah",
            "diagnosis": f"{detection_results.get('plant_type', 'Tanaman')} sehat",
            "detailed_diagnosis": "Tidak terdeteksi penyakit pada threshold saat ini",
            "confidence_level": "Tinggi",
            "is_healthy": True,
            "model_used": "Roboflow Model" if detection_results.get('is_real_model') else "Simulasi"
        }
    
    # Analisis berdasarkan prediksi
    is_unhealthy = any('healthy' not in p.get('class', '').lower() 
                      and p.get('class', '').lower() != 'healthy' 
                      for p in filtered_predictions)
    
    avg_confidence = np.mean([p['confidence'] for p in filtered_predictions])
    
    # Dapatkan informasi dari prediksi
    classes = list(set([p['class'] for p in filtered_predictions]))
    primary_class = classes[0] if classes else "Unknown"
    
    # Tentukan plant_type dari class
    plant_type = detection_results.get('plant_type', 'Tanaman')
    if 'Bell Pepper' in primary_class:
        plant_type = 'Bell Pepper'
    elif 'Tomato' in primary_class:
        plant_type = 'Tomato'
    elif 'Potato' in primary_class:
        plant_type = 'Potato'
    elif 'Apple' in primary_class:
        plant_type = 'Apple'
    elif 'Corn' in primary_class:
        plant_type = 'Corn'
    elif 'Grape' in primary_class:
        plant_type = 'Grape'
    
    # Hitung health score
    if is_unhealthy:
        health_score = max(0, 100 - (avg_confidence * 60))
        disease_risk = "Tinggi" if avg_confidence > 0.75 else "Sedang"
        
        # Ambil nama penyakit dari class
        disease_name = primary_class.replace(f"{plant_type} ", "")
        diagnosis = f"{plant_type} terdeteksi {disease_name}"
        detailed_diagnosis = f"Confidence rata-rata: {avg_confidence:.1%}"
        
        recommendations = [
            f"🚨 **Segera tangani** - {disease_name} terdeteksi",
            f"🔍 **Konfirmasi** - Periksa tanaman secara visual",
            f"💊 **Pengobatan** - Gunakan fungicide/baktericide sesuai",
            f"✂️ **Pemangkasan** - Buang bagian terinfeksi",
            f"🌡️ **Lingkungan** - Optimalkan kelembaban & sirkulasi udara",
            f"📅 **Monitoring** - Pantau perkembangan setiap 2 hari",
            f"🌱 **Nutrisi** - Beri pupuk seimbang untuk imunitas"
        ]
    else:
        health_score = min(100, 80 + (avg_confidence * 20))
        disease_risk = "Rendah"
        diagnosis = f"{plant_type} dalam kondisi sehat"
        detailed_diagnosis = f"Tidak terdeteksi penyakit (Confidence: {avg_confidence:.1%})"
        
        recommendations = [
            f"✅ **Kondisi baik** - Tanaman sehat",
            f"🌱 **Pertahankan** - Lanjutkan perawatan rutin",
            f"💧 **Penyiraman** - Sesuaikan dengan kebutuhan",
            f"☀️ **Cahaya** - Pastikan 6-8 jam/hari",
            f"📊 **Pemantauan** - Cek kesehatan mingguan",
            f"🛡️ **Preventif** - Jaga kebersihan area tanam"
        ]
    
    # Tentukan confidence level
    if len(filtered_predictions) >= 2 and avg_confidence > 0.8:
        confidence_level = "Sangat Tinggi"
    elif len(filtered_predictions) >= 1 and avg_confidence > 0.6:
        confidence_level = "Tinggi"
    else:
        confidence_level = "Sedang"
    
    return {
        "health_score": round(health_score),
        "disease_risk": disease_risk,
        "diagnosis": diagnosis,
        "detailed_diagnosis": detailed_diagnosis,
        "confidence_level": confidence_level,
        "recommendations": recommendations,
        "plant_type": plant_type,
        "is_healthy": not is_unhealthy,
        "model_used": "Roboflow Model" if detection_results.get('is_real_model') else "Simulasi",
        "predictions_count": len(filtered_predictions),
        "avg_confidence": round(avg_confidence * 100, 1),
        "detected_classes": classes
    }