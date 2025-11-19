import cv2
import numpy as np

def draw_glowing_box(img, pt1, pt2, color=(144, 232, 168), thickness=2):
    """
    Menggambar bounding box dengan efek techy/glowing di sudut-sudutnya.
    Default Color: Mint Green (BGR Format)
    """
    x1, y1 = pt1
    x2, y2 = pt2
    r = 20 # Panjang garis sudut
    
    # Gambar garis sudut (Corner Lines)
    # Kiri Atas
    cv2.line(img, (x1, y1), (x1 + r, y1), color, thickness)
    cv2.line(img, (x1, y1), (x1, y1 + r), color, thickness)
    # Kanan Atas
    cv2.line(img, (x2, y1), (x2 - r, y1), color, thickness)
    cv2.line(img, (x2, y1), (x2, y1 + r), color, thickness)
    # Kiri Bawah
    cv2.line(img, (x1, y2), (x1 + r, y2), color, thickness)
    cv2.line(img, (x1, y2), (x1, y2 - r), color, thickness)
    # Kanan Bawah
    cv2.line(img, (x2, y2), (x2 - r, y2), color, thickness)
    cv2.line(img, (x2, y2), (x2, y2 - r), color, thickness)
    
    # Tambahan titik sudut bercahaya (Aksen Putih)
    glow_color = (255, 255, 255)
    cv2.circle(img, (x1, y1), 3, glow_color, -1)
    cv2.circle(img, (x2, y1), 3, glow_color, -1)
    cv2.circle(img, (x1, y2), 3, glow_color, -1)
    cv2.circle(img, (x2, y2), 3, glow_color, -1)
    
    return img