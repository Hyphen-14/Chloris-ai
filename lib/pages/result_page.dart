import 'dart:io';
import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:path_provider/path_provider.dart';
import 'package:path/path.dart' as path;
import 'package:http/http.dart' as http;
import '../models/detection.dart';
import '../services/ai_service.dart';

class ResultPage extends StatefulWidget {
  final String imageFilePath;
  final List<Detection> detections;

  const ResultPage({
    super.key,
    required this.imageFilePath,
    required this.detections,
  });

  @override
  State<ResultPage> createState() => _ResultPageState();
}

class _ResultPageState extends State<ResultPage> {
  final TextEditingController _fileNameController = TextEditingController();
  final TextEditingController _folderNameController = TextEditingController();
  bool _isSaved = false;
  
  // State untuk AI analysis
  List<Detection> _finalDetections = [];
  bool _loading = true;
  String? _errorMessage;
  final AiService _aiService = AiService.instance;

  @override
  void initState() {
    super.initState();
    
    // Default nama file & folder
    _fileNameController.text = "Tanaman_${DateTime.now().millisecondsSinceEpoch}";
    _folderNameController.text = "Kebunku";
    
    // Jalankan AI analysis
    WidgetsBinding.instance.addPostFrameCallback((_) async {
      await _performAnalysis();
    });
  }

  @override
  void dispose() {
    _fileNameController.dispose();
    _folderNameController.dispose();
    super.dispose();
  }

  Future<void> _performAnalysis() async {
    try {
      setState(() {
        _loading = true;
        _errorMessage = null;
      });
      
      // Panggil AI Service (Roboflow + enrichment)
      final results = await _aiService.analyzeImage(widget.imageFilePath);
      
      // Convert ke model Detection
      final detections = results.map((map) => Detection.fromMap(map)).toList();
      
      if (mounted) {
        setState(() {
          _finalDetections = detections;
          _loading = false;
        });
      }
      
    } catch (e) {
      print('❌ Analysis error: $e');
      if (mounted) {
        setState(() {
          _loading = false;
          _errorMessage = 'Gagal menganalisis: $e';
          // Fallback ke detections dari parameter
          _finalDetections = widget.detections;
        });
      }
    }
  }

