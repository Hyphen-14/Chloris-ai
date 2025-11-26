import 'package:flutter/material.dart';
import 'package:camera/camera.dart';
// Import halaman utama yang baru
import 'pages/main_page.dart'; 

List<CameraDescription> cameras = [];

Future<void> main() async {
  WidgetsFlutterBinding.ensureInitialized();
  try {
    cameras = await availableCameras();
  } on CameraException catch (e) {
    print('Error: $e');
  }
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Plant Scan App',
      debugShowCheckedModeBanner: false,
      theme: ThemeData(
        primarySwatch: Colors.green,
        useMaterial3: true,
        // Atur font family jika mau, atau biarkan default
      ),
      // Arahkan ke MainPage (Halaman Home + Navbar)
      home: const MainPage(),
    );
  }
}