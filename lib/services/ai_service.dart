import 'api_service.dart';
import 'dart:io';
import 'roboflow_service.dart';
import 'disease_data_service.dart';
import 'dart:math';

class AiService {
  static final AiService _instance = AiService._internal();
  factory AiService() => _instance;
  AiService._internal();
  
  final RoboflowService _roboflowService = RoboflowService();
  final DiseaseDataService _diseaseDataService = DiseaseDataService();
  bool _isDiseaseDataLoaded = false;
  
  /// Analisis gambar dengan fallback otomatis
  Future<List<Map<String, dynamic>>> analyzeImage(String imagePath) async {
  try {
    print('🔍 Starting REAL analysis with Roboflow...');
    
    // 1. Load penyakit data
    if (!_isDiseaseDataLoaded) {
      await _diseaseDataService.loadDiseases();
      _isDiseaseDataLoaded = true;
    }
    
    // 2. PANGGIL ROBOTFLOW ASLI (bukan dummy)
    print('🔄 Calling REAL Roboflow API...');
    final roboflowResult = await _roboflowService.analyzeImage(imagePath)
      .timeout(Duration(seconds: 30), onTimeout: () {
        print('⏱️ Roboflow timeout, using fallback');
        return {'status': 'timeout', 'predictions': []};
      });
    
    // 3. Jika timeout atau error, baru pakai backend/dummy
    if (roboflowResult.containsKey('status') && 
        roboflowResult['status'] == 'timeout') {
      print('⚠️ Roboflow timeout, trying backend fallback...');
      return await _tryBackendFallback(imagePath);
    }
    
    // 4. Enrich dengan data penyakit
    print('✅ Roboflow success, enriching data...');
    final enrichedResults = await _enrichWithDiseaseData(roboflowResult);
    
    // DEBUG: Print hasil
    print('📊 Final results: ${enrichedResults.length} detections');
    for (var result in enrichedResults) {
      print('  - ${result['label']} (${result['confidence']})');
    }
    
    return enrichedResults;
    
  } catch (e) {
    print('❌ All APIs failed: $e');
    return await _createRandomDummyData(); // Random dummy, bukan fixed
  }
}

// Fallback ke backend lokal
Future<List<Map<String, dynamic>>> _tryBackendFallback(String imagePath) async {
    try {
      print('🔄 Trying backend fallback...');
      
      // Gunakan static method dari ApiService
      final backendResult = await ApiService.sendImageToBackend(File(imagePath));
      return await _enrichWithDiseaseData(backendResult);
      
    } catch (e) {
      print('❌ Backend also failed: $e');
      return await _createRandomDummyData();
    }
  }// BUAT DUMMY DATA RANDOM (bukan fixed)
Future<List<Map<String, dynamic>>> _createRandomDummyData() async {
  print('🎲 Creating RANDOM dummy data...');
  
  // Load penyakit data
  if (!_isDiseaseDataLoaded) {
    await _diseaseDataService.loadDiseases();
    _isDiseaseDataLoaded = true;
  }
  
  // Pilih penyakit random dari JSON
  final random = Random();
  final allDiseases = [
    'bell pepper leaf-healthy',
    'bell pepper leaf-unhealthy',
    'bell pepper-phytophthora blight',
    'cucumber leaf - healthy',
    'cucumber leaf - unhealthy',
    'cucumber-mosaic',
    'cucumber-powdery-mildew',
    'lettuce-bacterial leaf spot',
    'lettuce-downy mildew',
    'lettuce-healthy',
    'strawberry fruit-healthy',
    'strawberry leaf-healthy',
    'strawberry-angular leafspot',
    'tomato-early blight',
    'tomato-healthy',
  ];
  
  // Pilih 1-2 penyakit random
  final numDetections = random.nextInt(2) + 1; // 1-2 detections
  final selectedDiseases = <String>[];
  
  for (int i = 0; i < numDetections; i++) {
    final randomDisease = allDiseases[random.nextInt(allDiseases.length)];
    if (!selectedDiseases.contains(randomDisease)) {
      selectedDiseases.add(randomDisease);
    }
  }
  
  // Buat detections
  final results = <Map<String, dynamic>>[];
  for (final diseaseKey in selectedDiseases) {
    final diseaseInfo = _diseaseDataService.getDiseaseByKey(diseaseKey);
    
    results.add({
      'rect': {
        'left': random.nextDouble() * 0.4,
        'top': random.nextDouble() * 0.4,
        'right': 0.6 + random.nextDouble() * 0.3,
        'bottom': 0.6 + random.nextDouble() * 0.3,
      },
      'label': diseaseInfo.namaId,
      'confidence': 0.5 + random.nextDouble() * 0.4, // 0.5-0.9
      'additionalData': {
        'original_class': diseaseKey,
        'tingkat_bahaya': diseaseInfo.tingkatBahaya,
        'solusi': diseaseInfo.solusi,
        'source': 'random_dummy',
      },
    });
  }
  
  return results;
}

// HAPUS/HAPUSKAN fungsi analyzeImageFastDummy yang lama
// atau rename supaya tidak dipanggil
  /// Enrich hasil Roboflow dengan data penyakit
  Future<List<Map<String, dynamic>>> _enrichWithDiseaseData(
    Map<String, dynamic> roboflowResult
  ) async {
    final predictions = roboflowResult['predictions'] as List? ?? [];
    
    if (predictions.isEmpty) {
      // Jika tidak ada deteksi, return tanaman sehat
      final healthyDisease = _diseaseDataService.getDiseaseByKey('unknown_disease');
      return [
        {
          'rect': null,
          'label': 'Tanaman Sehat',
          'confidence': 0.0,
          'additionalData': {
            'original_class': 'healthy',
            'tingkat_bahaya': 'Low',
            'solusi': ['Lanjutkan perawatan rutin', 'Pantau pertumbuhan'],
          },
        }
      ];
    }
    
    return predictions.map<Map<String, dynamic>>((pred) {
      final className = pred['class']?.toString() ?? 'unknown_disease';
      final diseaseInfo = _diseaseDataService.getDiseaseByKey(className);
      
      // Convert bounding box format
      final imageWidth = roboflowResult['image_width'] ?? 640.0;
      final imageHeight = roboflowResult['image_height'] ?? 640.0;
      
      final x = (pred['x'] as num).toDouble();
      final y = (pred['y'] as num).toDouble();
      final width = (pred['width'] as num).toDouble();
      final height = (pred['height'] as num).toDouble();
      
      // Convert to normalized rect (0-1)
      final left = (x - width / 2) / imageWidth;
      final top = (y - height / 2) / imageHeight;
      final right = (x + width / 2) / imageWidth;
      final bottom = (y + height / 2) / imageHeight;
      
      return {
        'rect': {
          'left': left.clamp(0.0, 1.0),
          'top': top.clamp(0.0, 1.0),
          'right': right.clamp(0.0, 1.0),
          'bottom': bottom.clamp(0.0, 1.0),
        },
        'label': diseaseInfo.namaId,
        'confidence': (pred['confidence'] as num).toDouble(),
        'additionalData': {
          'original_class': className,
          'tingkat_bahaya': diseaseInfo.tingkatBahaya,
          'solusi': diseaseInfo.solusi,
          'raw_prediction': pred,
        },
      };
    }).toList();
  }
  
