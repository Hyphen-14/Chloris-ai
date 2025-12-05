"""
Integrasi dengan Roboflow API untuk deteksi penyakit tanaman
"""

import os
import tempfile
import cv2
import numpy as np
from PIL import Image
import requests
import json
from typing import Dict, List, Optional
import streamlit as st

class RoboflowAPI:
    """Client untuk API Roboflow"""
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv("ROBOFLOW_API_KEY")
        self.base_url = "https://detect.roboflow.com"
        self.model_id = "crop-disease-identification-dniia/2"
        self.classes = {}  # Akan di-load dari model
        
    def is_configured(self) -> bool:
        """Cek apakah API sudah dikonfigurasi"""
        return bool(self.api_key and self.api_key.strip())
    
    def load_model_classes(self):
        """Load daftar kelas dari model"""
        # Classes dari model crop-disease-identification-dniia
        self.classes = {
            "Apple___Apple_scab": "Apple Scab",
            "Apple___Black_rot": "Apple Black Rot",
            "Apple___Cedar_apple_rust": "Apple Cedar Rust",
            "Apple___healthy": "Apple Healthy",
            "Blueberry___healthy": "Blueberry Healthy",
            "Cherry_(including_sour)___Powdery_mildew": "Cherry Powdery Mildew",
            "Cherry_(including_sour)___healthy": "Cherry Healthy",
            "Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot": "Corn Gray Leaf Spot",
            "Corn_(maize)___Common_rust_": "Corn Common Rust",
            "Corn_(maize)___Northern_Leaf_Blight": "Corn Northern Leaf Blight",
            "Corn_(maize)___healthy": "Corn Healthy",
            "Grape___Black_rot": "Grape Black Rot",
            "Grape___Esca_(Black_Measles)": "Grape Black Measles",
            "Grape___Leaf_blight_(Isariopsis_Leaf_Spot)": "Grape Leaf Blight",
            "Grape___healthy": "Grape Healthy",
            "Orange___Haunglongbing_(Citrus_greening)": "Orange Citrus Greening",
            "Peach___Bacterial_spot": "Peach Bacterial Spot",
            "Peach___healthy": "Peach Healthy",
            "Pepper,_bell___Bacterial_spot": "Bell Pepper Bacterial Spot",
            "Pepper,_bell___healthy": "Bell Pepper Healthy",
            "Potato___Early_blight": "Potato Early Blight",
            "Potato___Late_blight": "Potato Late Blight",
            "Potato___healthy": "Potato Healthy",
            "Raspberry___healthy": "Raspberry Healthy",
            "Soybean___healthy": "Soybean Healthy",
            "Squash___Powdery_mildew": "Squash Powdery Mildew",
            "Strawberry___Leaf_scorch": "Strawberry Leaf Scorch",
            "Strawberry___healthy": "Strawberry Healthy",
            "Tomato___Bacterial_spot": "Tomato Bacterial Spot",
            "Tomato___Early_blight": "Tomato Early Blight",
            "Tomato___Late_blight": "Tomato Late Blight",
            "Tomato___Leaf_Mold": "Tomato Leaf Mold",
            "Tomato___Septoria_leaf_spot": "Tomato Septoria Leaf Spot",
            "Tomato___Spider_mites Two-spotted_spider_mite": "Tomato Spider Mites",
            "Tomato___Target_Spot": "Tomato Target Spot",
            "Tomato___Tomato_Yellow_Leaf_Curl_Virus": "Tomato Yellow Leaf Curl",
            "Tomato___Tomato_mosaic_virus": "Tomato Mosaic Virus",
            "Tomato___healthy": "Tomato Healthy"
        }
    
    def predict(self, image_path: str, confidence: float = 0.5, overlap: float = 0.5) -> Dict:
        """
        Lakukan prediksi menggunakan model Roboflow
        
        Args:
            image_path: Path ke gambar
            confidence: Threshold confidence (0-1)
            overlap: Threshold overlap/IoU (0-1)
        
        Returns:
            Dict dengan hasil prediksi
        """
        if not self.is_configured():
            raise ValueError("Roboflow API key belum dikonfigurasi")
        
        # Baca gambar
        if isinstance(image_path, str):
            image = cv2.imread(image_path)
        else:
            # Jika image_path adalah file-like object
            image = np.array(Image.open(image_path))
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        
        # Encode gambar ke jpg
        _, img_encoded = cv2.imencode('.jpg', image)
        
        # Setup parameters
        params = {
            'api_key': self.api_key,
            'confidence': confidence * 100,  # Convert to percentage
            'overlap': overlap * 100,       # Convert to percentage
            'format': 'json',
            'stroke': 5
        }
        
        # URL endpoint
        url = f"{self.base_url}/{self.model_id}"
        
        try:
            # Kirim request ke Roboflow
            response = requests.post(
                url,
                params=params,
                files={'file': ('image.jpg', img_encoded.tobytes(), 'image/jpeg')},
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                return self._format_predictions(result, image.shape)
            else:
                error_msg = f"API Error {response.status_code}: {response.text}"
                st.error(f"Roboflow API Error: {error_msg}")
                return None
                
        except requests.exceptions.RequestException as e:
            st.error(f"Koneksi ke Roboflow gagal: {str(e)}")
            return None
        except Exception as e:
            st.error(f"Error dalam prediksi: {str(e)}")
            return None
    
    def _format_predictions(self, api_response: Dict, image_shape) -> Dict:
        """Format hasil API ke format yang konsisten"""
        
        predictions = []
        image_height, image_width = image_shape[:2]
        
        if 'predictions' in api_response:
            for pred in api_response['predictions']:
                # Convert class name ke format yang lebih readable
                class_name = pred.get('class', 'Unknown')
                readable_name = self.classes.get(class_name, class_name.replace('_', ' ').title())
                
                # Format bounding box
                x_center = pred.get('x', 0)
                y_center = pred.get('y', 0)
                width = pred.get('width', 0)
                height = pred.get('height', 0)
                
                # Convert ke persentase jika dalam pixel
                if width > 100:  # Asumsi jika > 100 berarti pixel, bukan persen
                    x_center = (x_center / image_width) * 100
                    y_center = (y_center / image_height) * 100
                    width = (width / image_width) * 100
                    height = (height / image_height) * 100
                
                predictions.append({
                    'x': x_center,
                    'y': y_center,
                    'width': width,
                    'height': height,
                    'confidence': pred.get('confidence', 0),
                    'class': readable_name,
                    'original_class': class_name,
                    'points': []  # Tidak ada points dari API
                })
        
        # Hitung confidence rata-rata
        if predictions:
            avg_confidence = np.mean([p['confidence'] for p in predictions])
        else:
            avg_confidence = 0
        
        return {
            'predictions': predictions,
            'image': {
                'width': image_width,
                'height': image_height
            },
            'objects_detected': len(predictions),
            'avg_confidence': avg_confidence,
            'model': self.model_id,
            'inference_time': api_response.get('time', 0),
            'is_real_model': True
        }

# Singleton instance
_roboflow_client = None

def get_roboflow_client():
    """Dapatkan instance Roboflow client"""
    global _roboflow_client
    
    if _roboflow_client is None:
        api_key = st.session_state.get('roboflow_api_key') or os.getenv('ROBOFLOW_API_KEY')
        _roboflow_client = RoboflowAPI(api_key)
        _roboflow_client.load_model_classes()
    
    return _roboflow_client

def set_roboflow_api_key(api_key: str):
    """Set API key untuk Roboflow"""
    global _roboflow_client
    _roboflow_client = RoboflowAPI(api_key)
    _roboflow_client.load_model_classes()
    st.session_state.roboflow_api_key = api_key