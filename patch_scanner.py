# patch_scanner.py
import os
from pathlib import Path

def patch_scanner_file():
    """Patch the old scanner.py file to work with new structure"""
    scanner_path = Path("app/pages/scanner.py")
    
    if not scanner_path.exists():
        print("❌ scanner.py not found")
        return False
    
    # Read the file
    with open(scanner_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Replace imports with new structure
    patches = {
        # Remove old imports
        "from roboflow import Roboflow": "",
        "import json": "",
        "import tempfile": "",
        
        # Add new imports
        "import streamlit as st": '''import streamlit as st
import time
from datetime import datetime

# Import modules
from modules.scanner.detector import RoboflowDetector
from modules.scanner.processor import ImageProcessor
from modules.disease.analyzer import analyze_detection_result, update_detection_state
from components.ui_cards import glass_card, metric_card, disease_result_card
from components.ui_widgets import create_slider, create_toggle, create_button, create_uploader
''',
        
        # Replace _map_to_disease_database calls
        "_map_to_disease_database": "analyze_detection_result",
        
        # Replace _update_detection_state
        "_update_detection_state": "update_detection_state",
        
        # Replace _sdk_inference_with_settings
        "_sdk_inference_with_settings": "RoboflowDetector().predict"
    }
    
    # Apply patches
    for old, new in patches.items():
        if old in content:
            if new:
                content = content.replace(old, new)
            else:
                # Remove the line
                lines = content.split('\n')
                lines = [line for line in lines if old not in line]
                content = '\n'.join(lines)
    
    # Write back
    with open(scanner_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ scanner.py patched successfully")
    return True


def main():
    """Main patch function"""
    print("🔧 PATCHING SCANNER.PY FOR NEW STRUCTURE")
    
    if patch_scanner_file():
        print("\n✅ Patch applied successfully!")
        print("The scanner.py file has been updated to work with the new modular structure.")
    else:
        print("\n❌ Patch failed")


if __name__ == "__main__":
    main()