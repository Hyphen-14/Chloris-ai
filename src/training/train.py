from ultralytics import YOLO
import torch
#1. Pilih Model Dasar
# Kita pakai 'yolov8n.pt' (Nano). Ini versi paling kecil & cepat.
# Cocok untuk laptop dan HP. Kalau mau lebih pintar tapi berat, ganti jadi 'yolov8s.pt'
model = YOLO('yolov8s.pt')
print("GPU:", torch.cuda.get_device_name(0))

#2. Mulai Training
# Pastikan path data.yaml sudah benar!
print("Training dimulai... Siapin kipas laptop 😎🔥")

results = model.train(
    data='datasets/data.yaml',  # Path ke file data.yaml
    epochs=50,                  # Jumlah epoch training
    batch=16,                   # Ukuran batch
    imgsz=640,                  # Ukuran gambar (input standard YOLO)
    device = 0,
    optimizer = 'auto',         # Gunakan optimizer otomatis
    cos_lr=True,                # Gunakan cosine learning rate schedule(lebih halus)
    patience=20,                # Early stopping jika tidak ada peningkatan selama 20 epoch
    name='chloris-ai-model',
    amp = False     # Nama folder hasil training
)

print("Training selesai! Model tersimpan di folder 'runs/train/chloris-ai-model'")