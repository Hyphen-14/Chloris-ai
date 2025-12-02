import 'dart:io';
import 'dart:convert';
import 'package:http/http.dart' as http;

class ApiService {
  // Ganti dengan IP backend lokal Anda
  static const String baseUrl = "http://10.237.126.133:8000"; // IP Anda
  
  /// Kirim gambar ke backend lokal (fallback)
  static Future<Map<String, dynamic>> sendImageToBackend(File image) async {
    try {
      print('🔄 Mengirim ke backend lokal: $baseUrl');
      
      final uri = Uri.parse("$baseUrl/predict-image");
      final request = http.MultipartRequest("POST", uri);
      
      request.files.add(
        await http.MultipartFile.fromPath("file", image.path),
      );
      
      final response = await request.send();
      final respStr = await response.stream.bytesToString();
      
      print('📡 Backend response: ${response.statusCode}');
      
      if (response.statusCode == 200) {
        final Map<String, dynamic> data = jsonDecode(respStr);
        return _formatBackendResponse(data);
      } else {
        throw Exception('Backend error ${response.statusCode}: $respStr');
      }
    } catch (e) {
      print('❌ Backend service error: $e');
      rethrow;
    }
  }
  
  /// Format response backend ke format standar
  static Map<String, dynamic> _formatBackendResponse(Map<String, dynamic> data) {
    final detections = data['detections'] as List? ?? [];
    
    final predictions = detections.map((d) {
      final box = d['box'] ?? {};
      return {
        'class': d['label'] ?? 'unknown',
        'confidence': (d['score'] ?? 0).toDouble(),
        'x': ((box['x1'] ?? 0) + (box['x2'] ?? 0)) / 2,
        'y': ((box['y1'] ?? 0) + (box['y2'] ?? 0)) / 2,
        'width': ((box['x2'] ?? 0) - (box['x1'] ?? 0)).abs(),
        'height': ((box['y2'] ?? 0) - (box['y1'] ?? 0)).abs(),
      };
    }).toList();
    
    return {
      'status': predictions.isNotEmpty ? 'disease_detected' : 'healthy',
      'predictions': predictions,
      'image_width': 640.0,
      'image_height': 640.0,
      'time': 0.5,
      'source': 'local_backend', // Tandai sebagai dari backend lokal
    };
  }
  
  /// Test koneksi ke backend
  static Future<bool> testConnection() async {
    try {
      final uri = Uri.parse("$baseUrl/");
      final response = await http.get(uri).timeout(Duration(seconds: 5));
      return response.statusCode == 200;
    } catch (e) {
      print('⚠️ Backend connection test failed: $e');
      return false;
    }
  }
}