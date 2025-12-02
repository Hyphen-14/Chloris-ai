# scripts/collect_disease_data.py
import json
import requests
from pathlib import Path

def collect_disease_data():
    """Collect disease data from various sources"""
    
    base_data = {
        "template": {
            "nama_id": "",
            "latin": "", 
            "gejala": "",
            "solusi": [],
            "tingkat_bahaya": "",  # Aman, Low, Medium, High, Critical
            "pencegahan": [],
            "musim_rentan": "",
            "tanaman_rentan": "",
            "foto_contoh": "",
            "sumber": ""
        }
    }
    
    # Data yang perlu dikumpulkan
    diseases_to_research = [
        "leaf_miner",
        "caterpillar", 
        "aphids",
        "spider_mite",
        "root_rot",
        "fusarium_wilt",
        "verticillium_wilt",
        "gray_mold",
        "black_spot",
        "anthracnose"
    ]
    
    print("🔍 Diseases to research:", diseases_to_research)
    print("💡 Research sources:")
    print("   - PlantVillage Database")
    print("   - FAO Plant Protection")
    print("   - Local agricultural extension offices")
    print("   - Research papers on plant pathology")

if __name__ == "__main__":
    collect_disease_data()