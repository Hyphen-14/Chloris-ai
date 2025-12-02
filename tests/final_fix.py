# final_fix.py
import os
import shutil
import sys
from pathlib import Path

def final_fix():
    print("🔧 Running final fixes...")
    
    # 1. Fix Python path for testing
    project_root = Path(__file__).parent
    sys.path.insert(0, str(project_root))
    
    # 2. Fix penyakit.json location
    source_locations = [
        "App/data/penyakit.json",
        "app/data/penyakit.json", 
        "data/penyakit.json"
    ]
    
    target_location = "data/diseases/penyakit.json"
    
    for source in source_locations:
        if os.path.exists(source):
            os.makedirs(Path(target_location).parent, exist_ok=True)
            shutil.copy2(source, target_location)
            print(f"✅ Copied: {source} → {target_location}")
            break
    else:
        # Create minimal penyakit.json if not found
        Path(target_location).parent.mkdir(parents=True, exist_ok=True)
        minimal_json = {
            "healthy": {
                "nama_id": "Tanaman Sehat", 
                "latin": "Plantae sanus",
                "gejala": "Daun hijau segar, tidak ada bercak.",
                "solusi": ["Lanjutkan perawatan rutin."],
                "tingkat_bahaya": "Aman"
            }
        }
        import json
        with open(target_location, 'w', encoding='utf-8') as f:
            json.dump(minimal_json, f, indent=2, ensure_ascii=False)
        print(f"✅ Created minimal {target_location}")
    
    # 3. Ensure all __init__.py files
    init_files = [
        "app/__init__.py",
        "app/pages/__init__.py",
        "app/components/__init__.py", 
        "src/__init__.py",
        "src/core/__init__.py",
        "src/training/__init__.py",
        "src/utils/__init__.py",
        "tests/__init__.py"
    ]
    
    for init_file in init_files:
        Path(init_file).parent.mkdir(parents=True, exist_ok=True)
        Path(init_file).touch()
    
    print("✅ All __init__.py files created")
    
    # 4. Test imports
    print("\n🧪 Testing imports...")
    try:
        from app.styles import load_css
        print("✅ app.styles - OK")
        
        from src.utils.drawing import draw_glowing_box
        print("✅ src.utils.drawing - OK")
        
        print("🎉 All imports working!")
        
    except ImportError as e:
        print(f"❌ Import failed: {e}")
        return False
    
    return True

if __name__ == "__main__":
    if final_fix():
        print("\n🎊 All fixes applied successfully!")
        print("\n📋 Next steps:")
        print("1. Run: python test_structure.py")
        print("2. Run: cd app && streamlit run main.py")
    else:
        print("\n💥 Fixes failed. Please check manually.")