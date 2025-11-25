from ultralytics import YOLO

# --- Fungsi Utama untuk Proses Training ---
def train_model():
    # 1. Pilih Model Dasar
    # Kita pakai 'yolov8s.pt' (Small). Kecil, cepat, dan lebih pintar dari Nano.
    model = YOLO('yolov8s.pt')
    
    # 2. Tentukan Device (Langsung Arahkan ke GPU)
    # Kita tahu PyTorch sudah mendeteksi CUDA, jadi kita langsung pakai device 0.
    # Jika suatu saat PyTorch gagal mendeteksi GPU, training akan gagal.
    device_id = 0
    
    print(f"Menggunakan perangkat (device): {device_id} (GPU)")
    print("\nTraining dimulai... Siapin kipas laptop! 😎🔥")

    # 3. Mulai Training
    results = model.train(
        data='datasets/data.yaml',    # Path ke file data.yaml
        epochs=50,                    # Jumlah epoch training
        batch=16,                     # Ukuran batch
        imgsz=640,                    # Ukuran gambar (input standard YOLO)
        device=device_id,             # Langsung menggunakan GPU (device 0)
        optimizer='auto',             # Gunakan optimizer otomatis (default: SGD/AdamW)
        cos_lr=True,                  # Cosine learning rate schedule (lebih halus)
        patience=20,                  # Early stopping jika tidak ada peningkatan selama 20 epoch
        name='chloris-ai-model'       # Nama folder hasil training
    )

    print("\nTraining selesai! Model tersimpan di folder 'runs/train/chloris-ai-model'")

    # 4. Evaluasi Akhir Model
    evaluate_model('runs/train/chloris-ai-model/weights/best.pt', 'datasets/data.yaml') 

def evaluate_model(model_path, data_config):
    """Memuat model yang sudah tersimpan dan menjalankan validasi/evaluasi."""
    print("\n=============================================")
    print("Mulai Evaluasi Akhir Model...")
    print("=============================================")
    
    try:
        model = YOLO(model_path)
        results = model.val(data=data_config) 
        
        print("\n--- HASIL AKHIR EVALUASI (VALIDASI) ---")
        print(f"mAP50 (Mean Average Precision @ IoU 0.5): {results.box.map50:.4f}")
        print(f"mAP50-95 (Mean Average Precision @ IoU 0.5-0.95): {results.box.map:.4f}")
        print("--------------------------------------")
        
    except Exception as e:
        print(f"ERROR saat evaluasi: {e}")


# --- MAIN ENTRY POINT (Penting untuk Windows Multiprocessing) ---
if __name__ == '__main__':
    train_model()