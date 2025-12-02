import 'dart:io';
import 'package:flutter/material.dart';
import 'package:camera/camera.dart';
import '../services/camera_service.dart';
import '../services/ai_service.dart';
import '../models/detection.dart';
import 'result_page.dart';

class ScanPage extends StatefulWidget {
  const ScanPage({super.key});

  @override
  State<ScanPage> createState() => _ScanPageState();
}

class _ScanPageState extends State<ScanPage> with WidgetsBindingObserver {
  late CameraService _cameraService;
  bool _isInitialized = false;
  bool _isAnalyzing = false;

  @override
  void initState() {
    super.initState();
    // Menambahkan observer untuk mendeteksi jika aplikasi di-minimize/resume
    WidgetsBinding.instance.addObserver(this);
    _cameraService = CameraService();
    _initCamera();
  }

  Future<void> _initCamera() async {
    await _cameraService.initialize();
    if (mounted) {
      setState(() {
        _isInitialized = true;
      });
    }
  }

  @override
  void dispose() {
    WidgetsBinding.instance.removeObserver(this);
    _cameraService.dispose();
    super.dispose();
  }

  // Menangani lifecycle app (agar kamera tidak error saat aplikasi diminimize)
  @override
  void didChangeAppLifecycleState(AppLifecycleState state) {
    final CameraController? cameraController = _cameraService.controller;

    if (cameraController == null || !cameraController.value.isInitialized) {
      return;
    }

    if (state == AppLifecycleState.inactive) {
      cameraController.dispose();
    } else if (state == AppLifecycleState.resumed) {
      _initCamera();
    }
  }

 Future<void> _onCapturePressed() async {
  if (_isAnalyzing) return;
  
  setState(() => _isAnalyzing = true);
  
  final XFile? file = await _cameraService.takePicture();
  
  if (file != null) {
    print('📸 Picture taken: ${file.path}');
    
    try {
      final aiService = AiService.instance;
      print('🔄 Starting AI analysis...');
      
      final startTime = DateTime.now();
      final analysisResults = await aiService.analyzeImage(file.path);
      final endTime = DateTime.now();
      
      final duration = endTime.difference(startTime);
      print('⏱️ Analysis took: ${duration.inSeconds} seconds');
      
      final detections = analysisResults.map((map) => Detection.fromMap(map)).toList();
      
      print('🎯 Results: ${detections.length} detections');
      for (var detection in detections) {
        print('   - ${detection.label} (${detection.confidence})');
      }
      
      if (mounted) {
        Navigator.push(
          context,
          MaterialPageRoute(
            builder: (_) => ResultPage(
              imageFilePath: file.path, 
              detections: detections,
            ),
          ),
        );
      }
      
    } catch (e) {
      print('❌ Analysis error: $e');
      
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            content: Text('Analisis gagal: ${e.toString()}'),
            duration: Duration(seconds: 3),
          ),
        );
        
        // Tetap navigasi dengan empty results
        Navigator.push(
          context,
          MaterialPageRoute(
            builder: (_) => ResultPage(
              imageFilePath: file.path, 
              detections: [],
            ),
          ),
        );
      }
    }
  }
  
  if (mounted) {
    setState(() => _isAnalyzing = false);
  }
}  @override
  Widget build(BuildContext context) {
    if (!_isInitialized || !_cameraService.isInitialized) {
      return const Scaffold(
        backgroundColor: Colors.black,
        body: Center(child: CircularProgressIndicator(color: Colors.green)),
      );
    }

    return Scaffold(
      backgroundColor: Colors.black,
      body: Stack(
        children: [
          // 1. PREVIEW KAMERA
          // Menggunakan Center + CameraPreview akan mempertahankan rasio asli (biasanya 4:3)
          // Bagian atas/bawah yang sisa akan berwarna hitam (Letterbox), terlihat profesional.
          Center(
            child: CameraPreview(_cameraService.controller!),
          ),

          // 2. TOMBOL KEMBALI (UNDO/BACK) - POJOK KIRI ATAS
          Positioned(
            top: 50, // Jarak aman dari status bar (sinyal/baterai)
            left: 20,
            child: InkWell(
              onTap: () {
                Navigator.pop(context); // Perintah untuk kembali ke Home
              },
              child: Container(
                padding: const EdgeInsets.all(8),
                decoration: BoxDecoration(
                  color: Colors.black54, // Latar semi transparan agar terlihat jelas
                  shape: BoxShape.circle,
                  border: Border.all(color: Colors.white, width: 1.5),
                ),
                child: const Icon(
                  Icons.close, // Ikon X (Close)
                  color: Colors.white,
                  size: 28,
                ),
              ),
            ),
          ),

          // 3. OVERLAY LOADING (JIKA SEDANG PROSES)
          // Di scan_page.dart, update bagian loading:

          if (_isAnalyzing)
            Positioned.fill(
            child: Container(
              color: Colors.black87,
              child: Center(
                child: Card(
                  color: Colors.green[900]!.withOpacity(0.8),
                  elevation: 10,
                  shape: RoundedRectangleBorder(
                    borderRadius: BorderRadius.circular(20),
                  ),
                  child: Padding(
                    padding: const EdgeInsets.all(30),
                    child: Column(
                      mainAxisSize: MainAxisSize.min,
                      children: [
                        // Spinning loader
                        SizedBox(
                          width: 60,
                          height: 60,
                          child: CircularProgressIndicator(
                            strokeWidth: 5,
                            valueColor: AlwaysStoppedAnimation<Color>(Colors.white),
                          ),
                        ),
                        
                        SizedBox(height: 20),
                        
                        // Text
                        Text(
                          "SEDANG ANALISIS",
                          style: TextStyle(
                            color: Colors.white,
                            fontSize: 18,
                            fontWeight: FontWeight.bold,
                          ),
                        ),
                        
                        SizedBox(height: 10),
                        
                        Text(
                          "Gambar sedang diproses oleh AI",
                          style: TextStyle(color: Colors.white70),
                        ),
                        
                        SizedBox(height: 5),
                        
                        Text(
                          "Tunggu 5-10 detik",
                          style: TextStyle(
                            color: Colors.white60,
                            fontSize: 12,
                          ),
                        ),
                      ],
                    ),
                  ),
                ),
              ),
            ),
          ),

          // 4. TOMBOL SHUTTER (JEPRET) - TENGAH BAWAH
          if (!_isAnalyzing)
            Positioned(
              bottom: 50,
              left: 0,
              right: 0,
              child: Center(
                child: GestureDetector(
                  onTap: _onCapturePressed,
                  child: Container(
                    width: 80,
                    height: 80,
                    decoration: BoxDecoration(
                      shape: BoxShape.circle,
                      border: Border.all(color: Colors.white, width: 5),
                      color: Colors.transparent, // Transparan agar terlihat modern
                    ),
                    child: Container(
                      margin: const EdgeInsets.all(4),
                      decoration: const BoxDecoration(
                        shape: BoxShape.circle,
                        color: Colors.white, // Tombol putih di tengah
                      ),
                    ),
                  ),
                ),
              ),
            ),

            // 5. LABEL INSTRUKSI (OPSIONAL)
            if (!_isAnalyzing)
              const Positioned(
                bottom: 150,
                left: 0,
                right: 0,
                child: Text(
                  "Pastikan daun berada di dalam frame",
                  textAlign: TextAlign.center,
                  style: TextStyle(
                    color: Colors.white70, 
                    fontSize: 14,
                    shadows: [Shadow(color: Colors.black, blurRadius: 4)],
                  ),
                ),
              ),
        ],
      ),
    );
  }
}