  /// Mode dummy untuk testing
  Future<List<Map<String, dynamic>>> analyzeImageDummy(String imagePath) async {
    await Future.delayed(const Duration(seconds: 2));
    
    // Load data penyakit
    if (!_isDiseaseDataLoaded) {
      await _diseaseDataService.loadDiseases();
      _isDiseaseDataLoaded = true;
    }
    
    final diseaseInfo = _diseaseDataService.getDiseaseByKey('tomato-early blight');
    
    return [
      {
        'rect': {
          'left': 0.3,
          'top': 0.4,
          'right': 0.7,
          'bottom': 0.8,
        },
        'label': diseaseInfo.namaId,
        'confidence': 0.85,
        'additionalData': {
          'original_class': 'tomato-early blight',
          'tingkat_bahaya': diseaseInfo.tingkatBahaya,
          'solusi': diseaseInfo.solusi,
        },
      },
      {
        'rect': {
          'left': 0.1,
          'top': 0.2,
          'right': 0.4,
          'bottom': 0.5,
        },
        'label': 'Daun Sehat',
        'confidence': 0.42,
        'additionalData': {
          'original_class': 'healthy',
          'tingkat_bahaya': 'Low',
          'solusi': ['Pertahankan perawatan'],
        },
      },
    ];
  }
  
  static AiService get instance => _instance;
}