import os
import csv
import shutil
import json
import streamlit as st
from datetime import datetime
import pandas as pd
from pathlib import Path

# --- 1. IMPORT DETEKSI ---
try:
    from .detection import perform_detection
except ImportError:
    def perform_detection(*args, **kwargs): return {'predictions': [], 'image': None}

# --- HELPER: Load Database ---
def load_disease_db():
    try:
        paths = [Path("data/diseases/penyakit.json"), Path("penyakit.json")]
        for p in paths:
            if p.exists():
                with open(p, 'r') as f: return json.load(f)
    except:
        return {}
    return {}

# --- 2. CORE LOGIC (STRICT MATCHING FIX) ---
def analyze_detection_results(detection_results, threshold):
    predictions = detection_results.get('predictions', [])
    valid_preds = [p for p in predictions if p['confidence'] >= threshold]
    
    analysis = {
        'is_healthy': True,
        'health_score': 100,
        'disease_risk': "Rendah",
        'avg_confidence': 0.0,
        'diagnosis': "Tidak Terdeteksi",
        'detailed_diagnosis': "Tidak ada tanaman atau penyakit yang terdeteksi.",
        'recommendations': ["Pastikan pencahayaan cukup", "Fokuskan kamera pada daun"],
        'plant_type': "Unknown",
        'model_used': "YOLOv8"
    }

    if not valid_preds:
        return analysis

    confidences = [p['confidence'] for p in valid_preds]
    avg_conf = sum(confidences) / len(confidences)
    analysis['avg_confidence'] = round(avg_conf * 100, 1)

    # Cek Sehat vs Sakit
    unhealthy_preds = [p for p in valid_preds if 'healthy' not in p['class'].lower()]
    
    db = load_disease_db()
    
    # Tentukan Target Class Utama
    if unhealthy_preds:
        top_pred = max(unhealthy_preds, key=lambda x: x['confidence'])
        target_class = top_pred['class'].lower().strip()
        analysis['is_healthy'] = False
        analysis['health_score'] = max(10, 100 - int(top_pred['confidence'] * 100))
    else:
        # Jika semua sehat, ambil yang confidence tertinggi
        top_pred = max(valid_preds, key=lambda x: x['confidence'])
        target_class = top_pred['class'].lower().strip()
        analysis['is_healthy'] = True
        analysis['health_score'] = 95

    # --- LOGIKA PENCOCOKAN KETAT (STRICT MATCHING) ---
    matched_key = None
    
    # 1. Exact Match (Persis Sama)
    if target_class in db:
        matched_key = target_class
    else:
        # 2. Smart Matching
        # Kita pecah target class jadi kata-kata penting (tanpa 'leaf', 'veggie', 'fruit', '-')
        # Contoh: "cucumber veggie - healthy" -> ["cucumber", "healthy"]
        ignore_words = ['leaf', 'veggie', 'fruit', '-', '_', 'plant']
        target_words = set([w for w in target_class.replace("-", " ").split() if w not in ignore_words])
        
        best_match_key = None
        max_overlap_score = 0
        
        for key in db.keys():
            # Filter Awal: Jika target UNHEALTHY, jangan cocokkan dengan kunci HEALTHY (dan sebaliknya)
            key_is_healthy = 'healthy' in key.lower() and 'unhealthy' not in key.lower()
            target_is_healthy = 'healthy' in target_class and 'unhealthy' not in target_class
            
            if key_is_healthy != target_is_healthy:
                continue # Skip jika status kesehatan beda

            # Hitung Skor Overlap
            key_words = set([w for w in key.lower().replace("-", " ").split() if w not in ignore_words])
            
            # Intersection (Kata yang sama)
            common_words = target_words.intersection(key_words)
            overlap_count = len(common_words)
            
            # --- ATURAN TAMBAHAN: NAMA TANAMAN HARUS ADA ---
            # Cari nama tanaman umum (cucumber, tomato, pepper, dll)
            plant_names = ['cucumber', 'tomato', 'potato', 'corn', 'lettuce', 'pepper', 'strawberry']
            plant_match = False
            for plant in plant_names:
                if plant in target_class and plant in key.lower():
                    plant_match = True
                    break
            
            # Beri bobot tinggi jika nama tanaman cocok
            score = overlap_count + (10 if plant_match else 0)
            
            if score > max_overlap_score:
                max_overlap_score = score
                best_match_key = key
        
        # Hanya ambil jika skornya cukup meyakinkan (ada nama tanaman yang cocok)
        if max_overlap_score >= 10:
            matched_key = best_match_key

    # --- HASIL AKHIR ---
    if matched_key and matched_key in db:
        info = db[matched_key]
        analysis['diagnosis'] = info['nama_id']
        analysis['disease_risk'] = info['tingkat_bahaya']
        analysis['detailed_diagnosis'] = f"Sistem mendeteksi **{info['nama_id']}**. (Deteksi asli: {target_class})"
        analysis['recommendations'] = info['solusi']
    else:
        # Fallback (Gunakan nama asli dari AI jika tidak ketemu di DB)
        analysis['diagnosis'] = top_pred['class']
        analysis['disease_risk'] = "Medium" if not analysis['is_healthy'] else "Rendah"
        analysis['detailed_diagnosis'] = f"Deteksi: **{top_pred['class']}**. Detail belum tersedia di database."
        analysis['recommendations'] = ["Konsultasikan dengan ahli"] if not analysis['is_healthy'] else ["Perawatan rutin"]

    return analysis

