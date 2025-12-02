# src/core/disease_detector.py
import json
import streamlit as st
from pathlib import Path

class DiseaseDetector:
    def __init__(self):
        self.disease_db = self._load_disease_database()
    
    def _load_disease_database(self):
        """Load disease information from JSON"""
        try:
            db_path = Path("data/diseases/penyakit.json")
            with open(db_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            st.error("❌ Disease database not found!")
            return {}
        except json.JSONDecodeError:
            st.error("❌ Invalid disease database format!")
            return {}
    
    def get_disease_info(self, disease_class):
        """Get disease information by class name"""
        return self.disease_db.get(disease_class, None)
    
    def process_detection(self, results, model):
        """Process YOLO detection results"""
        if not results or not model:
            return None
            
        boxes = results[0].boxes
        if boxes is None or len(boxes) == 0:
            return None
        
        # Get highest confidence detection
        max_conf_idx = boxes.conf.argmax()
        box = boxes[max_conf_idx]
        
        detection_info = {
            'class_id': int(box.cls),
            'class_name': model.names[int(box.cls)],
            'confidence': float(box.conf),
            'bbox': box.xyxy[0].tolist()
        }
        
        # Add disease info
        disease_info = self.get_disease_info(detection_info['class_name'])
        if disease_info:
            detection_info.update(disease_info)
            
        return detection_info