# download_model_roboflow_new.py
from roboflow import Roboflow
import os
from pathlib import Path

def download_model_new():
    print("=== DOWNLOAD MODEL FROM ROBOFLOW (NEW VERSION) ===")
    
    # GANTI DENGAN INFORMASI ANDA
    API_KEY = "IbNv43xxhSDW6aWYIsqG"      # Dari Roboflow Account Settings
    WORKSPACE = "xof"       # Nama workspace Anda
    PROJECT = "crop-disease-identification-dniia"      # Nama project Anda  
    VERSION = 2                        # Versi model

    try:
        # Initialize Roboflow
        rf = Roboflow(api_key=API_KEY)
        
        print(f"🔗 Connecting to workspace: {WORKSPACE}")
        workspace = rf.workspace(WORKSPACE)
        
        print(f"📁 Accessing project: {PROJECT}")
        project = workspace.project(PROJECT)
        
        print(f"⬇️ Downloading version: {VERSION}")
        version = project.version(VERSION)
        
        # Download model dalam format YOLOv8
        print("💾 Downloading YOLOv8 model...")
        version.download(model_format="yolov8", location="models/")
        
        print("✅ Download completed successfully!")
        
        # Check downloaded files
        models_dir = Path("models")
        if models_dir.exists():
            print("\n📋 Files downloaded:")
            for file in models_dir.glob("*"):
                print(f"   - {file.name}")
                
        return True
        
    except Exception as e:
        print(f"❌ Download failed: {e}")
        return False

def alternative_manual_method():
    print("\n=== ALTERNATIVE MANUAL METHOD ===")
    print("Jika download code tidak bekerja, ikuti ini:")
    print("1. Di Roboflow, klik 'Deploy'")
    print("2. Pilih 'Edge Device'") 
    print("3. Pilih 'YOLOv8' format")
    print("4. Klik 'Show Download Code'")
    print("5. Copy code Python yang diberikan")
    print("6. Paste code tersebut di file baru dan jalankan")

def get_roboflow_info():
    print("\n=== CARA DAPATKAN INFORMASI ROBOFLOW ===")
    print("1. API_KEY:")
    print("   - Login ke app.roboflow.com")
    print("   - Klik profile picture → Account Settings") 
    print("   - Scroll ke 'Roboflow API' → Copy key")
    print("")
    print("2. WORKSPACE & PROJECT:")
    print("   - Pergi ke project Anda di Roboflow")
    print("   - Lihat URL: https://app.roboflow.com/{workspace}/{project}")
    print("   - Contoh: https://app.roboflow.com/john-doe/plant-disease")
    print("   - Maka: WORKSPACE = 'john-doe', PROJECT = 'plant-disease'")

if __name__ == "__main__":
    print("🌿 PLANT DISEASE MODEL DOWNLOADER")
    print("=" * 50)
    
    get_roboflow_info()
    
    print("\n" + "=" * 50)
    print("Ready to download? Make sure you have:")
    print("✅ API_KEY, WORKSPACE, PROJECT names")
    print("✅ Model training completed in Roboflow")
    print("✅ Internet connection")
    print("=" * 50)
    
    proceed = input("\nProceed with download? (y/n): ").lower().strip()
    
    if proceed == 'y':
        success = download_model_new()
        if success:
            print("\n🎉 DOWNLOAD SUCCESS! Next steps:")
            print("1. Run: python create_custom_database.py")
            print("2. Run: streamlit run app/main.py")
        else:
            print("\n❌ DOWNLOAD FAILED!")
            alternative_manual_method()
    else:
        print("Download cancelled.")