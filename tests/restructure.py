# restructure.py
import os
import shutil
from pathlib import Path

def create_structure():
    """Create the new folder structure"""
    folders = [
        # App structure
        "app/pages",
        "app/components", 
        "app/assets",
        # Source structure
        "src/core",
        "src/training",
        "src/utils",
        # Data structure
        "data/models",
        "data/diseases",
        "data/datasets",
        "data/references",
        # Tests & Docs
        "tests",
        "docs",
        "scripts"
    ]
    
    for folder in folders:
        os.makedirs(folder, exist_ok=True)
        print(f"✅ Created: {folder}")
        
    # Create __init__.py files
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
        Path(init_file).touch()
        print(f"✅ Created: {init_file}")

if __name__ == "__main__":
    create_structure()
    print("🎉 Folder structure created successfully!")