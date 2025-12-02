import shutil
import os

def migrate_files():
    # Mapping file lama ke file baru
    files_to_migrate = {
        "App/app.py": "app/main.py",
        "App/styles.py": "app/styles.py",
        # tambahkan file lainnya
    }
    
    # Langkah 1: Rename folder App ke temp folder
    if os.path.exists("App"):
        if os.path.exists("app_temp"):
            shutil.rmtree("app_temp")
        shutil.move("App", "app_temp")
        print("Renamed: App → app_temp")
    
    # Langkah 2: Rename temp folder ke app (lowercase)
    if os.path.exists("app_temp"):
        if os.path.exists("app"):
            shutil.rmtree("app")
        shutil.move("app_temp", "app")
        print("Renamed: app_temp → app")
    
    # Langkah 3: Rename file jika diperlukan
    if os.path.exists("app/app.py"):
        shutil.move("app/app.py", "app/main.py")
        print("Renamed: app/app.py → app/main.py")
    
    print("Migration completed!")

if __name__ == "__main__":
    migrate_files()