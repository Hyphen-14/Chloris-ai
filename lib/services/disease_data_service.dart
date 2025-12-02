import 'dart:convert';
import 'package:flutter/services.dart';

class DiseaseInfo {
  final String id;
  final String namaId;
  final String tingkatBahaya;
  final List<String> solusi;
  
  DiseaseInfo({
    required this.id,
    required this.namaId,
    required this.tingkatBahaya,
    required this.solusi,
  });
  
  factory DiseaseInfo.fromJson(String id, Map<String, dynamic> json) {
    return DiseaseInfo(
      id: id,
      namaId: json['nama_id'] ?? 'Tidak Dikenal',
      tingkatBahaya: json['tingkat_bahaya'] ?? 'Medium',
      solusi: List<String>.from(json['solusi'] ?? []),
    );
  }
}

class DiseaseDataService {
  Map<String, DiseaseInfo> _diseases = {};
  
  Future<void> loadDiseases() async {
    try {
      final jsonString = await rootBundle.loadString('lib/data/penyakit.json');
      final Map<String, dynamic> jsonData = json.decode(jsonString);
      
      _diseases = {};
      jsonData.forEach((key, value) {
        _diseases[key] = DiseaseInfo.fromJson(key, value);
      });
      
      print('✅ Loaded ${_diseases.length} diseases');
      
      // Debug: print available keys
      print('Available disease keys:');
      _diseases.keys.take(5).forEach(print);
      
    } catch (e) {
      print('❌ Error loading penyakit.json: $e');
      
      // Buat data default termasuk 'healthy'
      _diseases = {
        'healthy': DiseaseInfo(
          id: 'healthy',
          namaId: 'Tanaman Sehat',
          tingkatBahaya: 'Low',
          solusi: ['Pertahankan perawatan rutin'],
        ),
        'unknown_disease': DiseaseInfo(
          id: 'unknown_disease',
          namaId: 'Penyakit Tidak Dikenal',
          tingkatBahaya: 'Medium',
          solusi: ['Konsultasikan dengan ahli'],
        ),
      };
    }
  }
  
  DiseaseInfo getDiseaseByKey(String key) {
    // Normalisasi key
    String normalizedKey = key.toLowerCase().trim();
    
    // 1. Coba exact match
    if (_diseases.containsKey(normalizedKey)) {
      return _diseases[normalizedKey]!;
    }
    
    // 2. Cari 'healthy' dalam berbagai variasi
    if (normalizedKey.contains('healthy')) {
      // Cek apakah ada key yang mengandung 'healthy'
      for (var diseaseKey in _diseases.keys) {
        if (diseaseKey.toLowerCase().contains('healthy')) {
          return _diseases[diseaseKey]!;
        }
      }
      // Jika tidak ada, buat default healthy
      return DiseaseInfo(
        id: 'healthy',
        namaId: 'Tanaman Sehat',
        tingkatBahaya: 'Low',
        solusi: ['Pertahankan perawatan rutin'],
      );
    }
    
    // 3. Coba partial match
    for (var diseaseKey in _diseases.keys) {
      if (normalizedKey.contains(diseaseKey.toLowerCase()) || 
          diseaseKey.toLowerCase().contains(normalizedKey)) {
        return _diseases[diseaseKey]!;
      }
    }
    
    // 4. Fallback ke unknown
    return _diseases['unknown_disease'] ?? DiseaseInfo(
      id: 'unknown',
      namaId: 'Penyakit Tidak Dikenal',
      tingkatBahaya: 'Medium',
      solusi: ['Konsultasi dengan ahli tanaman'],
    );
  }
}