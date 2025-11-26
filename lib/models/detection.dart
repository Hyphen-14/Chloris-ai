import 'dart:ui';

class Detection {
  final Rect rect;
  final String label;
  final double score;

  Detection({
    required this.rect, 
    required this.label, 
    required this.score
  });
}