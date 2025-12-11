"""
Styles untuk aplikasi CHLORIS (Final Version - Clean)
"""
# 🎨 Color Palette
COLORS = {
    "primary": "#4CAF50",
    "secondary": "#E8F5E9",
    "background": "#FAFAFA",
    "card_bg": "#FFFFFF",
    "text_main": "#333333",
    "text_body": "#555555",
    "success": "#4CAF50",
    "warning": "#FF9800",
    "error": "#F44336",
    "info": "#2196F3",
    "border": "#E0E0E0",
    "header_bg": "#EFF8F0",
    "light_gray": "#F5F5F5", "text_medium": "#555555", "text_dark": "#333333",
    "light_text": "#333333", "medium_text": "#666666", "text_light": "#888888",
    "dark_bg": "#FFFFFF", "darker_bg": "#F5F5F5", "white": "#FFFFFF", "primary_light": "#C8E6C9"
}

# --- PALET WARNA TANAMAN ---
PLANT_COLORS = {
    "🍅 Tomat": "#FF6347",
    "🥔 Kentang": "#CD853F",
    "🌽 Jagung": "#FFD700",
    "🥬 Selada": "#90EE90",
    "🌶️ Cabai/Paprika": "#DC143C",
    "🍓 Stroberi": "#FF69B4",
    "🥒 Mentimun": "#32CD32",
    "🌿 Tanaman Lain": "#808080"
}

# 🖌️ Global CSS Style
# PENTING: Semua CSS harus diapit oleh <style> dan </style>
CSS_THEME = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Poppins', sans-serif;
        color: #333333;
    }

    .stApp { background-color: #FAFAFA; }

    /* TEXT COLOR FORCING */
    h1, h2, h3, h4, h5, h6, p, label, li, span, div {
        color: #333333;
    }

    /* HEADER BOX STYLE */
    .header-box {
        background-color: #EFF8F0; /* Hijau Mint */
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(76, 175, 80, 0.08);
        border: 1px solid #C8E6C9;
        margin-bottom: 2rem;
    }

    /* PAGE HEADER BOX */
    .page-header-box {
        background-color: #E3F2FD; /* Biru Langit */
        padding: 20px;
        border-radius: 15px;
        border: 1px solid #BBDEFB;
        border-left: 6px solid #2196F3;
        box-shadow: 0 4px 6px rgba(0,0,0,0.03);
        margin-bottom: 25px;
    }

    /* TAB STYLING (KOTAK) */
    div[data-testid="stTabs"] { gap: 10px; }
    button[data-baseweb="tab"] {
        background-color: #FFFFFF !important;
        border: 1px solid #E0E0E0 !important;
        border-radius: 10px !important;
        padding: 10px 20px !important;
        margin-right: 10px !important;
        height: auto !important;
        box-shadow: 0 2px 4px rgba(0,0,0,0.02) !important;
    }
    button[data-baseweb="tab"] div { color: #555555 !important; font-weight: 600 !important; }
    button[data-baseweb="tab"][aria-selected="true"] {
        background-color: #E8F5E9 !important; border: 1px solid #4CAF50 !important; color: #4CAF50 !important;
    }
    button[data-baseweb="tab"][aria-selected="true"] div { color: #4CAF50 !important; }
    div[data-testid="stTabs"] div[data-baseweb="tab-highlight"] { display: none; }

    /* SIDEBAR & WIDGETS */
    [data-testid="stSidebar"] { background-color: #FFFFFF; border-right: 1px solid #E0E0E0; }
    .stButton > button {
        background-color: #4CAF50; color: white !important; border-radius: 12px; border: none;
        padding: 0.5rem 1rem; box-shadow: 0 4px 6px rgba(76, 175, 80, 0.2);
    }
    
    /* DROPDOWN FIX */
    div[data-baseweb="select"] > div, div[data-baseweb="popover"], ul[data-baseweb="menu"] {
        background-color: #FFFFFF !important; color: #333333 !important;
    }
    li[data-baseweb="option"] { color: #333333 !important; }
    
    /* INPUT FIELDS */
    .stTextInput input { color: #333333 !important; background-color: #FFFFFF !important; }
    
    /* CHART CONTAINER (NATIVE) */
    .chart-container {
        background-color: #FFFFFF;
        border: 1px solid #E0E0E0;
        border-radius: 15px;
        padding: 20px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        margin-bottom: 20px;
    }
    .chart-title {
        color: #333333; font-weight: 700; font-size: 1.1rem; text-align: center; margin-bottom: 15px;
    }
    
    header[data-testid="stHeader"] { background-color: rgba(255, 255, 255, 0.95); }
</style>
"""