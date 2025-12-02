import 'dart:convert';
import 'dart:io';
import 'package:http/http.dart' as http;
import 'api_service.dart'; // Import api_service sebagai fallback

class RoboflowService {
  static const String _apiKey = 'IbNv43xxhSDW6aWYIsqG';
  static const String _modelId = 'crop-disease-identification-dniia/2';
  static const String _baseUrl = 'https://serverless.roboflow.com';
  
  /// Analisis dengan Roboflow, fallback ke backend lokal jika gagal
  Future<Map<String, dynamic>> analyzeImageWithFallback(String imagePath) async {
    try {
      print('🚀 Mencoba Roboflow API...');
      
      // 1. Coba Roboflow dulu
      final roboflowResult = await _callRoboflowAPI(imagePath);
      print('✅ Roboflow sukses');
      return roboflowResult;
      
    } catch (roboflowError) {
      print('⚠️ Roboflow gagal: $roboflowError');
      
      try {
        print('🔄 Fallback ke backend lokal...');
        
        // 2. Coba backend lokal
        final backendResult = await ApiService.sendImageToBackend(File(imagePath));
        print('✅ Backend lokal sukses');
        
        // Tambahkan flag untuk identifikasi sumber
        return {
          ...backendResult,
          'source': 'fallback_backend',
          'roboflow_error': roboflowError.toString(),
        };
        
      } catch (backendError) {
        print('❌ Semua API gagal');
        
        // 3. Return error dengan data kosong
        return {
          'status': 'error',
          'predictions': [],
          'image_width': 640.0,
          'image_height': 640.0,
          'time': 0,
          'source': 'error',
          'error': 'Roboflow: $roboflowError\nBackend: $backendError',
        };
      }
    }
  }
  
  /// Panggil Roboflow API langsung (tanpa fallback)
 Future<Map<String, dynamic>> analyzeImage(String imagePath) async {
  try {
    print('🚀 Mengirim ke Roboflow...');
    
    final imageFile = File(imagePath);
    final imageBytes = await imageFile.readAsBytes();
    
    // COMPRESI GAMBAR: Kurangi ukuran
    final compressedBytes = await _compressImageForUpload(imageBytes);
    final base64Image = base64Encode(compressedBytes);
    
    final endpoint = '$_baseUrl/$_modelId?api_key=$_apiKey';
    
    // TIMEOUT LEBIH PENDEK: 20 detik saja
    final response = await http.post(
      Uri.parse(endpoint),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({
        'image': {'type': 'base64', 'value': base64Image}
      }),
    ).timeout(Duration(seconds: 20)); // ↓ dari 45 ke 20 detik
    
    print('✅ Roboflow response: ${response.statusCode}');
    
    if (response.statusCode == 200) {
      return jsonDecode(response.body);
    } else {
      throw Exception('Roboflow error ${response.statusCode}');
    }
  } catch (e) {
    print('❌ Roboflow API error: $e');
    rethrow;
  }
}

// FUNGSI KOMPRESI GAMBAR
Future<List<int>> _compressImageForUpload(List<int> imageBytes) async {
  try {
    // Jika gambar kecil (<500KB), langsung return
    if (imageBytes.length < 500 * 1024) {
      return imageBytes;
    }
    
    print('📏 Compressing image: ${imageBytes.length ~/ 1024}KB');
    
    // Pakai package image jika ada
    // import 'package:image/image.dart' as img;
    // final image = img.decodeImage(imageBytes);
    // if (image != null) {
    //   final resized = img.copyResize(image, width: 800);
    //   return img.encodeJpg(resized, quality: 80);
    // }
    
    // Fallback: return asli (tapi kasih warning)
    print('⚠️ Image compression package not available');
    return imageBytes;
  } catch (e) {
    print('⚠️ Compression failed: $e');
    return imageBytes;
    }
  }
  
  /// Implementasi panggilan ke Roboflow
  Future<Map<String, dynamic>> _callRoboflowAPI(String imagePath) async {
    final imageFile = File(imagePath);
    final imageBytes = await imageFile.readAsBytes();
    final base64Image = base64Encode(imageBytes);
    
    final endpoint = '$_baseUrl/$_modelId?api_key=$_apiKey';
    final uri = Uri.parse(endpoint);
    
    final response = await http.post(
      uri,
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({
        'image': {'type': 'base64', 'value': base64Image}
      }),
    ).timeout(Duration(seconds: 45));
    
    if (response.statusCode == 200) {
      final data = jsonDecode(response.body);
      return {
        ...data,
        'source': 'roboflow', // Tandai sebagai dari Roboflow
      };
    } else {
      throw Exception('Roboflow API Error ${response.statusCode}');
    }
  }
}