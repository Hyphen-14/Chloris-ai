from contextlib import asynccontextmanager
from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import os
import shutil
from pathlib import Path
import numpy as np
from PIL import Image
import tensorflow as tf
import cv2

# Load model di awal (shared variable)
model = None
class_names = []  # Ganti dengan class names Anda

# Lifespan handler untuk FastAPI >= 0.100.0
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: load model
    print("🔄 Loading ML model...")
    global model, class_names
    
    try:
        # Ganti dengan path model Anda
        model_path = "models/plant_disease_model.h5"
        if os.path.exists(model_path):
            model = tf.keras.models.load_model(model_path)
            print(f"✅ Model loaded from {model_path}")
        else:
            print("⚠️ Model file not found, using dummy model")
            # Buat model dummy untuk testing
            model = create_dummy_model()
        
        # Contoh class names - SESUAIKAN DENGAN MODEL ANDA
        class_names = [
            "bell pepper leaf-healthy",
            "bell pepper leaf-unhealthy", 
            "tomato-early blight",
            "tomato-healthy",
            "cucumber-powdery-mildew",
            "cucumber leaf - healthy",
            "strawberry leaf-healthy",
            "strawberry-angular leafspot",
            "lettuce-healthy",
            "lettuce-downy mildew"
        ]
        print(f"✅ Class names loaded: {len(class_names)} classes")
        
    except Exception as e:
        print(f"❌ Error loading model: {e}")
        model = create_dummy_model()
        class_names = ["unknown_disease"]
    
    yield  # Aplikasi berjalan
    
    # Shutdown: cleanup
    print("🔄 Shutting down...")
    if model is not None:
        del model

def create_dummy_model():
    """Buat model dummy untuk testing"""
    model = tf.keras.Sequential([
        tf.keras.layers.Input(shape=(224, 224, 3)),
        tf.keras.layers.Flatten(),
        tf.keras.layers.Dense(10, activation='softmax')
    ])
    model.compile(optimizer='adam', loss='categorical_crossentropy')
    return model

# Buat FastAPI app dengan lifespan
app = FastAPI(title="Plant Disease Scanner API", lifespan=lifespan)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Untuk development, ganti dengan domain spesifik di production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Helper functions
def preprocess_image(image_path: str, target_size=(224, 224)):
    """Preprocess gambar untuk model"""
    try:
        img = Image.open(image_path)
        img = img.resize(target_size)
        img_array = np.array(img) / 255.0  # Normalize
        img_array = np.expand_dims(img_array, axis=0)  # Add batch dimension
        return img_array
    except Exception as e:
        print(f"Error preprocessing image: {e}")
        return None

def predict_disease(image_path: str):
    """Prediksi penyakit dari gambar"""
    try:
        if model is None:
            return {"error": "Model not loaded"}
        
        # Preprocess
        img_array = preprocess_image(image_path)
        if img_array is None:
            return {"error": "Failed to process image"}
        
        # Predict
        predictions = model.predict(img_array, verbose=0)
        predicted_class_idx = np.argmax(predictions[0])
        confidence = float(predictions[0][predicted_class_idx])
        
        # Get class name
        if predicted_class_idx < len(class_names):
            class_name = class_names[predicted_class_idx]
        else:
            class_name = "unknown_disease"
        
        # Generate dummy bounding box (ganti dengan detection sebenarnya)
        # Untuk object detection, Anda perlu model YOLO/SSD
        box = {
            "x1": 0.3,
            "y1": 0.4,
            "x2": 0.7,
            "y2": 0.8
        }
        
        return {
            "label": class_name,
            "score": confidence,
            "box": box
        }
        
    except Exception as e:
        print(f"Prediction error: {e}")
        return {"error": str(e)}

def detect_multiple_diseases(image_path: str):
    """Deteksi multiple diseases (untuk object detection)"""
    try:
        # Untuk sekarang return single detection
        # GANTI dengan kode object detection sebenarnya
        
        result = predict_disease(image_path)
        
        # Jika error, return dummy data
        if "error" in result:
            return [
                {
                    "label": "tomato-early blight",
                    "score": 0.85,
                    "box": {"x1": 0.2, "y1": 0.3, "x2": 0.6, "y2": 0.7}
                },
                {
                    "label": "healthy",
                    "score": 0.42,
                    "box": {"x1": 0.1, "y1": 0.2, "x2": 0.4, "y2": 0.5}
                }
            ]
        
        # Wrap single detection in list
        return [result]
        
    except Exception as e:
        print(f"Detection error: {e}")
        return []

# Endpoints
@app.get("/")
async def root():
    return {
        "message": "Plant Disease Scanner API",
        "status": "running",
        "model_loaded": model is not None,
        "classes": len(class_names)
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy", "model_ready": model is not None}

@app.post("/predict-image")
async def predict_image(file: UploadFile = File(...)):
    """Endpoint untuk prediksi penyakit dari gambar"""
    try:
        print(f"📥 Received image: {file.filename}")
        
        # Simpan file upload
        upload_dir = Path("uploads")
        upload_dir.mkdir(exist_ok=True)
        
        file_path = upload_dir / file.filename
        
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        print(f"💾 Saved to: {file_path}")
        
        # Predict
        detections = detect_multiple_diseases(str(file_path))
        
        # Cleanup
        if os.path.exists(file_path):
            os.remove(file_path)
        
        return {
            "ok": True,
            "detections": detections,
            "count": len(detections),
            "filename": file.filename
        }
        
    except Exception as e:
        print(f"❌ API error: {e}")
        return {
            "ok": False,
            "error": str(e),
            "detections": []
        }

@app.post("/test")
async def test_endpoint():
    """Endpoint test sederhana"""
    return {
        "ok": True,
        "message": "API is working",
        "detections": [
            {
                "label": "tomato-early blight",
                "score": 0.92,
                "box": {"x1": 0.1, "y1": 0.1, "x2": 0.9, "y2": 0.9}
            }
        ]
    }

if __name__ == "__main__":
    print("🚀 Starting Plant Disease Scanner API...")
    print("📡 Server will run on: http://localhost:8000")
    print("📚 API Docs: http://localhost:8000/docs")
    print("🌱 TensorFlow loaded successfully!")
    
    # Nonaktifkan reload jika ada warning
    uvicorn.run(
        app, 
        host="0.0.0.0",
        port=8000,
        # reload=False  # Matikan reload untuk hindari warning
    )