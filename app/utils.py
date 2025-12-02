import cv2
import numpy as np

def draw_glowing_box(img, pt1, pt2, color=(144, 232, 168), thickness=2):
    """
    Menggambar bounding box dengan efek techy/glowing.
    Color: Mint Green (BGR Format untuk OpenCV)
    """
    x1, y1 = pt1
    x2, y2 = pt2
    r = 20 
    
    # Gambar garis sudut
    cv2.line(img, (x1, y1), (x1 + r, y1), color, thickness)
    cv2.line(img, (x1, y1), (x1, y1 + r), color, thickness)
    cv2.line(img, (x2, y1), (x2 - r, y1), color, thickness)
    cv2.line(img, (x2, y1), (x2, y1 + r), color, thickness)
    cv2.line(img, (x1, y2), (x1 + r, y2), color, thickness)
    cv2.line(img, (x1, y2), (x1, y2 - r), color, thickness)
    cv2.line(img, (x2, y2), (x2 - r, y2), color, thickness)
    cv2.line(img, (x2, y2), (x2, y2 - r), color, thickness)
    
    # Titik sudut bercahaya (Putih)
    glow_color = (255, 255, 255)
    cv2.circle(img, (x1, y1), 3, glow_color, -1)
    cv2.circle(img, (x2, y1), 3, glow_color, -1)
    cv2.circle(img, (x1, y2), 3, glow_color, -1)
    cv2.circle(img, (x2, y2), 3, glow_color, -1)
    
    return img