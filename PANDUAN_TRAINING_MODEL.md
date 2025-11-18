# 🚀 Panduan Training Model YOLOv8 — Chloris AI  
*(Laptop RTX 4060 / RTX 40-Series Ready)*

Halo!  
Dokumen ini berfungsi sebagai **panduan lengkap** untuk melakukan training AI model YOLOv8 dari awal.  
Dikhususkan untuk laptop dengan GPU RTX 4050 / 4060 / 4070 atau lebih tinggi.

---

## 🎯 Tujuan

1. Setup Python environment yang **bersih** & **ringan**
2. Training YOLOv8 menggunakan **GPU CUDA**
3. Dataset tidak di-push (diunduh otomatis)
4. Memastikan semua member tim bisa:
   - install environment ulang
   - download dataset ulang
   - melakukan training ulang

---

## 🛠 Software yang Harus Terpasang

### 1. Python 3.10 — **WAJIB versi ini**
**Download:**
https://www.python.org/downloads/release/python-31011/

Saat install, centang:
* [✔] Add Python 3.10 to PATH


---

### 2. Git
**Download:**
https://git-scm.com/downloads


---

### 3. NVIDIA Driver Terbaru
Via **GeForce Experience → Drivers → Update**

---

# STEP PENGERJAAN
-----
1. ## 📦 Clone Repo

**Buka folder yang kamu mau, lalu:**

```bash
git clone https://github.com/Hyphen-14/Chloris-ai.git
cd Chloris-ai
```

---

2. ## 🧪 Setup Virtual Environment

*** Note : venv tidak di-push ke repo ***
```bash
py -3.10 -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
```

---

**Kalau berhasil:**
```bash
(venv) PS D:\Chloris-ai>
```

---

3. ## 🔥 Install PyTorch CUDA untuk RTX 40-Series

**Wajib CUDA 12.1:**
```bash
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
```

---

4. ## 📥 Install Dependensi Lain
```bash
pip install ultralytics roboflow opencv-python pandas
```

---

5. ## 📌 Generate requirements.txt (Penting!)

**Ini file yang akan dipakai tim lain:**
*Jalankan:*
```bash
pip freeze > requirements.txt
```

---

6. ## 📂 Download Dataset (Tidak Ada di GitHub)

**Dataset sengaja tidak dipush ke repo agar repo tetap ringan.**

*Kamu butuh API key Roboflow (minta ke Yasin)*

**Jalankan:**
```bash
python src/download_data.py
```

---

**Jika berhasil → muncul folder:**
```bash
datasets/
  └── PlantDoc-1/
      ├── train/
      ├── valid/
      ├── test/
      └── data.yaml
```
---

7. ## 🏁 Mulai Training Model YOLOv8

**Terminal:**
```bash
python src/train.py
```
---

8. ## 🎉 Tanda Training Berhasil

* Kipas laptop bunyi kencang 🌀

* GPU Usage naik 70–95%

* Terminal nunjukin progress:
```bash
epoch 1/50 | loss 2.13 | mAP 0.48 | speed: 19ms/it
```

9. ## 📤 Cara Berbagi Model Tanpa GitHub Error

*File .pt TIDAK boleh dipush ke Git.*

### Upload model ke:

* Google Drive
* Mega
* Dropbox

Lalu tempel link di README:


