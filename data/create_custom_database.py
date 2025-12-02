# create_custom_database.py
import json
from pathlib import Path

def create_custom_disease_database():
    """Create disease database berdasarkan 29 classes Anda"""
    
    disease_db = {
        # BELL PEPPER CLASSES
        "bell pepper leaf-healthy": {
            "nama_id": "Daun Bell Pepper Sehat",
            "tingkat_bahaya": "Low",
            "solusi": [
                "Pertahankan perawatan rutin",
                "Jaga kelembaban tanah optimal",
                "Berikan pupuk seimbang"
            ]
        },
        "bell pepper leaf-unhealthy": {
            "nama_id": "Daun Bell Pepper Sakit",
            "tingkat_bahaya": "Medium", 
            "solusi": [
                "Periksa gejala lebih detail",
                "Isolasi tanaman sementara",
                "Kurangi penyiraman berlebihan"
            ]
        },
        "bell pepper-phytophthora blight": {
            "nama_id": "Phytophthora Blight - Bell Pepper",
            "tingkat_bahaya": "High",
            "solusi": [
                "Hentikan penyiraman berlebihan",
                "Gunakan fungisida sistemik",
                "Buang tanaman yang terinfeksi parah",
                "Rotasi tanaman dengan jenis berbeda"
            ]
        },
        
        # CUCUMBER CLASSES
        "cucumber leaf - healthy": {
            "nama_id": "Daun Mentimun Sehat", 
            "tingkat_bahaya": "Low",
            "solusi": [
                "Lanjutkan perawatan rutin",
                "Jaga suhu 18-24°C",
                "Berikan air secara teratur"
            ]
        },
        "cucumber leaf - unhealthy": {
            "nama_id": "Daun Mentimun Sakit",
            "tingkat_bahaya": "Medium",
            "solusi": [
                "Periksa hama dan penyakit",
                "Tingkatkan sirkulasi udara",
                "Gunakan pestisida organik"
            ]
        },
        "cucumber-mosaic": {
            "nama_id": "Mosaic Virus - Mentimun",
            "tingkat_bahaya": "High",
            "solusi": [
                "Buang tanaman terinfeksi",
                "Kendalikan serangga vektor",
                "Gunakan varietas tahan virus",
                "Sterilkan alat kebun"
            ]
        },
        "cucumber-powdery-mildew": {
            "nama_id": "Powdery Mildew - Mentimun", 
            "tingkat_bahaya": "Medium",
            "solusi": [
                "Semprot baking soda solution",
                "Tingkatkan sirkulasi udara",
                "Gunakan fungisida sulfur",
                "Hindari penyiraman daun"
            ]
        },
        
        # LETTUCE CLASSES
        "lettuce-bacterial leaf spot": {
            "nama_id": "Bercak Bakteri - Selada",
            "tingkat_bahaya": "Medium",
            "solusi": [
                "Hindari penyiraman dari atas",
                "Gunakan bakterisida tembaga",
                "Buang daun terinfeksi",
                "Tingkatkan jarak tanam"
            ]
        },
        "lettuce-downy mildew": {
            "nama_id": "Downy Mildew - Selada",
            "tingkat_bahaya": "High",
            "solusi": [
                "Kurangi kelembaban",
                "Gunakan fungisida sistemik", 
                "Rotasi tanaman",
                "Buang tanaman terinfeksi"
            ]
        },
        "lettuce-healthy": {
            "nama_id": "Selada Sehat",
            "tingkat_bahaya": "Low",
            "solusi": [
                "Pertahankan perawatan",
                "Jaga tanah tetap lembab",
                "Berikan pupuk nitrogen"
            ]
        },
        
        # STRAWBERRY CLASSES  
        "strawberry fruit-healthy": {
            "nama_id": "Buah Stroberi Sehat",
            "tingkat_bahaya": "Low",
            "solusi": [
                "Lanjutkan perawatan",
                "Jaga pH tanah 5.5-6.5",
                "Berikan pupuk kaya kalium"
            ]
        },
        "strawberry leaf-healthy": {
            "nama_id": "Daun Stroberi Sehat",
            "tingkat_bahaya": "Low", 
            "solusi": [
                "Pertahankan perawatan rutin",
                "Jaga kebersihan sekitar tanaman",
                "Pantau pertumbuhan rutin"
            ]
        },
        "strawberry-angular leafspot": {
            "nama_id": "Bercak Sudut - Stroberi",
            "tingkat_bahaya": "Medium",
            "solusi": [
                "Gunakan fungisida tembaga",
                "Hindari penyiraman daun",
                "Buang daun terinfeksi",
                "Tingkatkan sirkulasi udara"
            ]
        },
        
        # TOMATO CLASSES
        "tomato-early blight": {
            "nama_id": "Hawar Dini - Tomat",
            "tingkat_bahaya": "High",
            "solusi": [
                "Gunakan fungisida chlorothalonil",
                "Buang daun bawah terinfeksi",
                "Rotasi tanaman 3-4 tahun",
                "Hindari penyiraman dari atas"
            ]
        },
        "tomato-healthy": {
            "nama_id": "Tomat Sehat",
            "tingkat_bahaya": "Low",
            "solusi": [
                "Lanjutkan perawatan optimal",
                "Berikan pupuk seimbang",
                "Jaga kelembaban konsisten"
            ]
        },
        
        # FALLBACK FOR OTHER CLASSES
        "unknown_disease": {
            "nama_id": "Penyakit Tidak Dikenal",
            "tingkat_bahaya": "Medium", 
            "solusi": [
                "Konsultasikan dengan ahli tanaman",
                "Foto gejala dari berbagai angle",
                "Isolasi tanaman sementara",
                "Pantau perkembangan gejala"
            ]
        }
    }
    
    # Save database
    Path("data/diseases").mkdir(exist_ok=True)
    with open("data/diseases/penyakit.json", "w", encoding="utf-8") as f:
        json.dump(disease_db, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Custom disease database created with {len(disease_db)} entries!")
    return disease_db

if __name__ == "__main__":
    create_custom_disease_database()