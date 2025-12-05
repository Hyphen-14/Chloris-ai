# verify_structure.py
import os
from pathlib import Path

def verify_project_structure(base_dir=None):
    """Verify the new project structure"""
    base_dir = Path(base_dir) if base_dir else Path.cwd()
    
    print("🔍 VERIFYING PROJECT STRUCTURE")
    print("="*60)
    
    # Expected structure
    expected_structure = {
        "app/": [
            "main.py",
            "config.py",
            "styles.py",
            "utils.py",
            "components/sidebar.py",
            "components/ui_cards.py",
            "components/ui_widgets.py",
            "pages/scanner.py",
            "pages/encyclopedia.py",
            "pages/reports.py",
            "pages/settings.py",
            "modules/disease/__init__.py",
            "modules/disease/mapper.py",
            "modules/disease/database.py",
            "modules/disease/analyzer.py",
            "modules/scanner/__init__.py",
            "modules/scanner/detector.py",
            "modules/scanner/processor.py",
        ],
        "data/diseases/": [
            "penyakit.json"
        ],
        "": [
            ".env",
            "requirements.txt",
            "README.md"
        ]
    }
    
    missing = []
    found = 0
    
    for directory, files in expected_structure.items():
        dir_path = base_dir / directory
        
        for file in files:
            file_path = dir_path / file if directory else base_dir / file
            
            if file_path.exists():
                print(f"✅ {file_path.relative_to(base_dir)}")
                found += 1
            else:
                print(f"❌ MISSING: {file_path.relative_to(base_dir)}")
                missing.append(str(file_path.relative_to(base_dir)))
    
    print("\n" + "="*60)
    print(f"📊 Verification Results:")
    print(f"   ✅ Found: {found} files")
    print(f"   ❌ Missing: {len(missing)} files")
    
    if missing:
        print("\n⚠️  Missing files:")
        for item in missing:
            print(f"   - {item}")
        
        print("\n🔧 To fix missing files:")
        print("1. Copy penyakit.json to data/diseases/")
        print("2. Run: python restructure_project.py again")
        print("3. Or manually create missing files")
    
    return len(missing) == 0


def check_requirements():
    """Check if required packages are installed"""
    print("\n📦 CHECKING REQUIRED PACKAGES")
    print("="*60)
    
    required_packages = [
        "streamlit",
        "opencv-python",
        "numpy", 
        "roboflow",
        "python-dotenv"
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.replace("-", "_"))
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package}")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n⚠️  Missing packages: {', '.join(missing_packages)}")
        print("Install with: pip install " + " ".join(missing_packages))
    
    return len(missing_packages) == 0


def main():
    """Main verification function"""
    print("🔧 CHLORIS AI STRUCTURE VERIFIER")
    
    # Verify structure
    structure_ok = verify_project_structure()
    
    # Check requirements
    requirements_ok = check_requirements()
    
    print("\n" + "="*60)
    
    if structure_ok and requirements_ok:
        print("🎉 Everything looks good! You can run:")
        print("   streamlit run app/main.py")
        return True
    else:
        print("⚠️  Some issues found. Please fix them before running the app.")
        return False


if __name__ == "__main__":
    main()