import 'dart:io';
import 'package:flutter/material.dart';
import 'package:path_provider/path_provider.dart'; // Untuk akses folder penyimpanan
import 'package:path/path.dart' as path; // Untuk memanipulasi nama file
import '../models/detection.dart';
import '../widgets/disease_card.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';

class ResultPage extends StatefulWidget {
  final String imageFilePath;
  final List<Detection> detections; // tetap terima, tapi kita gunakan local state

  const ResultPage({
    super.key,
    required this.imageFilePath,
    required this.detections,
  });

  @override
  State<ResultPage> createState() => _ResultPageState();
}

class _ResultPageState extends State<ResultPage> {
  // Controller untuk input teks
  final TextEditingController _fileNameController = TextEditingController();
  final TextEditingController _folderNameController = TextEditingController();
  bool _isSaved = false;

  // <-- GANTI: gunakan state lokal untuk menyimpan hasil backend
  List<Detection> _backendDetections = [];
  bool _loading = true; // untuk menampilkan loading spinner

  @override
  void initState() {
    super.initState();

    // default nama file & folder
    _fileNameController.text = "Tanaman_${DateTime.now().millisecondsSinceEpoch}";
    _folderNameController.text = "Kebunku";

    // jalankan inference setelah frame build
    WidgetsBinding.instance.addPostFrameCallback((_) async {
      try {
        final results = await _fetchDetectionsFromBackend(widget.imageFilePath);
        if (!mounted) return;
        
        setState(() {
          _backendDetections = results;
          _loading = false;
        });
      } catch (e) {
        // error -> tetap hentikan loading dan tunjukkan message
        if (!mounted) return;

        setState(() {
          _backendDetections = [];
          _loading = false;
        });
        if (mounted) {
          ScaffoldMessenger.of(context).showSnackBar(
            SnackBar(content: Text("Gagal memanggil backend: $e")),
          );
        }
      }
    });
  }

  @override
  void dispose() {
    _fileNameController.dispose();
    _folderNameController.dispose();
    super.dispose();
  }

  // sambung backend
  Future<List<Detection>> _fetchDetectionsFromBackend(String imagePath) async {
    final uri = Uri.parse("http://10.237.126.133:8000/predict-image");

    final request = http.MultipartRequest("POST", uri);
    request.files.add(await http.MultipartFile.fromPath("file", imagePath));

    final streamed = await request.send();
    final response = await http.Response.fromStream(streamed);

    // *** DEBUG: tampilkan body response supaya mudah cek apa backend kirimkan
    // buka console log di Flutter (debug console)
    debugPrint("API response status: ${response.statusCode}");
    debugPrint("API response body: ${response.body}");

    if (response.statusCode != 200) {
      throw Exception("Gagal memanggil API: ${response.statusCode} ${response.body}");
    }

    final data = jsonDecode(response.body);

    if (data["ok"] != true) {
      throw Exception("Backend error: ${data['error'] ?? 'unknown'}");
    }

    List detectionsJson = data["detections"] ?? [];

    // backend diasumsikan mengirim box dalam rasio 0..1 (normalisasi)
    return detectionsJson.map<Detection>((d) {
      final box = d["box"];
      // convert to Rect using ratio (left, top, right, bottom)
      return Detection(
        rect: Rect.fromLTRB(
          (box["x1"] as num).toDouble(),
          (box["y1"] as num).toDouble(),
          (box["x2"] as num).toDouble(),
          (box["y2"] as num).toDouble(),
        ),
        label: d["label"] ?? "unknown",
        score: (d["score"] as num).toDouble(),
      );
    }).toList();
  }