def create_detection_summary(predictions, threshold):
    valid_preds = [p for p in predictions if p['confidence'] >= threshold]
    unhealthy = [p for p in valid_preds if 'healthy' not in p['class'].lower()]
    healthy = [p for p in valid_preds if 'healthy' in p['class'].lower()]
    
    primary_disease = None
    if unhealthy:
        best_pred = max(unhealthy, key=lambda x: x['confidence'])
        primary_disease = best_pred['class']
    elif healthy:
        primary_disease = "Tanaman Sehat"
        
    return {
        'total_detections': len(predictions),
        'filtered_detections': len(valid_preds),
        'healthy_count': len(healthy),
        'unhealthy_count': len(unhealthy),
        'primary_disease': primary_disease
    }

# --- 3. API & HISTORY ---
def set_roboflow_api_key(api_key):
    st.session_state['roboflow_api_key'] = api_key

HISTORY_DIR = Path("data/history")
LOG_FILE = HISTORY_DIR / "detection_log.csv"

def init_history_db():
    if not HISTORY_DIR.exists(): HISTORY_DIR.mkdir(parents=True, exist_ok=True)
    if not LOG_FILE.exists():
        df = pd.DataFrame(columns=["timestamp", "filename", "disease_name", "confidence", "risk_level", "image_path"])
        df.to_csv(LOG_FILE, index=False)

def save_scan_result(image_pil, filename, disease_name, confidence, risk_level):
    init_history_db()
    safe_disease_name = "".join([c if c.isalnum() or c in (' ', '-', '_') else '_' for c in str(disease_name)]).strip()
    disease_folder = HISTORY_DIR / safe_disease_name
    disease_folder.mkdir(exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    save_filename = f"{timestamp}_{filename}"
    save_path = disease_folder / save_filename
    
    try:
        if image_pil.mode in ("RGBA", "P"): image_pil = image_pil.convert("RGB")
        image_pil.save(save_path, quality=95)
        
        new_record = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "filename": filename,
            "disease_name": disease_name,
            "confidence": confidence,
            "risk_level": risk_level,
            "image_path": str(save_path)
        }
        
        with open(LOG_FILE, 'a', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=new_record.keys())
            writer.writerow(new_record)
        return True, "Data berhasil disimpan!"
    except Exception as e:
        return False, f"Gagal: {str(e)}"

def get_history_dataframe():
    init_history_db()
    try: return pd.read_csv(LOG_FILE)
    except: return pd.DataFrame()

def delete_single_record(timestamp_str):
    """Menghapus satu data riwayat berdasarkan timestamp unik."""
    init_history_db()
    try:
        df = pd.read_csv(LOG_FILE)
        df['timestamp'] = df['timestamp'].astype(str)
        target_row = df[df['timestamp'] == timestamp_str]
        
        if target_row.empty: return False, "Data tidak ditemukan."
            
        image_path = target_row.iloc[0]['image_path']
        if os.path.exists(image_path): os.remove(image_path)
            
        df = df[df['timestamp'] != timestamp_str]
        df.to_csv(LOG_FILE, index=False)
        return True, "Data berhasil dihapus."
    except Exception as e:
        return False, f"Gagal menghapus: {str(e)}"

def clear_history_data():
    try:
        if HISTORY_DIR.exists(): shutil.rmtree(HISTORY_DIR)
        init_history_db()
        return True
    except: return False