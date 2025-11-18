🌿 Panduan untuk App Developer - Project Chloris

Hey, Rayner dan Faiz!

Selamat datang di tim! Peranmu sangat krusial: kamu yang akan membuat "wajah" dan "badan" dari aplikasi Chloris.

FOKUS UTAMA: Membuat aplikasi Python yang bisa menyalakan webcam, mengambil gambar real-time, dan menampilkannya di layar.

TUGAS SEKUNDER: Menerima hasil deteksi AI (nanti berupa file model .pt dari [Yasin]) dan menggambar kotak/teks di atas video feed.

Kamu TIDAK PERLU pusing soal training AI. Anggap saja file AI-nya adalah black box yang sudah jadi.

🛠️ Tech Stack & Inspirasi Desain

Untuk membuat UI yang modern, kita TIDAK AKAN pakai tkinter atau PyQt yang kaku dan jadul.

Kita akan pakai framework modern yang dibuat khusus untuk project data science & AI:

Streamlit (Rekomendasi Utama):

Kenapa: Sangat gampang, 100% Python murni. Kamu cuma nulis st.title("Chloris AI") langsung jadi judul web keren. Cocok untuk demo real-time video.

Install: pip install streamlit

Jalankan: streamlit run src/app.py

Gradio (Alternatif):

Kenapa: Mirip Streamlit, sangat cepat untuk bikin demo AI. Tampilannya bersih dan modern.

Install: pip install gradio

Inspirasi Desain Modern:
Cek website ini untuk dapat "feel" desain yang kita kejar:

Dribbble.com (Cari: "plant app", "AI dashboard", "scanner app")

Behance.net

Workflow GitHub (WAJIB DIIKUTI!)

Supaya kerja kita gak bentrok, JANGAN PERNAH coding langsung di branch main. Selalu ikuti alur ini:

Langkah 1: Selalu Ambil Update Terbaru
Sebelum mulai coding, pastikan kodemu sama dengan yang ada di server.

# Pindah ke branch utama
git checkout main

# Tarik update terbaru dari server
git pull origin main


Langkah 2: Buat "Meja Kerja" Sendiri (Branch Baru)
Buat cabang baru dengan nama yang jelas sesuai fitur yang kamu kerjakan.

# Buat dan langsung pindah ke branch baru
git checkout -b feature-webcam-ui


(Nama feature-webcam-ui hanya contoh, boleh ganti)

Langkah 3: Coding!
Sekarang kamu aman untuk coding di branch-mu.

Buat file src/app.py

Mulai coding pakai Streamlit dan OpenCV.

(Lihat contoh kode starter di bawah)

Langkah 4: Simpan dan Kirim Karyamu (ke Cabangmu)
Setelah selesai (atau sore hari sebelum bubar), simpan kerjamu.

# Daftarkan semua file yang kamu ubah
git add .

# Bungkus dengan pesan yang jelas
git commit -m "feat: Menambahkan UI webcam dasar dengan Streamlit"

# Kirim ke server (tapi ke cabangmu, BUKAN ke main)
git push origin feature-webcam-ui


Langkah 5: Minta Review (Pull Request)
Ini adalah cara "minta izin" untuk menggabungkan kodemu ke main.

Buka website GitHub repository kita.

Akan muncul pop-up kuning feature-webcam-ui had recent pushes.

Klik tombol "Compare & pull request".

Kasih judul (misal: "Fitur Webcam UI Selesai") dan di deskripsi, mention @[Username-GitHub-Ketua-Tim] (Ketua timmu).

Klik "Create pull request".

Nanti tim akan review kodemu. Kalau sudah aman, baru kita Merge (gabungkan) ke main.

🚀 Kode Starter Pack (src/app.py)

Ini adalah kode awal untuk src/app.py menggunakan Streamlit dan OpenCV. Fokus kita adalah menyalakan kamera dulu.

import streamlit as st
import cv2
import numpy as np
# from ultralytics import YOLO # <-- Nanti kita aktifkan ini

# --- Konfigurasi Halaman Streamlit ---
st.set_page_config(
    page_title="Chloris AI - Smart Plant Scanner",
    page_icon="🌿",
    layout="wide"
)

# --- Judul & Deskripsi ---
st.title("🌿 Chloris AI Scanner")
st.markdown("Arahkan kamera ke daun tanaman untuk deteksi *real-time*.")

# --- Nanti kita load model AI di sini ---
# model_path = '../models/best.pt' # <-- Contoh path
# try:
#     model = YOLO(model_path)
# except Exception as e:
#     st.error(f"Error loading model: {e}")

# --- Area Tampilan Video ---
stframe = st.empty()
cap = cv2.VideoCapture(0) # 0 = Webcam bawaan

if not cap.isOpened():
    st.error("Gagal membuka webcam. Pastikan kamera tidak dipakai aplikasi lain.")
else:
    while cap.isOpened():
        success, frame = cap.read()
        if not success:
            st.error("Gagal membaca frame dari webcam.")
            break
        
        # --- NANTI PROSES AI DI SINI ---
        # 1. Kirim 'frame' ke model AI
        # results = model(frame)
        # 2. Gambar kotak hasil deteksi ke 'frame'
        # annotated_frame = results[0].plot()
        
        # --- Untuk sekarang, kita tampilkan frame asli dulu ---
        annotated_frame = frame
        
        # Tampilkan frame di Streamlit
        # (OpenCV pakai BGR, Streamlit pakai RGB, jadi harus dibalik warnanya)
        try:
            stframe.image(cv2.cvtColor(annotated_frame, cv2.COLOR_BGR2RGB),
                          channels="RGB",
                          use_column_width=True)
        except Exception as e:
            st.error(f"Error displaying frame: {e}")
            break

    cap.release()
    cv2.destroyAllWindows()


Tugas Pertamamu:

Ikuti alur GitHub (Pull, Checkout branch baru).

Buat file src/app.py dan requirements.txt (isi dengan streamlit, opencv-python, ultralytics).

Jalankan kode di atas (streamlit run src/app.py) dan pastikan webcam-mu nyala di browser.

Kalau sudah, push ke branch-mu dan buat Pull Request.

Semangat! Kalau bingung, tanya di grup.