# test_api.py
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("ROBOFLOW_API_KEY")
print(f"API Key: {api_key}")
print(f"Length: {len(api_key) if api_key else 0}")

# Test Roboflow
from roboflow import Roboflow
try:
    rf = Roboflow(api_key=api_key)
    print("✅ API Key valid")
except Exception as e:
    print(f"❌ API Key error: {e}")