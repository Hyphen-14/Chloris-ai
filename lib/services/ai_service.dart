import 'dart:io';
import 'dart:ui';
// import 'package:tflite_flutter/tflite_flutter.dart' as tfl; // Nanti dinyalakan saat sudah ada model
import '../models/detection.dart';

class AiService {
  // Singleton pattern
  AiService._privateConstructor();
  static final AiService instance = AiService._privateConstructor();

  // Future<void> loadModel() async { ... } // Nanti kita isi

  /// Fungsi ini mensimulasikan proses AI
  /// Menerima [imagePath], mengembalikan list [Detection]
  Future<List<Detection>> analyzeImage(String imagePath) async {
    
    // 1. Simulasi Loading (pura-pura mikir)
    await Future.delayed(const Duration(seconds: 2));

    // 2. Kembalikan Hasil Dummy (Hardcoded)
    // Nanti di sini kita ganti dengan logika 'image' package + interpreter.run
    return [
      Detection(
        // Kotak merah imajiner di tengah gambar
        rect: const Rect.fromLTWH(0.2, 0.3, 0.6, 0.4), 
        label: "Bercak Daun (Dummy)",
        score: 0.92,
      ),
    ];
  }
}