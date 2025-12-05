# restructure_project.py
import os
import shutil
import sys
from pathlib import Path
import time

class ProjectRestructurer:
    def __init__(self, base_dir=None):
        """Initialize with base directory"""
        self.base_dir = Path(base_dir) if base_dir else Path.cwd()
        print(f"📁 Working directory: {self.base_dir}")
        
        # Struktur folder baru yang diinginkan
        self.new_structure = {
            "app": {
                "components": {
                    "sidebar.py": None,
                    "ui_cards.py": None,
                    "ui_widgets.py": None,
                    "camera": {
                        "__init__.py": None,
                        "camera_capture.py": None,
                        "camera_utils.py": None
                    }
                },
                "pages": {
                    "scanner.py": None,
                    "encyclopedia.py": None,
                    "reports.py": None,
                    "settings.py": None
                },
                "modules": {
                    "disease": {
                        "__init__.py": None,
                        "mapper.py": None,
                        "database.py": None,
                        "analyzer.py": None
                    },
                    "scanner": {
                        "__init__.py": None,
                        "detector.py": None,
                        "processor.py": None,
                        "validator.py": None
                    },
                    "api": {
                        "__init__.py": None,
                        "roboflow_client.py": None,
                        "api_validator.py": None
                    },
                    "analytics": {
                        "__init__.py": None,
                        "reporter.py": None,
                        "visualizer.py": None
                    }
                },
                "assets": {
                    "images": {
                        "chloris_logo-removebg.png": None
                    }
                },
                "__init__.py": "",
                "main.py": None,
                "styles.py": None,
                "utils.py": None,
                "config.py": None
            },
            "data": {
                "diseases": {
                    "penyakit.json": None
                },
                "datasets": {},
                "references": {}
            },
            "docs": {},
            "scripts": {
                "check_gpu.py": None,
                "check_torch.py": None,
                "collect_disease_data.py": None
            },
            "tests": {
                "__init__.py": "",
                "test_disease_mapper.py": None,
                "test_scanner.py": None,
                "test_api.py": None
            }
        }
        
        # File-file yang harus dipertahankan
        self.essential_files = [
            ".env",
            ".gitignore",
            "README.md",
            "requirements.txt",
            "PANDUAN_APP_DEVELOPER.md",
            "PANDUAN_TRAINING_MODEL.md"
        ]
        
        # Folder lama yang akan dihapus/dipindahkan
        self.old_dirs_to_remove = [
            "app/src",
            "app/AppPrev",
            "src/AppPrev",
            "src/function",
            "src/training"
        ]

    def create_directory_structure(self):
        """Create new directory structure"""
        print("\n" + "="*60)
        print("🏗️  CREATING NEW DIRECTORY STRUCTURE")
        print("="*60)
        
        total_created = 0
        total_errors = 0
        
        def create_structure(base_path, structure, indent=0):
            nonlocal total_created, total_errors
            
            for name, content in structure.items():
                path = base_path / name
                
                # Create directory
                if content is not None and isinstance(content, dict):
                    try:
                        path.mkdir(parents=True, exist_ok=True)
                        print(f"{'  ' * indent}📁 Created: {path.relative_to(self.base_dir)}")
                        total_created += 1
                        
                        # Create __init__.py if it's a Python package
                        if name not in ["assets", "data", "docs", "scripts", "tests"]:
                            init_file = path / "__init__.py"
                            if not init_file.exists():
                                init_file.write_text("# Package initialization\n")
                                total_created += 1
                        
                        # Recursively create subdirectories
                        create_structure(path, content, indent + 1)
                        
                    except Exception as e:
                        print(f"{'  ' * indent}❌ Error creating {path}: {e}")
                        total_errors += 1
                
                # Create file
                elif content is None:
                    try:
                        if not path.exists():
                            path.touch()
                            print(f"{'  ' * indent}📄 Created: {path.relative_to(self.base_dir)}")
                            total_created += 1
                    except Exception as e:
                        print(f"{'  ' * indent}❌ Error creating {path}: {e}")
                        total_errors += 1
        
        # Start creating structure from base directory
        create_structure(self.base_dir, self.new_structure)
        
        print(f"\n✅ Structure created: {total_created} items")
        if total_errors > 0:
            print(f"⚠️  Errors: {total_errors}")
        
        return total_created

    def cleanup_old_structure(self, backup=True):
        """Clean up old directories and files"""
        print("\n" + "="*60)
        print("🧹 CLEANING UP OLD STRUCTURE")
        print("="*60)
        
        total_removed = 0
        total_backed_up = 0
        
        # Backup directory
        backup_dir = self.base_dir / "backup_old" / time.strftime("%Y%m%d_%H%M%S")
        
        if backup:
            backup_dir.mkdir(parents=True, exist_ok=True)
        
        # Remove old directories
        for old_dir in self.old_dirs_to_remove:
            dir_path = self.base_dir / old_dir
            if dir_path.exists():
                try:
                    if backup:
                        # Copy to backup
                        backup_path = backup_dir / old_dir
                        backup_path.parent.mkdir(parents=True, exist_ok=True)
                        shutil.copytree(dir_path, backup_path, dirs_exist_ok=True)
                        total_backed_up += 1
                        print(f"📦 Backed up: {old_dir}")
                    
                    # Remove directory
                    shutil.rmtree(dir_path)
                    print(f"🗑️  Removed: {old_dir}")
                    total_removed += 1
                    
                except Exception as e:
                    print(f"❌ Error removing {old_dir}: {e}")
        
        # Clean up orphaned Python files in root
        root_py_files = [
            "download_model.py",
            "check_classes.py",
            "create_custom_database.py",
            "temp_frame.jpg"
        ]
        
        for py_file in root_py_files:
            file_path = self.base_dir / py_file
            if file_path.exists():
                try:
                    if backup:
                        shutil.copy2(file_path, backup_dir / py_file)
                    
                    file_path.unlink()
                    print(f"🗑️  Removed: {py_file}")
                    total_removed += 1
                    
                except Exception as e:
                    print(f"❌ Error removing {py_file}: {e}")
        
        print(f"\n✅ Cleanup complete:")
        print(f"   Removed: {total_removed} items")
        if backup:
            print(f"   Backed up: {total_backed_up} items to {backup_dir.relative_to(self.base_dir)}")
        
        return total_removed

    def migrate_essential_files(self):
        """Migrate essential files from old structure to new"""
        print("\n" + "="*60)
        print("🚚 MIGRATING ESSENTIAL FILES")
        print("="*60)
        
        migration_map = {
            # From old to new location
            ("app/assets/chloris_logo-removebg.png", "app/assets/images/chloris_logo-removebg.png"),
            ("data/diseases/penyakit.json", "data/diseases/penyakit.json"),
            ("app/pages/scanner.py", "app/pages/scanner.py"),
            ("app/components/sidebar.py", "app/components/sidebar.py"),
            ("app/styles.py", "app/styles.py"),
            ("app/main.py", "app/main.py"),
            ("app/utils.py", "app/utils.py"),
            ("requirements.txt", "requirements.txt"),
            (".env", ".env"),
            (".gitignore", ".gitignore")
        }
        
        migrated = 0
        errors = 0
        
        for source_rel, dest_rel in migration_map:
            source_path = self.base_dir / source_rel
            dest_path = self.base_dir / dest_rel
            
            if source_path.exists():
                try:
                    # Ensure destination directory exists
                    dest_path.parent.mkdir(parents=True, exist_ok=True)
                    
                    # Copy file
                    shutil.copy2(source_path, dest_path)
                    print(f"📋 Migrated: {source_rel} → {dest_rel}")
                    migrated += 1
                    
                except Exception as e:
                    print(f"❌ Error migrating {source_rel}: {e}")
                    errors += 1
            else:
                print(f"⚠️  Source not found: {source_rel}")
        
        print(f"\n✅ Migration complete:")
        print(f"   Migrated: {migrated} files")
        if errors > 0:
            print(f"   Errors: {errors}")
        
        return migrated

    def create_template_files(self):
        """Create template content for new files"""
        print("\n" + "="*60)
        print("📝 CREATING TEMPLATE FILES")
        print("="*60)
        
        templates = {
            # Config file
            "app/config.py": '''# app/config.py
import os
from pathlib import Path

# Path configurations
BASE_DIR = Path(__file__).parent.parent if "app" in str(Path(__file__).parent) else Path(__file__).parent
APP_DIR = BASE_DIR / "app"
DATA_DIR = BASE_DIR / "data"
DISEASE_DB_PATH = DATA_DIR / "diseases" / "penyakit.json"
ASSETS_DIR = BASE_DIR / "assets"

# Model configurations
MODEL_CONFIG = {
    "name": "crop-disease-identification-dniia",
    "version": 2,
    "workspace": "xof",
    "type": "instance_segmentation",
    "confidence_threshold": 0.3,
    "processing_size": 640
}

# UI configurations
UI_CONFIG = {
    "primary_color": "#A8E890",
    "secondary_color": "#1A2F23",
    "danger_color": "#FF6B6B",
    "warning_color": "#FFC300",
    "glass_effect": True
}

# Session state defaults
SESSION_DEFAULTS = {
    'detection_confidence': 0.0,
    'detection_class': 'Pilih mode untuk memulai',
    'detection_severity': 'Low',
    'detection_solutions': ['Gunakan camera real-time atau upload gambar'],
    'camera_active': False,
    'confidence_threshold': 0.3,
    'overlap_threshold': 0.5,
    'inference_interval': 3,
    'debug_mode': False,
    'scanner_init': True
}

# Check and create directories
for directory in [DATA_DIR, ASSETS_DIR, DATA_DIR / "diseases"]:
    directory.mkdir(parents=True, exist_ok=True)
''',
            
            # Main file
            "app/main.py": '''# app/main.py
import streamlit as st
import sys
import os

# Add app directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from styles import load_css
from components.sidebar import create_sidebar

# Load CSS
load_css()

def main():
    """Main application entry point"""
    
    # Initialize session state
    from modules.scanner.validator import initialize_scanner_state
    initialize_scanner_state()
    
    # Get selected page from sidebar
    selected_page = create_sidebar()
    
    # Route to appropriate page
    if selected_page == "Scanner Tanaman":
        from pages.scanner import show_scanner_page
        show_scanner_page()
    
    elif selected_page == "Ensiklopedia":
        from pages.encyclopedia import show_encyclopedia_page
        show_encyclopedia_page()
    
    elif selected_page == "Laporan":
        from pages.reports import show_reports_page
        show_reports_page()
    
    elif selected_page == "Pengaturan":
        from pages.settings import show_settings_page
        show_settings_page()

if __name__ == "__main__":
    main()
''',
            
            # Disease mapper
            "app/modules/disease/mapper.py": '''# app/modules/disease/mapper.py
import re
import streamlit as st
from .database import load_disease_database

def normalize_class_name(class_name):
    """Normalize class name for matching"""
    if not class_name:
        return ""
    
    # Convert to lowercase and strip whitespace
    normalized = class_name.strip().lower()
    
    # Remove multiple spaces
    normalized = re.sub(r'\\s+', ' ', normalized)
    
    # Standardize spacing around hyphens
    normalized = re.sub(r'\\s*-\\s*', '-', normalized)
    
    return normalized

def map_to_disease_database(class_name, confidence):
    """Map detection result to disease database"""
    db = load_disease_database()
    
    if not class_name:
        return create_unknown_disease_info(confidence)
    
    # Normalize input class name
    class_normalized = normalize_class_name(class_name)
    
    # 1. Try exact match
    if class_normalized in db:
        info = db[class_normalized].copy()
        info['confidence'] = confidence
        return info
    
    # 2. Try partial match
    for db_key, db_info in db.items():
        db_key_normalized = normalize_class_name(db_key)
        
        if (class_normalized in db_key_normalized or 
            db_key_normalized in class_normalized):
            info = db_info.copy()
            info['confidence'] = confidence
            info['nama_id'] = f"{db_info['nama_id']} (Kemungkinan)"
            return info
    
    # 3. Fallback to unknown
    return create_unknown_disease_info(confidence, class_name)

def create_unknown_disease_info(confidence, class_name=None):
    """Create fallback disease info"""
    return {
        'confidence': confidence,
        'nama_id': f'{class_name.replace("-", " ").title() if class_name else "Penyakit Tidak Dikenal"}',
        'tingkat_bahaya': 'Medium',
        'solusi': [
            'Konsultasikan dengan ahli tanaman',
            'Ambil foto dari berbagai angle untuk analisis lebih lanjut',
            'Perhatikan gejala seperti perubahan warna, bercak, atau bentuk tidak normal'
        ]
    }
''',
            
            # Disease database
            "app/modules/disease/database.py": '''# app/modules/disease/database.py
import json
import streamlit as st
from app.config import DISEASE_DB_PATH

def load_disease_database():
    """Load disease database from JSON file"""
    try:
        if DISEASE_DB_PATH.exists():
            with open(DISEASE_DB_PATH, 'r', encoding='utf-8') as f:
                db = json.load(f)
            
            if st.session_state.get('debug_mode', False):
                st.sidebar.success(f"✅ Database loaded: {len(db)} diseases")
            
            return db
        else:
            st.error(f"❌ Database file not found at: {DISEASE_DB_PATH}")
            return get_fallback_database()
    except Exception as e:
        st.error(f"❌ Error loading database: {e}")
        return get_fallback_database()

def get_fallback_database():
    """Fallback database jika file tidak ditemukan"""
    return {
        "bell pepper leaf-healthy": {
            "nama_id": "Daun Bell Pepper Sehat",
            "tingkat_bahaya": "Low",
            "solusi": ["Pertahankan perawatan rutin", "Jaga kelembaban tanah optimal"]
        },
        "bell pepper leaf-unhealthy": {
            "nama_id": "Daun Bell Pepper Sakit",
            "tingkat_bahaya": "Medium",
            "solusi": ["Periksa gejala lebih detail", "Isolasi tanaman sementara"]
        }
    }
''',
            
            # Disease analyzer
            "app/modules/disease/analyzer.py": '''# app/modules/disease/analyzer.py
import streamlit as st
from .mapper import map_to_disease_database

def analyze_detection_result(prediction_data):
    """Analyze detection result and return comprehensive info"""
    if not prediction_data:
        return None
    
    # Extract class and confidence
    class_name = prediction_data.get('class', 'unknown')
    confidence = prediction_data.get('confidence', 0)
    
    # Map to disease database
    disease_info = map_to_disease_database(class_name, confidence)
    
    # Add additional analysis
    disease_info.update({
        'original_class': class_name,
        'model_version': 'crop-disease-identification-dniia/2'
    })
    
    return disease_info

def update_detection_state(detection_info):
    """Update session state with detection info"""
    if detection_info and isinstance(detection_info, dict):
        st.session_state.update({
            'detection_confidence': detection_info.get('confidence', 0.0),
            'detection_class': detection_info.get('nama_id', 'Unknown'),
            'detection_severity': detection_info.get('tingkat_bahaya', 'Medium'),
            'detection_solutions': detection_info.get('solusi', ['No solutions available']),
            'last_detection_time': st.session_state.get('last_detection_time', '')
        })
    else:
        st.session_state.update({
            'detection_confidence': 0.0,
            'detection_class': 'Tidak terdeteksi',
            'detection_severity': 'Low',
            'detection_solutions': ['Coba gambar berbeda', 'Ubah pengaturan confidence']
        })
''',
            
            # Scanner detector
            "app/modules/scanner/detector.py": '''# app/modules/scanner/detector.py
import os
import cv2
import tempfile
import streamlit as st
from roboflow import Roboflow
from app.config import MODEL_CONFIG

class RoboflowDetector:
    """Roboflow AI Detector"""
    
    def __init__(self):
        self.api_key = os.getenv("ROBOFLOW_API_KEY")
        self.model = None
        self.initialized = False
        
    def initialize(self):
        """Initialize Roboflow model"""
        if not self.api_key or self.api_key == "your_actual_api_key_here":
            st.error("❌ API Key tidak valid")
            return False
        
        try:
            rf = Roboflow(api_key=self.api_key)
            project = rf.workspace(MODEL_CONFIG["workspace"]).project(MODEL_CONFIG["name"])
            self.model = project.version(MODEL_CONFIG["version"]).model
            self.initialized = True
            return True
        except Exception as e:
            st.error(f"❌ Model initialization failed: {e}")
            return False
    
    def predict(self, image, confidence_threshold=0.3):
        """Run prediction on image"""
        if not self.initialized and not self.initialize():
            return None
        
        try:
            # Save image to temp file
            with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as tmp_file:
                # Resize image to model expected size
                resized = cv2.resize(image, (640, 640))
                cv2.imwrite(tmp_file.name, resized)
                
                # Run prediction
                results = self.model.predict(
                    tmp_file.name,
                    confidence=int(confidence_threshold * 100)
                ).json()
                
                # Cleanup
                os.unlink(tmp_file.name)
                
                return results
                
        except Exception as e:
            st.error(f"❌ Prediction failed: {e}")
            return None
''',
            
            # UI Cards
            "app/components/ui_cards.py": '''# app/components/ui_cards.py
import streamlit as st

def glass_card(content_html, **kwargs):
    """Create glass card"""
    return f"""
    <div class="glass-card" {' '.join([f'{k}="{v}"' for k, v in kwargs.items()])}>
        {content_html}
    </div>
    """

def metric_card(value, label, icon="", color="#FFB7B2"):
    """Create metric card"""
    return f"""
    <div style="text-align: center; padding: 15px; border-radius: 15px; 
                background: linear-gradient(145deg, rgba(255, 255, 255, 0.05), rgba(255, 255, 255, 0.02)); 
                border: 1px solid rgba(255, 182, 193, 0.2); margin-bottom: 10px;">
        {f'<div style="font-size: 24px; color: {color};">{icon}</div>' if icon else ''}
        <div style="font-size: 26px; font-weight: bold; color: {color};">{value}</div>
        <div style="font-size: 12px; color: #a3b1a8;">{label}</div>
    </div>
    """

def disease_result_card(disease_info):
    """Create disease result card"""
    severity_color = {
        "low": "#4CAF50",
        "medium": "#FF9800",
        "high": "#F44336"
    }.get(disease_info['tingkat_bahaya'].lower(), "#FF9800")
    
    confidence = disease_info.get('confidence', 0)
    
    html = f"""
    <div class="glass-card">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px;">
            <h3 style="color: #A8E890; margin: 0;">{disease_info['nama_id']}</h3>
            <span style="background: {severity_color}20; color: {severity_color}; 
                        padding: 5px 15px; border-radius: 20px; font-size: 12px; 
                        border: 1px solid {severity_color}50; font-weight: bold;">
                {disease_info['tingkat_bahaya'].upper()}
            </span>
        </div>
        
        <div style="margin-bottom: 15px;">
            <p style="color: #d1e7dd; margin-bottom: 5px;">Confidence: <strong>{confidence:.1%}</strong></p>
            <div style="background: rgba(168, 232, 144, 0.1); height: 8px; border-radius: 4px; overflow: hidden;">
                <div style="width: {confidence*100}%; height: 100%; background: #A8E890;"></div>
            </div>
        </div>
        
        <div>
            <p style="color: #d1e7dd; font-weight: 600; margin-bottom: 10px;">💡 Treatment Recommendations:</p>
            <ul style="color: #a3b1a8; margin-left: 20px; margin-bottom: 0;">
    """
    
    for solution in disease_info.get('solusi', []):
        html += f"<li style='margin-bottom: 5px;'>{solution}</li>"
    
    html += "</ul></div></div>"
    return html
''',
            
            # UI Widgets
            "app/components/ui_widgets.py": '''# app/components/ui_widgets.py
import streamlit as st
import uuid

def unique_key(widget_name):
    """Generate unique key for widgets"""
    return f"{widget_name}_{str(uuid.uuid4())[:8]}"

def create_slider(label, min_val, max_val, default_val, step, key_suffix, help_text=""):
    """Create slider with unique key"""
    key = unique_key(f"slider_{key_suffix}")
    return st.slider(
        label, min_val, max_val, default_val, step,
        help=help_text, key=key
    )

def create_toggle(label, default, key_suffix):
    """Create toggle with unique key"""
    key = unique_key(f"toggle_{key_suffix}")
    return st.toggle(label, value=default, key=key)
''',
            
            # Requirements template
            "requirements.txt": '''streamlit>=1.28.0
opencv-python>=4.8.0
numpy>=1.24.0
roboflow>=1.1.0
python-dotenv>=1.0.0
pillow>=10.0.0
pandas>=2.0.0
plotly>=5.17.0
streamlit-option-menu>=0.3.0
'''
        }
        
        created = 0
        for file_path, content in templates.items():
            full_path = self.base_dir / file_path
            try:
                full_path.parent.mkdir(parents=True, exist_ok=True)
                
                # Only write if file doesn't exist or is empty
                if not full_path.exists() or full_path.stat().st_size == 0:
                    full_path.write_text(content, encoding='utf-8')
                    print(f"📝 Created template: {file_path}")
                    created += 1
            except Exception as e:
                print(f"❌ Error creating {file_path}: {e}")
        
        print(f"\n✅ Created {created} template files")
        return created

    def run_restructure(self, backup=True, migrate=True):
        """Run complete restructuring process"""
        print("\n" + "="*60)
        print("🚀 STARTING PROJECT RESTRUCTURING")
        print("="*60)
        
        try:
            # 1. Backup and cleanup old structure
            removed = self.cleanup_old_structure(backup=backup)
            
            # 2. Create new structure
            created = self.create_directory_structure()
            
            # 3. Migrate essential files
            migrated = 0
            if migrate:
                migrated = self.migrate_essential_files()
            
            # 4. Create template files
            templates = self.create_template_files()
            
            print("\n" + "="*60)
            print("🎉 RESTRUCTURING COMPLETE!")
            print("="*60)
            print(f"""
📊 Summary:
├── 📁 Directories/Files created: {created}
├── 🗑️  Old items removed: {removed}
├── 📋 Files migrated: {migrated}
├── 📝 Templates created: {templates}
└── 📍 Backup created: {'Yes' if backup else 'No'}

🚀 Next steps:
1. Run the application: streamlit run app/main.py
2. Check if all essential files are in place
3. Verify database path: data/diseases/penyakit.json
4. Update .env file with your API key if needed

⚠️  Note: Old structure has been backed up to 'backup_old' directory
            """)
            
            return True
            
        except Exception as e:
            print(f"\n❌ Restructuring failed: {e}")
            import traceback
            traceback.print_exc()
            return False


def main():
    """Main function"""
    print("🌿 CHLORIS AI PROJECT RESTRUCTURER")
    print("This script will:")
    print("1. 🗑️  Clean up old directories and files")
    print("2. 🏗️  Create new organized directory structure")
    print("3. 📋 Migrate essential files")
    print("4. 📝 Create template files for new structure")
    
    # Ask for confirmation
    response = input("\n⚠️  WARNING: This will modify your project structure. Continue? (yes/no): ")
    
    if response.lower() not in ['yes', 'y']:
        print("❌ Operation cancelled.")
        return
    
    # Create restructurer
    restructurer = ProjectRestructurer()
    
    # Run restructuring
    success = restructurer.run_restructure(
        backup=True,    # Create backup of old files
        migrate=True    # Migrate essential files
    )
    
    if success:
        print("\n✅ Restructuring completed successfully!")
    else:
        print("\n❌ Restructuring failed. Check errors above.")


if __name__ == "__main__":
    main()