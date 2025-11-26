import 'package:flutter/material.dart';
import '../services/ai_service.dart';
import '../models/detection.dart';

class DiseaseCard extends StatelessWidget {
  final Detection detection;
  const DiseaseCard({required this.detection});

  @override
  Widget build(BuildContext context) {
    return Card(
      margin: EdgeInsets.symmetric(vertical: 8),
      child: ListTile(
        leading: Icon(Icons.bug_report, color: Colors.orange),
        title: Text(detection.label),
        subtitle: Text('Confidence: ${(detection.score * 100).toStringAsFixed(1)}%'),
        trailing: Icon(Icons.arrow_forward_ios, size: 16),
        onTap: () {
          // TODO: show detailed diagnosis + suggestions
          showDialog(
            context: context,
            builder: (_) => AlertDialog(
              title: Text(detection.label),
              content: Text('Suggested actions:\n- Trim infected area\n- Improve airflow\n- Apply fungicide (if applicable)\n\nConfidence: ${(detection.score * 100).toStringAsFixed(1)}%'),
              actions: [TextButton(onPressed: () => Navigator.pop(context), child: Text('Close'))],
            ),
          );
        },
      ),
    );
  }
}
