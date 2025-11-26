import 'dart:io';
import 'package:http/http.dart' as http;

class ApiService {
  static const String baseUrl = http://YOUR_PC_IP_ADDRESS:8000

  static Future<String> sendImage(File image) async {
    final uri = Uri.parse("$baseUrl/predict-image");
    final request = http.MultipartRequest("POST", uri);

    request.files.add(
      await http.MultipartFile.fromPath("file", image.path),
    );

    final response = await request.send();
    final respStr = await response.stream.bytesToString();
    return respStr;
  }
}
