# server.py
from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from io import BytesIO
from PIL import Image
import uvicorn
import torch
import torchvision.transforms as T
import numpy as np
import json
from ultralytics import YOLO

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # untuk prototype. Batasi di production.
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ========== CONFIG ==========
MODEL_PATH = "model/best.pt"  # ganti dengan nama file modelmu
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
CONF_THRESHOLD = 0.35  # confidence threshold untuk filtering
# label map: ganti sesuai label training kamu (index -> name)
LABELS = {
    0: "healthy",
    1: "leaf_spot",
    2: "blight",
    # tambahkan sesuai modelmu
}

# ========== load model ==========
model = None

@app.on_event("startup")
def load_model():
    global model
    full_path = "model/best.pt"
    print(f"Loading YOLO model from {full_path} ...")

    try:
        model = YOLO(full_path)
        print("Model loaded successfully!")
    except Exception as e:
        print("ERROR loading YOLO model:", e)
        raise e
    print("Model loaded.")

# ========== preprocessing ==========
def preprocess_image(pil_image: Image.Image, img_size=(640, 640)):
    # Resize/letterbox sesuai kebutuhan modelmu.
    transform = T.Compose([
        T.Resize(img_size),
        T.ToTensor(),
        # Normalisasi: sesuaikan dengan preprocess saat training
        T.Normalize(mean=[0.485, 0.456, 0.406],
                    std=[0.229, 0.224, 0.225]),
    ])
    return transform(pil_image).unsqueeze(0)  # shape [1, C, H, W]

# ========== postprocess ==========
def postprocess_detections(raw_output, orig_w, orig_h, conf_thresh=CONF_THRESHOLD):
    """
    Harap sesuaikan fungsi ini dengan output modelmu.
    Beberapa model (Faster R-CNN) mengembalikan list of dicts like:
      [{ 'boxes': Tensor[N,4], 'labels': Tensor[N], 'scores': Tensor[N] }]
    YOLO custom might return Tensor with x,y,w,h,conf,class...
    Di sini kita tangani format common: list[dict].
    """
    results = []
    # jika raw_output adalah Tensor atau tuple, adapt di sini.
    if isinstance(raw_output, (list, tuple)) and len(raw_output) > 0 and isinstance(raw_output[0], dict):
        det = raw_output[0]
        boxes = det.get("boxes")
        labels = det.get("labels")
        scores = det.get("scores")
        if boxes is None:
            return results
        boxes = boxes.detach().cpu().numpy()
        labels = labels.detach().cpu().numpy()
        scores = scores.detach().cpu().numpy()
        for b, l, s in zip(boxes, labels, scores):
            if s < conf_thresh:
                continue
            x1, y1, x2, y2 = b.tolist()
            # clamp & scale if necessary (assume boxes in original image coords)
            # If model output was resized image coords, scale to orig size:
            # Here we assume boxes are already in orig coords. If not, implement scaling.
            results.append({
                "label_id": int(l),
                "label": LABELS.get(int(l), str(int(l))),
                "score": float(s),
                "box": {
                    "x1": float(max(0, x1)),
                    "y1": float(max(0, y1)),
                    "x2": float(min(orig_w, x2)),
                    "y2": float(min(orig_h, y2)),
                }
            })
    else:
        # fallback: try to interpret as tensor [N,6] => x1,y1,x2,y2,score,class
        try:
            out = raw_output.detach().cpu().numpy()
            if out.ndim == 2 and out.shape[1] >= 6:
                for row in out:
                    x1,y1,x2,y2,score,cls = row[:6]
                    if score < conf_thresh: continue
                    results.append({
                        "label_id": int(cls),
                        "label": LABELS.get(int(cls), str(int(cls))),
                        "score": float(score),
                        "box": {"x1": float(x1), "y1": float(y1), "x2": float(x2), "y2": float(y2)}
                    })
        except Exception:
            pass
    return results

# ========== endpoint ==========
@app.post("/predict-image")
async def predict_image(file: UploadFile = File(...)):
    contents = await file.read()
    try:
        img = Image.open(BytesIO(contents)).convert("RGB")
    except Exception as e:
        return {"ok": False, "error": f"Can't open image: {e}"}

    orig_w, orig_h = img.size

    try:
        # Jalankan inference menggunakan API ultralytics (menerima PIL.Image langsung)
        # sesuaikan parameter conf dan iou sesuai kebutuhan
        results = model(img, conf=CONF_THRESHOLD, stream=False)  # returns Results object or list

        detections = []
        # results bisa berupa list of Results; iterasi aman
        for r in results:
            # r.boxes bisa berisi banyak box. Gunakan .boxes.data atau .boxes.xyxy
            boxes = getattr(r, "boxes", None)
            if boxes is None:
                continue

            # boxes.data is tensor Nx6 [x1,y1,x2,y2,conf,class]
            # But ultralytics exposes box.xyxy, box.conf, box.cls
            for box in boxes:
                # box.xyxy is tensor of shape (4,) or box.xyxy[0]
                xyxy = box.xyxy.cpu().numpy().tolist()  # [x1,y1,x2,y2]
                conf = float(box.conf.cpu().numpy()) if hasattr(box, "conf") else float(box[4].cpu().numpy())
                cls = int(box.cls.cpu().numpy()) if hasattr(box, "cls") else int(box[5].cpu().numpy())

                x1, y1, x2, y2 = xyxy
                # normalisasi ke 0..1
                norm = {
                    "x1": max(0.0, min(1.0, x1 / orig_w)),
                    "y1": max(0.0, min(1.0, y1 / orig_h)),
                    "x2": max(0.0, min(1.0, x2 / orig_w)),
                    "y2": max(0.0, min(1.0, y2 / orig_h)),
                }

                label = r.names.get(cls, str(cls)) if hasattr(r, "names") else LABELS.get(cls, str(cls))

                detections.append({
                    "label": label,
                    "score": conf,
                    "box": norm
                })

        return {"ok": True, "detections": detections, "image_size": {"width": orig_w, "height": orig_h}}
    except Exception as e:
        # log error supaya gampang debug
        print("Inference error:", e)
        return {"ok": False, "error": str(e)}
