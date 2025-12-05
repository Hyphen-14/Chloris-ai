# validate_model.py (CPU Version)
from ultralytics import YOLO
import yaml
import json
import numpy as np

def test_model_cpu():
    print("🔍 TESTING AI MODEL ON CPU...")
    
    try:
        # Load model dengan CPU
        model_path = 'model/best.pt'
        model = YOLO(model_path)
        
        # Force CPU
        model.overrides['device'] = 'cpu'
        
        print("✅ Model loaded on CPU successfully!")
        print(f"📋 Class names: {model.names}")
        
        # Test dengan dummy image
        dummy_image = np.random.randint(0, 255, (640, 640, 3), dtype=np.uint8)
        results = model(dummy_image)
        
        print("✅ Inference test passed!")
        
        return model.names
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

if __name__ == "__main__":
    test_model_cpu()