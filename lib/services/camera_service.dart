import 'package:camera/camera.dart';

class CameraService {
  CameraController? _controller;

  CameraController? get controller => _controller;
  bool get isInitialized => _controller?.value.isInitialized ?? false;

  Future<void> initialize() async {
    final cameras = await availableCameras();
    if (cameras.isEmpty) return;

    // Gunakan kamera belakang, resolusi tinggi
    _controller = CameraController(
      cameras[0], 
      ResolutionPreset.high, 
      enableAudio: false
    );

    await _controller!.initialize();
  }

  Future<XFile?> takePicture() async {
    if (!isInitialized) return null;
    try {
      // Stop image stream jika ada (safety)
      if (_controller!.value.isStreamingImages) {
        await _controller!.stopImageStream();
      }
      return await _controller!.takePicture();
    } catch (e) {
      print("Error taking picture: $e");
      return null;
    }
  }

  void dispose() {
    _controller?.dispose();
  }
}