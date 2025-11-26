import 'package:flutter/material.dart';
import '../services/ai_service.dart';

class BoundingBoxOverlay extends StatelessWidget {
  final List<Detection> detections;
  const BoundingBoxOverlay({this.detections = const []});

  @override
  Widget build(BuildContext context) {
    return LayoutBuilder(builder: (context, constraints) {
      return Stack(
        children: detections.map((d) {
          // d.rect is normalized: left, top, width, height
          final left = d.rect.left * constraints.maxWidth;
          final top = d.rect.top * constraints.maxHeight;
          final width = d.rect.width * constraints.maxWidth;
          final height = d.rect.height * constraints.maxHeight;
          return Positioned(
            left: left,
            top: top,
            width: width,
            height: height,
            child: Container(
              decoration: BoxDecoration(
                border: Border.all(color: Colors.redAccent, width: 3),
                borderRadius: BorderRadius.circular(4),
              ),
              child: Align(
                alignment: Alignment.topLeft,
                child: Container(
                  padding: EdgeInsets.symmetric(horizontal: 6, vertical: 2),
                  color: Colors.redAccent.withOpacity(0.8),
                  child: Text(
                    '${d.label} (${(d.score * 100).toStringAsFixed(0)}%)',
                    style: TextStyle(color: Colors.white, fontSize: 12),
                  ),
                ),
              ),
            ),
          );
        }).toList(),
      );
    });
  }
}
