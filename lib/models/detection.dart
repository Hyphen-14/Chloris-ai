// lib/models/detection.dart
import 'dart:ui';

class Detection {
  final Rect? rect;
  final String label;
  final double confidence;
  final Map<String, dynamic>? additionalData;
  
  Detection({
    this.rect,
    required this.label,
    required this.confidence,
    this.additionalData,
  });
  
  factory Detection.fromMap(Map<String, dynamic> map) {
    Rect? rect;
    
    if (map['rect'] != null && map['rect'] is Map<String, dynamic>) {
      final rectMap = map['rect'] as Map<String, dynamic>;
      rect = Rect.fromLTRB(
        (rectMap['left'] as num?)?.toDouble() ?? 0.0,
        (rectMap['top'] as num?)?.toDouble() ?? 0.0,
        (rectMap['right'] as num?)?.toDouble() ?? 0.0,
        (rectMap['bottom'] as num?)?.toDouble() ?? 0.0,
      );
    }
    
    return Detection(
      rect: rect,
      label: map['label']?.toString() ?? 'Unknown',
      confidence: (map['confidence'] as num?)?.toDouble() ?? 0.0,
      additionalData: map['additionalData'] as Map<String, dynamic>?,
    );
  }
  
  // TAMBAHKAN METHOD toMap() INI ↓
  Map<String, dynamic> toMap() {
    return {
      'rect': rect != null ? {
        'left': rect!.left,
        'top': rect!.top,
        'right': rect!.right,
        'bottom': rect!.bottom,
      } : null,
      'label': label,
      'confidence': confidence,
      'additionalData': additionalData,
    };
  }
  
  @override
  String toString() {
    return 'Detection($label: ${(confidence * 100).toStringAsFixed(1)}%)';
  }
}