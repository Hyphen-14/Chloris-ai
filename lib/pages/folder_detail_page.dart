import 'dart:io';
import 'package:flutter/material.dart';
import 'package:path/path.dart' as path;

class FolderDetailPage extends StatefulWidget {
  final String folderPath;
  final String folderName;

  const FolderDetailPage({
    super.key,
    required this.folderPath,
    required this.folderName,
  });

  @override
  State<FolderDetailPage> createState() => _FolderDetailPageState();
}

class _FolderDetailPageState extends State<FolderDetailPage> {
  List<FileSystemEntity> _images = [];
  bool _isLoading = true;

  @override
  void initState() {
    super.initState();
    _loadImages();
  }

  // Fungsi membaca isi folder
  void _loadImages() {
    setState(() => _isLoading = true);
    
    final Directory dir = Directory(widget.folderPath);
    
    // Ambil semua file, lalu filter hanya yang berakhiran .jpg atau .png
    List<FileSystemEntity> files = dir.listSync();
    
    setState(() {
      _images = files.where((file) {
        return file.path.toLowerCase().endsWith('.jpg') || 
               file.path.toLowerCase().endsWith('.png');
      }).toList();
      _isLoading = false;
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text(widget.folderName),
      ),
      body: _isLoading
          ? const Center(child: CircularProgressIndicator())
          : _images.isEmpty
              ? const Center(child: Text("Folder ini kosong."))
              : GridView.builder(
                  padding: const EdgeInsets.all(10),
                  gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(
                    crossAxisCount: 2, // Menampilkan 2 foto per baris
                    crossAxisSpacing: 10,
                    mainAxisSpacing: 10,
                    childAspectRatio: 0.8, // Mengatur rasio tinggi kotak
                  ),
                  itemCount: _images.length,
                  itemBuilder: (context, index) {
                    final File imageFile = File(_images[index].path);
                    final String imageName = path.basename(_images[index].path);

                    return Card(
                      elevation: 3,
                      shape: RoundedRectangleBorder(
                        borderRadius: BorderRadius.circular(12),
                      ),
                      clipBehavior: Clip.antiAlias,
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.stretch,
                        children: [
                          // Gambar
                          Expanded(
                            child: Image.file(
                              imageFile,
                              fit: BoxFit.cover,
                            ),
                          ),
                          // Nama File
                          Padding(
                            padding: const EdgeInsets.all(8.0),
                            child: Text(
                              imageName,
                              maxLines: 1,
                              overflow: TextOverflow.ellipsis,
                              style: const TextStyle(fontSize: 12),
                              textAlign: TextAlign.center,
                            ),
                          ),
                        ],
                      ),
                    );
                  },
                ),
    );
  }
}