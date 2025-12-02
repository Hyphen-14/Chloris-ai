# check_api_status.py
import requests

def check_api_key_status():
    print("=== CHECKING API KEY STATUS ===")
    
    api_key = "IbNv43xxhSDW6aWYIsqG"
    
    # Test different endpoints
    endpoints = [
        "https://api.roboflow.com/",
        f"https://api.roboflow.com/{api_key}",
        "https://detect.roboflow.com/crop-disease-identification-dnila/2"
    ]
    
    for endpoint in endpoints:
        try:
            response = requests.get(endpoint, timeout=10)
            print(f"🔗 {endpoint[:50]}... : {response.status_code}")
        except Exception as e:
            print(f"🔗 {endpoint[:50]}... : ERROR - {e}")

def test_with_simple_image():
    print("\n=== TESTING WITH SIMPLE IMAGE ===")
    
    api_key = "IbNv43xxhSDW6aWYIsqG"
    
    # Create a very simple test image
    import numpy as np
    image = np.ones((100, 100, 3), dtype=np.uint8) * 255  # White image
    
    # Encode
    import cv2
    _, buffer = cv2.imencode('.jpg', image)
    image_bytes = buffer.tobytes()
    
    try:
        response = requests.post(
            "https://detect.roboflow.com/crop-disease-identification-dnila/2",
            params={"api_key": api_key},
            data=image_bytes,
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            timeout=15
        )
        
        print(f"📤 API Response: {response.status_code}")
        if response.status_code == 200:
            print("✅ API WORKING!")
            results = response.json()
            print(f"   Predictions: {results}")
        elif response.status_code == 403:
            print("❌ 403 Forbidden - API Key invalid or no credits")
            print("   💡 Solution: Check API key or upgrade plan")
        elif response.status_code == 429:
            print("❌ 429 Rate Limited - Too many requests")
        else:
            print(f"❌ Error {response.status_code}: {response.text}")
            
    except Exception as e:
        print(f"❌ Request failed: {e}")

if __name__ == "__main__":
    check_api_key_status()
    test_with_simple_image()