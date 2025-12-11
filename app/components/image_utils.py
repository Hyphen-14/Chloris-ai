from PIL import Image, ImageDraw, ImageFont
import streamlit as st

def draw_bounding_boxes(image, predictions, threshold=0.4):
    """
    Menggambar kotak deteksi pada gambar.
    FIX: Mengonversi koordinat Center (Roboflow) ke Top-Left (Pillow).
    """
    # Copy gambar agar tidak merusak yang asli di memori
    draw_image = image.copy()
    draw = ImageDraw.Draw(draw_image)
    
    # Coba load font, jika tidak ada pakai default
    try:
        # Gunakan font default sistem jika memungkinkan agar lebih rapi
        font = ImageFont.truetype("arial.ttf", 20)
    except IOError:
        font = ImageFont.load_default()

    width, height = draw_image.size

    for p in predictions:
        if p['confidence'] >= threshold:
            # --- RUMUS PERBAIKAN KOORDINAT ---
            # Roboflow memberikan: x (center), y (center), width, height
            # Pillow butuh: x0 (kiri), y0 (atas), x1 (kanan), y1 (bawah)
            
            x_center = p['x']
            y_center = p['y']
            box_width = p['width']
            box_height = p['height']

            # Konversi ke Pojok Kiri Atas & Kanan Bawah
            x0 = x_center - (box_width / 2)
            y0 = y_center - (box_height / 2)
            x1 = x_center + (box_width / 2)
            y1 = y_center + (box_height / 2)

            # Warna berdasarkan status (Healthy vs Unhealthy)
            label = p['class']
            is_healthy = "healthy" in label.lower() or "sehat" in label.lower()
            color = "#4CAF50" if is_healthy else "#FF5252" # Hijau atau Merah
            
            # 1. Gambar Kotak (Tebal 4px biar jelas)
            draw.rectangle([x0, y0, x1, y1], outline=color, width=4)
            
            # 2. Gambar Label Background
            text = f"{label} ({p['confidence']:.1%})"
            
            # Hitung ukuran teks menggunakan textbbox (Pillow versi baru)
            try:
                text_bbox = draw.textbbox((x0, y0), text, font=font)
                text_w = text_bbox[2] - text_bbox[0]
                text_h = text_bbox[3] - text_bbox[1]
            except AttributeError:
                # Fallback untuk Pillow versi lama
                text_w, text_h = draw.textsize(text, font=font)
            
            # Gambar background teks di atas kotak
            draw.rectangle([x0, y0 - text_h - 10, x0 + text_w + 10, y0], fill=color)
            
            # 3. Tulis Teks Putih
            draw.text((x0 + 5, y0 - text_h - 5), text, fill="white", font=font)

    return draw_image

def create_detection_summary(predictions, threshold):
    """Helper untuk membuat ringkasan jumlah deteksi"""
    valid_preds = [p for p in predictions if p['confidence'] >= threshold]
    unhealthy = [p for p in valid_preds if 'healthy' not in p['class'].lower()]
    healthy = [p for p in valid_preds if 'healthy' in p['class'].lower()]
    
    primary_disease = None
    if unhealthy:
        best_pred = max(unhealthy, key=lambda x: x['confidence'])
        primary_disease = best_pred['class']
        
    return {
        'total_detections': len(predictions),
        'filtered_detections': len(valid_preds),
        'healthy_count': len(healthy),
        'unhealthy_count': len(unhealthy),
        'primary_disease': primary_disease
    }