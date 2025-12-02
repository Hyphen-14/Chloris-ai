from ultralytics import YOLO
import yaml

# Cara 1: Load model dan cek class names
print("=== CLASS NAMES FROM MODEL ===")
model = YOLO('model/best.pt')
print("Model class names:", model.names)

# Cara 2: Cek dari data.yaml
print("\n=== CLASS NAMES FROM data.yaml ===")
with open('datasets/data.yaml', 'r') as f:
    data = yaml.safe_load(f)
    print("YAML class names:", data['names'])

# Cara 3: Bandingkan dengan penyakit.json
print("\n=== COMPARISON WITH penyakit.json ===")
import json
with open('data/penyakit.json', 'r') as f:
    penyakit_data = json.load(f)
    print("Penyakit.json keys:", list(penyakit_data.keys()))