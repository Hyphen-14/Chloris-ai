# check_download.py
import os
from pathlib import Path

def check_downloaded_files():
    print("=== CHECKING DOWNLOADED FILES ===")
    
    # Cek seluruh struktur folder
    base_dir = Path(".")
    print("📁 Current directory structure:")
    
    for root, dirs, files in os.walk("."):
        # Skip venv dan folder besar lainnya
        if 'venv' in root or '.git' in root:
            continue
            
        level = root.replace(".", "").count(os.sep)
        indent = " " * 2 * level
        print(f"{indent}📂 {os.path.basename(root)}/")
        
        subindent = " " * 2 * (level + 1)
        for file in files:
            if file.endswith(('.pt', '.pth', '.zip', '.yaml')):
                print(f"{subindent}📄 {file}")

def search_for_model_files():
    print("\n=== SEARCHING FOR MODEL FILES ===")
    
    model_files = []
    for root, dirs, files in os.walk("."):
        for file in files:
            if file.endswith(('.pt', '.pth')):
                full_path = Path(root) / file
                model_files.append(full_path)
    
    if model_files:
        print("✅ Found model files:")
        for file in model_files:
            print(f"   📍 {file}")
            print(f"   📏 Size: {file.stat().st_size / (1024*1024):.1f} MB")
    else:
        print("❌ No .pt or .pth files found!")

if __name__ == "__main__":
    check_downloaded_files()
    search_for_model_files()