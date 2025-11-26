import 'dart:io';
import 'package:flutter/material.dart';

class RecordDetailPage extends StatefulWidget {
  final String recordId;
  final String plantName;
  const RecordDetailPage({required this.recordId, required this.plantName});

  @override
  _RecordDetailPageState createState() => _RecordDetailPageState();
}

class _RecordDetailPageState extends State<RecordDetailPage> {
  // mock timeline entries. later persist in DB
  List<Map<String, dynamic>> timeline = [
    {'date': '2025-11-10', 'note': 'Initial detection: leaf spots', 'imagePath': null},
    {'date': '2025-11-12', 'note': 'Applied treatment A', 'imagePath': null},
  ];

  void _addEntry() async {
    // For starter: add a dummy entry with today's date
    final today = DateTime.now();
    setState(() {
      timeline.insert(0, {
        'date': '${today.year}-${today.month.toString().padLeft(2,'0')}-${today.day.toString().padLeft(2,'0')}',
        'note': 'New entry (manual)',
        'imagePath': null
      });
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text(widget.plantName),
      ),
      body: Column(
        children: [
          ListTile(
            leading: Icon(Icons.local_florist, size: 40),
            title: Text(widget.plantName, style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
            subtitle: Text('Record ID: ${widget.recordId}'),
            trailing: ElevatedButton(
              onPressed: _addEntry,
              child: Text('Add Entry'),
            ),
          ),
          Divider(),
          Expanded(
            child: timeline.isEmpty
                ? Center(child: Text('No entries yet. Tap "Add Entry" to create.'))
                : ListView.separated(
                    padding: EdgeInsets.all(12),
                    itemCount: timeline.length,
                    separatorBuilder: (_, __) => Divider(),
                    itemBuilder: (context, i) {
                      final e = timeline[i];
                      return ListTile(
                        leading: e['imagePath'] == null ? Icon(Icons.image) : Image.file(File(e['imagePath']), width: 48, height: 48, fit: BoxFit.cover),
                        title: Text(e['date']),
                        subtitle: Text(e['note']),
                        onTap: () {
                          // show detail modal
                          showDialog(
                            context: context,
                            builder: (_) => AlertDialog(
                              title: Text('Entry ${e['date']}'),
                              content: Text(e['note']),
                              actions: [TextButton(onPressed: () => Navigator.pop(context), child: Text('Close'))],
                            ),
                          );
                        },
                      );
                    },
                  ),
          ),
        ],
      ),
    );
  }
}
