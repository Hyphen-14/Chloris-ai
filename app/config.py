import os
from pathlib import Path

# Impor COLORS dan CSS_THEME dari styles.py
# Pastikan tidak ada circular import (styles tidak boleh import config)
from styles import COLORS, CSS_THEME

# Base Directory
BASE_DIR = Path(__file__).parent.parent

# Definisikan path penting lainnya
ASSETS_DIR = BASE_DIR / "assets"
MODEL_DIR = BASE_DIR / "models"

# --- TAMBAHAN BARU: WARNA SPESIFIK TANAMAN ---
PLANT_COLORS = {
    "🍅 Tomat": "#FF6347",          # Merah Tomat
    "🥔 Kentang": "#CD853F",        # Coklat Kentang
    "🌽 Jagung": "#FFD700",         # Kuning Jagung
    "🥬 Selada": "#90EE90",         # Hijau Muda
    "🌶️ Cabai/Paprika": "#DC143C",  # Merah Cabai
    "🍓 Stroberi": "#FF69B4",       # Pink Stroberi
    "🥒 Mentimun": "#32CD32",       # Lime Green
    "🌿 Tanaman Lain": "#808080"    # Abu-abu
}