# app/components/camera.py
import cv2
import time
import numpy as np
import streamlit as st
from src.utils.drawing import draw_glowing_box

class CameraController:
    def __init__(self):
        self.cap = None
        self.frame_count = 0
        
    def start_camera(self, camera_index=0):
        """Start camera capture"""
        try:
            self.cap = cv2.VideoCapture(camera_index)
            return self.cap.isOpened()
        except Exception as e:
            st.error(f"Camera error: {e}")
            return False
    
    def get_frame(self):
        """Get frame from camera"""
        if self.cap and self.cap.isOpened():
            ret, frame = self.cap.read()
            if ret:
                self.frame_count += 1
                return frame
        return None
    
    def stop_camera(self):
        """Stop camera capture"""
        if self.cap:
            self.cap.release()
            self.cap = None
    
    def should_process_frame(self, skip_frames=5):
        """Determine if current frame should be processed by AI"""
        return self.frame_count % skip_frames == 0
    
    def draw_detection(self, frame, detection_info):
        """Draw detection bounding box and label"""
        if not detection_info or 'bbox' not in detection_info:
            return frame
            
        x1, y1, x2, y2 = map(int, detection_info['bbox'])
        
        # Draw glowing box
        draw_glowing_box(frame, (x1, y1), (x2, y2))
        
        # Draw label
        label = f"{detection_info.get('class_name', 'Unknown')} :: {detection_info.get('confidence', 0):.1%}"
        cv2.rectangle(frame, (x1, y1-30), (x1 + 250, y1-5), (20, 30, 25), -1)
        cv2.putText(frame, label, (x1+10, y1-12), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (168, 232, 144), 1)
        
        return frame