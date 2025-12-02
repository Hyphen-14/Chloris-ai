# debug_camera.py
import cv2
import requests
import numpy as np
from pathlib import Path

def debug_camera_feed():
    print("=== CAMERA & API DEBUG ===")
    
    # Test 1: Camera Access
    print("1. Testing camera access...")
    cap = cv2.VideoCapture(0)
    if cap.isOpened():
        ret, frame = cap.read()
        if ret:
            print("✅ Camera OK - Frame captured")
            print(f"   Frame shape: {frame.shape}")
        else:
            print("❌ Camera can read but no frame")
    else:
        print("❌ Camera not accessible")
    cap.release()
    
    # Test 2: API Connection
    print("\n2. Testing API connection...")
    api_key = "IbNv43xxhSDW6aWYIsqG"
    
    # Create a real plant-like image for testing
    test_image = create_test_image()
    _, buffer = cv2.imencode('.jpg', test_image)
    image_bytes = buffer.tobytes()
    
    try:
        response = requests.post(
            "https://detect.roboflow.com/crop-disease-identification-dnila/2",
            params={"api_key": api_key, "confidence": 0.1},  # Very low confidence
            data=image_bytes,
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            timeout=10
        )
        
        print(f"✅ API Response: {response.status_code}")
        if response.status_code == 200:
            results = response.json()
            predictions = results.get('predictions', [])
            print(f"   Predictions found: {len(predictions)}")
            for pred in predictions:
                print(f"   - {pred['class']} ({pred['confidence']:.3f})")
        else:
            print(f"   Error: {response.text}")
            
    except Exception as e:
        print(f"❌ API Error: {e}")

def create_test_image():
    """Create a synthetic plant-like image for testing"""
    # Create green background (like a plant)
    image = np.zeros((640, 640, 3), dtype=np.uint8)
    image[:, :] = [50, 150, 50]  # Green color
    
    # Add some "disease" spots
    for _ in range(10):
        x, y = np.random.randint(100, 540, 2)
        radius = np.random.randint(5, 20)
        color = [30, 30, 30]  # Dark spots
        cv2.circle(image, (x, y), radius, color, -1)
    
    return image

if __name__ == "__main__":
    debug_camera_feed()