  // LOGIKA UTAMA: Simpan File ke Folder Khusus
  Future<void> _saveToTracker() async {
    // 1. Cek apakah kolom input kosong
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
      // 2. Dapatkan direktori penyimpanan
      final Directory appDir = await getApplicationDocumentsDirectory();

      // 3. Siapkan Folder Tujuan
      final String folderPath = path.join(appDir.path, _folderNameController.text);
      final Directory newDirectory = Directory(folderPath);

      // Buat folder jika belum ada
      if (!await newDirectory.exists()) {
        await newDirectory.create(recursive: true);
      }

      // 4. Siapkan Nama File Baru
      final String newFileName = "${_fileNameController.text}.jpg";
      final String newFilePath = path.join(newDirectory.path, newFileName);

      // 5. Salin file dari Cache ke Folder Tujuan
      final File tempFile = File(widget.imageFilePath);
      await tempFile.copy(newFilePath);

      if (!mounted) return;

      Navigator.of(context).pop(); // tutup dialog
      Navigator.of(context).popUntil((route) => route.isFirst);

      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(
          content: Text("Tersimpan di folder: ${_folderNameController.text}"),
          backgroundColor: Colors.green,
          duration: const Duration(seconds: 3),
        ),
      );

    } catch (e) {
      debugPrint("Error saving file: $e");
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text("Gagal menyimpan: $e")),
        );
      }
    }
  }

  // TAMPILAN: Dialog Formulir Simpan
  void _showSaveDialog() {
    showDialog(
      context: context,
      builder: (context) {
        return AlertDialog(
          title: const Text("Simpan ke Tracker"),
          content: Column(
            mainAxisSize: MainAxisSize.min,
            children: [
              TextField(
                controller: _folderNameController,
                decoration: const InputDecoration(
                  labelText: "Nama Folder (Kategori)",
                  hintText: "Cth: Kebun Belakang",
                  prefixIcon: Icon(Icons.folder_open),
                  border: OutlineInputBorder(),
                ),
              ),
              const SizedBox(height: 16),
              TextField(
                controller: _fileNameController,
                decoration: const InputDecoration(
                  labelText: "Nama File (Tanaman)",
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
              child: const Text("Batal"),
            ),
            ElevatedButton(
              onPressed: _saveToTracker,
              style: ElevatedButton.styleFrom(backgroundColor: Colors.green),
              child: const Text("SIMPAN", style: TextStyle(color: Colors.white)),
            ),
          ],
        );
      },
    );
  }

  // Optional helper: convert normalized rect (0..1) to pixel rect given image display size
  Rect _rectFromNormalized(Rect normalized, double imgW, double imgH) {
    return Rect.fromLTRB(
      normalized.left * imgW,
      normalized.top * imgH,
      normalized.right * imgW,
      normalized.bottom * imgH,
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
            color: _isSaved ? Colors.green : Colors.black,
            onPressed: _isSaved ? null : _showSaveDialog,
            tooltip: "Simpan ke Tracker",
          ),
        ],
      ),
      body: Column(
        children: [
          // 1. Gambar
          Expanded(
            flex: 2,
            child: Container(
              width: double.infinity,
              color: Colors.black12,
              child: Image.file(File(widget.imageFilePath), fit: BoxFit.contain),
            ),
          ),
          // 2. Hasil AI
          Expanded(
            flex: 3,
            child: Container(
              padding: const EdgeInsets.all(20),
              decoration: const BoxDecoration(
                color: Colors.white,
                borderRadius: BorderRadius.vertical(top: Radius.circular(24)),
                boxShadow: [BoxShadow(blurRadius: 10, color: Colors.black12)],
              ),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  const Text("Terdeteksi:", style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
                  const SizedBox(height: 10),

                  // jika masih loading tunjukkan spinner
                  if (_loading) const Center(child: CircularProgressIndicator()),

                  // Tampilkan hasil jika ada
                  if (!_loading)
                    Expanded(
                      child: _backendDetections.isEmpty
                          ? const Center(child: Text("Tidak ada deteksi."))
                          : ListView.builder(
                              itemCount: _backendDetections.length,
                              itemBuilder: (context, index) => DiseaseCard(detection: _backendDetections[index]),
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
                      ),
                      child: const Text("SCAN LAGI"),
                    ),
                  )
                ],
              ),
            ),
          ),
        ],
      ),
    );
  }
}
