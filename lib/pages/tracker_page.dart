import 'dart:io';
import 'package:flutter/material.dart';
import 'package:path_provider/path_provider.dart';
import 'package:path/path.dart' as path;
// JANGAN LUPA IMPORT HALAMAN BARU TADI:
import 'folder_detail_page.dart'; 

class TrackerPage extends StatefulWidget {
  const TrackerPage({super.key});

  @override
  State<TrackerPage> createState() => _TrackerPageState();
}

class _TrackerPageState extends State<TrackerPage> {
  List<FileSystemEntity> _folders = [];
  bool _isLoading = true;

  @override
  void initState() {
    super.initState();
    _loadFolders();
  }

  Future<void> _loadFolders() async {
    setState(() => _isLoading = true);
    final appDir = await getApplicationDocumentsDirectory();
    final List<FileSystemEntity> entities = appDir.listSync();
    
    setState(() {
      _folders = entities.whereType<Directory>().toList();
      _isLoading = false;
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text("Tracker Tanaman"),
        actions: [
          IconButton(icon: const Icon(Icons.refresh), onPressed: _loadFolders)
        ],
      ),
      body: _isLoading 
        ? const Center(child: CircularProgressIndicator())
        : _folders.isEmpty
          ? const Center(child: Text("Belum ada folder tanaman tersimpan."))
          : ListView.builder(
              padding: const EdgeInsets.all(16),
              itemCount: _folders.length,
              itemBuilder: (context, index) {
                String folderName = path.basename(_folders[index].path);
                
                return Card(
                  elevation: 2,
                  margin: const EdgeInsets.only(bottom: 12),
                  child: ListTile(
                    leading: const Icon(Icons.folder, color: Colors.amber, size: 40),
                    title: Text(folderName, style: const TextStyle(fontWeight: FontWeight.bold)),
                    subtitle: Text("Ketuk untuk melihat foto tanaman"),
                    trailing: const Icon(Icons.arrow_forward_ios, size: 16),
                    onTap: () {
                      // --- PERUBAHAN DI SINI ---
                      // Navigasi ke halaman detail folder
                      Navigator.push(
                        context,
                        MaterialPageRoute(
                          builder: (context) => FolderDetailPage(
                            folderPath: _folders[index].path,
                            folderName: folderName,
                          ),
                        ),
                      );
                      // -------------------------
                    },
                  ),
                );
              },
            ),
    );
  }
}