  // FUNGSI SIMPAN (tetap sama)
  Future<void> _saveToTracker() async {
    if (_fileNameController.text.isEmpty || _folderNameController.text.isEmpty) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(
          content: Text("Nama file dan folder tidak boleh kosong!"),
          backgroundColor: Colors.red,
        ),
      );
      return;
    }

    try {
      final Directory appDir = await getApplicationDocumentsDirectory();
      final String folderPath = path.join(appDir.path, _folderNameController.text);
      final Directory newDirectory = Directory(folderPath);

      if (!await newDirectory.exists()) {
        await newDirectory.create(recursive: true);
      }

      final String newFileName = "${_fileNameController.text}.jpg";
      final String newFilePath = path.join(newDirectory.path, newFileName);

      final File tempFile = File(widget.imageFilePath);
      await tempFile.copy(newFilePath);

      // Juga simpan metadata hasil analisis
      await _saveAnalysisMetadata(newDirectory.path, newFileName);

      if (!mounted) return;

      Navigator.of(context).pop();
      Navigator.of(context).popUntil((route) => route.isFirst);

      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(
          content: Text("Tersimpan di: ${_folderNameController.text}/$newFileName"),
          backgroundColor: Colors.green,
          duration: const Duration(seconds: 3),
        ),
      );

    } catch (e) {
      debugPrint("Error saving: $e");
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text("Gagal menyimpan: $e")),
        );
      }
    }
  }

  // Simpan metadata analisis
  Future<void> _saveAnalysisMetadata(String folderPath, String baseFileName) async {
    try {
      final metadata = {
        'timestamp': DateTime.now().toIso8601String(),
        'original_image': widget.imageFilePath,
        'detections': _finalDetections.map((d) => d.toMap()).toList(),
        'analysis_date': DateTime.now().toString(),
      };
      
      final metadataFile = File('$folderPath/${baseFileName.split('.').first}_meta.json');
      await metadataFile.writeAsString(jsonEncode(metadata));
    } catch (e) {
      print('⚠️ Gagal simpan metadata: $e');
    }
  }

  void _showSaveDialog() {
    showDialog(
      context: context,
      builder: (context) => AlertDialog(
        title: const Text("Simpan ke Tracker"),
        content: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            TextField(
              controller: _folderNameController,
              decoration: const InputDecoration(
                labelText: "Nama Folder",
                hintText: "Cth: Kebun Belakang",
                prefixIcon: Icon(Icons.folder_open),
                border: OutlineInputBorder(),
              ),
            ),
            const SizedBox(height: 16),
            TextField(
              controller: _fileNameController,
              decoration: const InputDecoration(
                labelText: "Nama File",
                hintText: "Cth: Tomat Sakit 1",
                prefixIcon: Icon(Icons.image),
                border: OutlineInputBorder(),
              ),
            ),
          ],
        ),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(context),
            child: const Text("BATAL"),
          ),
          ElevatedButton(
            onPressed: _saveToTracker,
            style: ElevatedButton.styleFrom(backgroundColor: Colors.green),
            child: const Text("SIMPAN", style: TextStyle(color: Colors.white)),
          ),
        ],
      ),
    );
  }

  // Widget untuk menampilkan penyakit
  Widget _buildDiseaseCard(Detection detection) {
    final tingkatBahaya = detection.additionalData?['tingkat_bahaya']?.toString() ?? 'Medium';
    final solusiList = detection.additionalData?['solusi'] as List<dynamic>? ?? [];
    
    Color getColorFromTingkat(String tingkat) {
      switch (tingkat.toLowerCase()) {
        case 'high': return Colors.red;
        case 'medium': return Colors.orange;
        case 'low': return Colors.green;
        default: return Colors.grey;
      }
    }
    
    IconData getIconFromTingkat(String tingkat) {
      switch (tingkat.toLowerCase()) {
        case 'high': return Icons.warning;
        case 'medium': return Icons.error_outline;
        case 'low': return Icons.check_circle;
        default: return Icons.help;
      }
    }
    
    final warna = getColorFromTingkat(tingkatBahaya);
    
    return Card(
      margin: EdgeInsets.symmetric(vertical: 8),
      child: Padding(
        padding: EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            // Header dengan tingkat bahaya dan confidence
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                Row(
                  children: [
                    Icon(getIconFromTingkat(tingkatBahaya), color: warna),
                    SizedBox(width: 8),
                    Text(
                      tingkatBahaya.toUpperCase(),
                      style: TextStyle(
                        color: warna,
                        fontWeight: FontWeight.bold,
                      ),
                    ),
                  ],
                ),
                Chip(
                  label: Text(
                    '${(detection.confidence * 100).toStringAsFixed(1)}%',
                    style: TextStyle(color: Colors.white),
                  ),
                  backgroundColor: detection.confidence > 0.7 
                      ? Colors.green 
                      : detection.confidence > 0.4 
                        ? Colors.orange 
                        : Colors.red,
                ),
              ],
            ),
            
            SizedBox(height: 12),
            
            // Nama penyakit
            Text(
              detection.label,
              style: TextStyle(
                fontSize: 18,
                fontWeight: FontWeight.bold,
              ),
            ),
            
            // Solusi (jika ada)
            if (solusiList.isNotEmpty) ...[
              SizedBox(height: 12),
              Text(
                'Rekomendasi:',
                style: TextStyle(
                  fontWeight: FontWeight.w500,
                  color: Colors.grey[700],
                ),
              ),
              SizedBox(height: 8),
              ...solusiList.take(3).map((solusi) => Padding(
                padding: EdgeInsets.only(bottom: 4),
                child: Row(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Icon(Icons.check, size: 16, color: Colors.green),
                    SizedBox(width: 8),
                    Expanded(child: Text(solusi.toString())),
                  ],
                ),
              )).toList(),
            ],
          ],
        ),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text("Hasil Diagnosa"),
        actions: [
          IconButton(
            icon: Icon(_isSaved ? Icons.check_circle : Icons.save),
            color: _isSaved ? Colors.green : null,
            onPressed: _isSaved ? null : _showSaveDialog,
            tooltip: "Simpan ke Tracker",
          ),
        ],
      ),
      body: Column(
        children: [
          // 1. Gambar dengan bounding boxes
          Expanded(
            flex: 2,
            child: Container(
              width: double.infinity,
              color: Colors.black12,
              child: Stack(
                children: [
                  Image.file(
                    File(widget.imageFilePath),
                    fit: BoxFit.contain,
                    width: double.infinity,
                    height: double.infinity,
                  ),
                  
                  // Bounding boxes untuk detections dengan rect
                  if (!_loading)
                    ..._finalDetections.where((d) => d.rect != null).map((detection) {
                      return Positioned(
                        left: detection.rect!.left * MediaQuery.of(context).size.width,
                        top: detection.rect!.top * MediaQuery.of(context).size.height,
                        width: (detection.rect!.right - detection.rect!.left) * MediaQuery.of(context).size.width,
                        height: (detection.rect!.bottom - detection.rect!.top) * MediaQuery.of(context).size.height,
                        child: Container(
                          decoration: BoxDecoration(
                            border: Border.all(
                              color: detection.confidence > 0.7 
                                ? Colors.green 
                                : detection.confidence > 0.4 
                                  ? Colors.orange 
                                  : Colors.red,
                              width: 2,
                            ),
                          ),
                        ),
                      );
                    }).toList(),
                ],
              ),
            ),
          ),
          
          // 2. Hasil Analisis
          Expanded(
            flex: 3,
            child: Container(
              padding: const EdgeInsets.all(20),
              decoration: const BoxDecoration(
                color: Colors.white,
                borderRadius: BorderRadius.vertical(top: Radius.circular(24)),
              ),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  const Text(
                    "Hasil Deteksi:",
                    style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
                  ),
                  const SizedBox(height: 10),
                  
                  // Loading
                  if (_loading)
                    Expanded(
                      child: Center(
                        child: Column(
                          mainAxisAlignment: MainAxisAlignment.center,
                          children: [
                            CircularProgressIndicator(),
                            SizedBox(height: 16),
                            Text(
                              "Menganalisis dengan Roboflow...",
                              style: TextStyle(color: Colors.grey),
                            ),
                          ],
                        ),
                      ),
                    ),
                  
                  // Error
                  if (!_loading && _errorMessage != null)
                    Expanded(
                      child: Center(
                        child: Column(
                          mainAxisAlignment: MainAxisAlignment.center,
                          children: [
                            Icon(Icons.error, color: Colors.red, size: 50),
                            SizedBox(height: 16),
                            Text(
                              _errorMessage!,
                              textAlign: TextAlign.center,
                              style: TextStyle(color: Colors.red),
                            ),
                            SizedBox(height: 16),
                            ElevatedButton(
                              onPressed: _performAnalysis,
                              child: Text("Coba Lagi"),
                            ),
                          ],
                        ),
                      ),
                    ),
                  
                  // Hasil
                  if (!_loading && _errorMessage == null)
                    Expanded(
                      child: _finalDetections.isEmpty
                          ? Center(
                              child: Column(
                                mainAxisAlignment: MainAxisAlignment.center,
                                children: [
                                  Icon(Icons.check_circle, color: Colors.green, size: 60),
                                  SizedBox(height: 16),
                                  Text(
                                    "Tanaman Sehat!",
                                    style: TextStyle(
                                      fontSize: 18,
                                      fontWeight: FontWeight.bold,
                                      color: Colors.green,
                                    ),
                                  ),
                                  SizedBox(height: 8),
                                  Text(
                                    "Tidak terdeteksi penyakit",
                                    style: TextStyle(color: Colors.grey),
                                  ),
                                ],
                              ),
                            )
                          : ListView.builder(
                              itemCount: _finalDetections.length,
                              itemBuilder: (context, index) => 
                                  _buildDiseaseCard(_finalDetections[index]),
                            ),
                    ),
                  
                  const SizedBox(height: 10),
                  SizedBox(
                    width: double.infinity,
                    child: ElevatedButton(
                      onPressed: () => Navigator.pop(context),
                      style: ElevatedButton.styleFrom(
                        backgroundColor: Colors.green,
                        foregroundColor: Colors.white,
                        padding: EdgeInsets.symmetric(vertical: 16),
                      ),
                      child: const Text("SCAN LAGI"),
                    ),
                  ),
                ],
              ),
            ),
          ),
        ],
      ),
    );
  }
}