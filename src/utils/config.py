# src/utils/config.py
from pathlib import Path

# Base paths
PROJECT_ROOT = Path(__file__).parent.parent.parent
APP_DIR = PROJECT_ROOT / "app"
DATA_DIR = PROJECT_ROOT / "data"
MODEL_PATH = DATA_DIR / "models" / "best.pt"
DISEASE_DB_PATH = DATA_DIR / "diseases" / "penyakit.json"

# AI Settings
AI_CONFIDENCE_THRESHOLD = 0.5
DETECTION_FRAME_SKIP = 5
MAX_DETECTIONS = 10

# Camera Settings
CAMERA_WIDTH = 640
CAMERA_HEIGHT = 480
CAMERA_FPS = 30