"""
Konfigurasi tema warna untuk aplikasi CHLORIS
Tema: Cerah dengan warna pastel variatif
"""

# Warna tema pastel variatif
COLORS = {
    # Primary - Hijau
    "primary": "#4CAF50",
    "primary_light": "#E8F5E9",
    "primary_lighter": "#F1F8E9",
    
    # Secondary - Biru
    "secondary": "#2196F3",
    "secondary_light": "#E3F2FD",
    
    # Accents - Variasi pastel
    "accent_yellow": "#FFF3E0",    # Kuning pastel
    "accent_orange": "#FFF8E1",    # Orange pastel
    "accent_purple": "#F3E5F5",    # Ungu pastel
    "accent_blue": "#E1F5FE",      # Biru pastel
    
    # Status
    "success": "#4CAF50",
    "warning": "#FF9800",
    "error": "#f44336",
    "info": "#2196F3",
    
    # Netral
    "white": "#FFFFFF",
    "light_gray": "#F5F5F5",
    "gray": "#E0E0E0",
    "dark_gray": "#757575",
    
    # Text
    "text_dark": "#2C3E50",
    "text_medium": "#546E7A",
    "text_light": "#90A4AE",
    
    # Card colors berdasarkan fungsi
    "card_diagnosis": "#E8F5E9",      # Hijau untuk diagnosis
    "card_recommendation": "#E1F5FE", # Biru untuk rekomendasi
    "card_metrics": "#FFF3E0",        # Kuning untuk metrics
    "card_upload": "#F3E5F5",         # Ungu untuk upload
}

# CSS untuk tema cerah
CSS_THEME = f"""
<style>
    /* RESET & BASE STYLES - BACKGROUND CERAH */
    .main {{
        background-color: {COLORS['white']};
        color: {COLORS['text_dark']};
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    }}
    
    /* SIDEBAR - HIJAU MUDA CERAH */
    section[data-testid="stSidebar"] {{
        background: linear-gradient(180deg, {COLORS['primary_lighter']} 0%, {COLORS['white']} 100%);
        border-right: 1px solid {COLORS['gray']};
    }}
    
    section[data-testid="stSidebar"] > div:first-child {{
        padding: 1.5rem;
    }}
    
    /* HEADER - GRADIENT HIJAU CERAH */
    .app-header {{
        background: linear-gradient(135deg, {COLORS['primary_lighter']} 0%, {COLORS['white']} 100%);
        padding: 2rem 0;
        margin-bottom: 2rem;
        border-radius: 15px;
        border: 1px solid {COLORS['primary_light']};
        box-shadow: 0 4px 12px rgba(76, 175, 80, 0.1);
    }}
    
    /* CARDS - WARNA VARIATIF BERDASARKAN FUNGSI */
    .card-diagnosis {{
        background: {COLORS['card_diagnosis']};
        border-left: 4px solid {COLORS['success']};
    }}
    
    .card-recommendation {{
        background: {COLORS['card_recommendation']};
        border-left: 4px solid {COLORS['info']};
    }}
    
    .card-metrics {{
        background: {COLORS['card_metrics']};
        border-left: 4px solid {COLORS['warning']};
    }}
    
    .card-upload {{
        background: {COLORS['card_upload']};
        border-left: 4px solid {COLORS['primary']};
    }}
    
    /* BASE CARD STYLE */
    .custom-card {{
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
        border: 1px solid {COLORS['gray']};
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
        transition: all 0.3s ease;
    }}
    
    .custom-card:hover {{
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.08);
        transform: translateY(-2px);
    }}
    
    .card-title {{
        color: {COLORS['text_dark']} !important;
        font-weight: 600;
        font-size: 1.25rem;
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }}
    
    /* BUTTONS - HIJAU CERAH */
    .stButton > button {{
        background-color: {COLORS['primary']};
        color: {COLORS['white']};
        border: none;
        border-radius: 8px;
        padding: 0.75rem 1.5rem;
        font-weight: 500;
        transition: all 0.2s ease;
    }}
    
    .stButton > button:hover {{
        background-color: #45a049;
        box-shadow: 0 4px 12px rgba(76, 175, 80, 0.2);
    }}
    
    /* METRICS - KUNING PASTEL */
    [data-testid="stMetric"] {{
        background: {COLORS['card_metrics']};
        border: 1px solid {COLORS['gray']};
        border-radius: 10px;
        padding: 1.25rem;
    }}
    
    [data-testid="stMetricLabel"] {{
        color: {COLORS['text_medium']};
        font-weight: 500;
    }}
    
    [data-testid="stMetricValue"] {{
        color: {COLORS['text_dark']};
        font-weight: 700;
    }}
    
    /* TABS */
    .stTabs [data-baseweb="tab-list"] {{
        background: {COLORS['white']};
        border-bottom: 1px solid {COLORS['gray']};
        gap: 0;
    }}
    
    .stTabs [data-baseweb="tab"] {{
        color: {COLORS['text_medium']};
        padding: 0.75rem 1.5rem;
        border-bottom: 2px solid transparent;
        transition: all 0.2s ease;
    }}
    
    .stTabs [data-baseweb="tab"]:hover {{
        color: {COLORS['primary']};
        background-color: {COLORS['primary_light']};
    }}
    
    .stTabs [aria-selected="true"] {{
        color: {COLORS['primary']} !important;
        background-color: {COLORS['white']};
        border-bottom: 2px solid {COLORS['primary']};
    }}
    
    /* UPLOAD AREA - UNGU PASTEL */
    .upload-area {{
        border: 2px dashed {COLORS['primary']};
        border-radius: 12px;
        background: {COLORS['card_upload']};
        padding: 3rem 2rem;
        text-align: center;
        transition: all 0.3s ease;
    }}
    
    .upload-area:hover {{
        background: {COLORS['white']};
        border-color: {COLORS['secondary']};
    }}
    
    /* TEXT STYLES */
    h1, h2, h3, h4, h5, h6 {{
        color: {COLORS['text_dark']} !important;
        font-weight: 600 !important;
    }}
    
    h1 {{
        color: {COLORS['primary']} !important;
        font-size: 2rem !important;
    }}
    
    p, span, label {{
        color: {COLORS['text_dark']} !important;
    }}
    
    /* STATUS BADGES */
    .status-healthy {{
        color: {COLORS['success']};
        font-weight: 600;
        background: {COLORS['card_diagnosis']};
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        display: inline-block;
    }}
    
    .status-warning {{
        color: {COLORS['warning']};
        font-weight: 600;
        background: {COLORS['card_metrics']};
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        display: inline-block;
    }}
    
    .status-critical {{
        color: {COLORS['error']};
        font-weight: 600;
        background: #FFEBEE;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        display: inline-block;
    }}
    
    /* EXPANDER */
    .streamlit-expanderHeader {{
        background: {COLORS['primary_light']};
        border-radius: 8px;
        color: {COLORS['text_dark']};
    }}
    
    .streamlit-expanderContent {{
        background: {COLORS['white']};
        border-radius: 0 0 8px 8px;
        border: 1px solid {COLORS['primary_light']};
        border-top: none;
    }}
    
    /* FOOTER */
    .app-footer {{
        margin-top: 3rem;
        padding-top: 1.5rem;
        border-top: 1px solid {COLORS['gray']};
        color: {COLORS['text_medium']};
        font-size: 0.9rem;
    }}
</style>
"""