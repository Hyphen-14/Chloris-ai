# 🌿 Chloris AI
**Smart Plant Disease Detector & Recovery Assistant**

> *"Menjaga Ketahanan Pangan, Satu Daun Setiap Waktu."*

## 📖 Tentang Project
**Chloris** adalah aplikasi berbasis Artificial Intelligence (AI) yang dirancang untuk membantu petani dan pecinta tanaman mendeteksi penyakit pada tanaman pangan secara dini. 

Berbeda dengan aplikasi klasik yang hanya mengklasifikasikan gambar statis, Chloris menggunakan teknologi **Object Detection (YOLO)** untuk memindai tanaman secara *real-time* dan memberikan lokasi spesifik penyakit pada daun. Tidak hanya mendiagnosa, Chloris juga memberikan saran perawatan untuk pemulihan.

## ✨ Fitur Utama
1.  **Real-Time Scanner:** Mendeteksi penyakit langsung dari kamera (webcam/HP) tanpa perlu memotret dulu.
2.  **Precise Localization:** Menandai area sakit dengan *bounding box* (kotak) agar pengguna tahu bagian mana yang harus dipangkas.
3.  **Smart Diagnosis & Solution:** Memberikan nama penyakit beserta saran penanganan (lingkungan & perawatan).
4.  **Recovery Tracker:** (Next Phase) Memantau perkembangan kesembuhan tanaman dari hari ke hari.
5.  **Offline Mode:** (Next Phase) Model AI yang ringan untuk digunakan di daerah minim sinyal.

## 🛠️ Tech Stack
* **Bahasa:** Python 3.10+
* **AI Core:** YOLOv8 (Ultralytics) - *State-of-the-Art Object Detection*
* **Dataset Management:** Roboflow (Format YOLO)
* **Version Control:** Git & GitHub
* **Deployment Target:** Localhost (Presentasi) & Mobile (Future)

---

## 🗺️ Roadmap Project (Tahap Pengerjaan)

Project ini dibagi menjadi 5 Fase utama agar pengerjaan terstruktur:

### ✅ Phase 1: Setup & Preparation (Minggu 1)
* [x] Pembentukan Tim & Ideasi.
* [x] Setup GitHub Repository & Struktur Folder.
* [ ] Setup Environment Python (Virtual Environment).
* [ ] Instalasi Library Utama (`ultralytics`, `opencv`, `pandas`).

### 🔄 Phase 2: Data Engineering (Minggu 2)
* [ ] **Dataset Hunting:** Mengumpulkan dataset penyakit tanaman (Target: *PlantDoc* atau Dataset Tomat/Cabai).
* [ ] **Data Cleaning:** Membuang gambar buram atau tidak relevan.
* [ ] **Preprocessing:** Resize gambar dan memastikan format anotasi (labeling) sesuai standar YOLO (.txt).

### 🤖 Phase 3: AI Training (Minggu 3)
* [ ] **Training Model:** Melatih YOLOv8n (Nano) agar mengenali penyakit.
* [ ] **Evaluation:** Mengecek akurasi model (mAP Score).
* [ ] **Tuning:** Memperbaiki parameter jika akurasi masih rendah.

### 💻 Phase 4: App Development (Minggu 4)
* [ ] Membuat script Python untuk menjalankan kamera (Webcam).
* [ ] Mengintegrasikan Model AI ke dalam script kamera.
* [ ] Menambahkan logika "Saran Solusi" (Jika terdeteksi 'Rust', tampilkan teks saran).

### 🚀 Phase 5: Finalization & Demo (Minggu 5)
* [ ] Testing di berbagai kondisi pencahayaan.
* [ ] Pembuatan Slide Presentasi.
* [ ] Dokumentasi Final (Video Demo).

---

## ⚙️ Cara Menjalankan Project (Untuk Tim)

1.  **Clone Repository**
    ```bash
    git clone [https://github.com/Hyphen-14/Chloris-ai.git](https://github.com/Hyphen-14/Chloris-ai.git)
    cd Chloris-ai
    ```

2.  **Buat & Aktifkan Virtual Environment (Windows)**
    ```bash
    python -m venv venv
    .\venv\Scripts\activate
    ```

3.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```
    *(Note: File requirements.txt akan diupdate setelah kita mulai coding)*

---
**Author:** Team Chloris @ BINUS University