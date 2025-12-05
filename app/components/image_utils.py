from PIL import Image, ImageDraw, ImageFont
import numpy as np
from config import COLORS

def draw_bounding_boxes(image, predictions, confidence_threshold):
    """Gambar bounding box dengan warna berdasarkan jenis deteksi"""
    
    if image.mode == 'RGBA':
        image = image.convert('RGB')
    
    img = image.copy()
    draw = ImageDraw.Draw(img)
    
    # Colors untuk jenis deteksi berbeda
    colors = {
        'healthy': (76, 175, 80),      # Hijau untuk sehat
        'unhealthy_high': (244, 67, 54),  # Merah untuk sakit confidence tinggi
        'unhealthy_medium': (255, 152, 0), # Orange untuk sakit confidence medium
        'unhealthy_low': (255, 193, 7),    # Kuning untuk sakit confidence rendah
    }
    
    # Font untuk label
    try:
        font = ImageFont.truetype("arial.ttf", 12)
        font_small = ImageFont.truetype("arial.ttf", 10)
    except:
        font = ImageFont.load_default()
        font_small = ImageFont.load_default()
    
    for pred in predictions:
        if pred['confidence'] >= confidence_threshold:
            # Tentukan warna berdasarkan class dan confidence
            is_unhealthy = 'unhealthy' in pred['class'].lower()
            
            if not is_unhealthy:
                color = colors['healthy']
                label_color = (255, 255, 255)
            else:
                if pred['confidence'] > 0.8:
                    color = colors['unhealthy_high']
                elif pred['confidence'] > 0.6:
                    color = colors['unhealthy_medium']
                else:
                    color = colors['unhealthy_low']
                label_color = (255, 255, 255)
            
            # Koordinat bounding box
            x_center = pred['x'] / 100 * img.width
            y_center = pred['y'] / 100 * img.height
            width = pred['width'] / 100 * img.width
            height = pred['height'] / 100 * img.height
            
            # Hitung koordinat sudut
            x1 = x_center - width / 2
            y1 = y_center - height / 2
            x2 = x_center + width / 2
            y2 = y_center + height / 2
            
            # Gambar rectangle
            draw.rectangle([x1, y1, x2, y2], outline=color, width=2)
            
            # Label dengan class dan confidence
            class_name = pred['class'].replace('leaf-', ' ').replace('_', ' ').title()
            label = f"{class_name}"
            confidence_label = f"{pred['confidence']:.1%}"
            
            # Background untuk main label
            try:
                text_bbox = draw.textbbox((x1, y1 - 25), label, font=font)
                text_width = text_bbox[2] - text_bbox[0]
                text_height = text_bbox[3] - text_bbox[1]
            except:
                text_width = len(label) * 8
                text_height = 20
            
            label_bg = [
                x1 - 2,
                y1 - text_height - 5,
                x1 + text_width + 4,
                y1 - 1
            ]
            draw.rectangle(label_bg, fill=color)
            
            # Gambar teks label
            draw.text((x1, y1 - text_height - 3), label, fill=label_color, font=font)
            
            # Confidence label di bawah
            confidence_bg = [
                x1 - 2,
                y2 + 1,
                x1 + len(confidence_label) * 6 + 4,
                y2 + 20
            ]
            draw.rectangle(confidence_bg, fill=color)
            draw.text((x1, y2 + 2), confidence_label, fill=label_color, font=font_small)
    
    return img

def create_detection_summary(predictions, confidence_threshold):
    """Buat ringkasan deteksi yang informatif"""
    filtered_predictions = [p for p in predictions if p['confidence'] >= confidence_threshold]
    
    if not filtered_predictions:
        return {
            'total_detections': 0,
            'filtered_detections': 0,
            'avg_confidence': 0,
            'healthy_count': 0,
            'unhealthy_count': 0,
            'primary_disease': None
        }
    
    # Hitung statistik
    healthy_count = sum(1 for p in filtered_predictions if 'healthy' in p['class'].lower())
    unhealthy_count = sum(1 for p in filtered_predictions if 'unhealthy' in p['class'].lower())
    
    avg_confidence = np.mean([p['confidence'] for p in filtered_predictions])
    
    # Cari penyakit utama
    primary_disease = None
    if unhealthy_count > 0:
        # Ambil prediksi dengan confidence tertinggi
        highest_conf = max(filtered_predictions, key=lambda x: x['confidence'])
        if 'disease_name' in highest_conf:
            primary_disease = highest_conf['disease_name']
    
    return {
        'total_detections': len(predictions),
        'filtered_detections': len(filtered_predictions),
        'avg_confidence': avg_confidence,
        'healthy_count': healthy_count,
        'unhealthy_count': unhealthy_count,
        'primary_disease': primary_disease
    }