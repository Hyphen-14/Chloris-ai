import 'package:flutter/material.dart';
import 'history_page.dart';
import 'tracker_page.dart';
import 'scan_page.dart'; // Pastikan import ini ada untuk navigasi ke kamera

class MainPage extends StatefulWidget {
  const MainPage({super.key});

  @override
  State<MainPage> createState() => _MainPageState();
}

class _MainPageState extends State<MainPage> {
  int _currentIndex = 0;

  // Daftar halaman untuk navigasi bawah
  final List<Widget> _pages = [
    const HomeTab(),      // Tab 0: Home (Tombol Scan ada di sini)
    const HistoryPage(),  // Tab 1: Riwayat
    const TrackerPage(),  // Tab 2: Tracker
  ];

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      // Menampilkan halaman sesuai index yang dipilih
      body: _pages[_currentIndex],
      
      // Navbar Bawah
      bottomNavigationBar: NavigationBar(
        selectedIndex: _currentIndex,
        onDestinationSelected: (int index) {
          setState(() {
            _currentIndex = index;
          });
        },
        destinations: const [
          NavigationDestination(
            icon: Icon(Icons.home_outlined),
            selectedIcon: Icon(Icons.home),
            label: 'Home',
          ),
          NavigationDestination(
            icon: Icon(Icons.history_outlined),
            selectedIcon: Icon(Icons.history),
            label: 'Riwayat',
          ),
          NavigationDestination(
            icon: Icon(Icons.spa_outlined), // Ikon daun/tanaman
            selectedIcon: Icon(Icons.spa),
            label: 'Tracker',
          ),
        ],
      ),
    );
  }
}

// --- WIDGET HOME TAB (TAMPILAN HALAMAN DEPAN) ---
class HomeTab extends StatelessWidget {
  const HomeTab({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.grey[50],
      body: SafeArea(
        child: Padding(
          padding: const EdgeInsets.all(20.0),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              // 1. Header Salam
              const Text(
                "Halo, Petani Muda! 🌱",
                style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold),
              ),
              const SizedBox(height: 8),
              Text(
                "Jaga kesehatan tanamanmu hari ini.",
                style: TextStyle(color: Colors.grey[600], fontSize: 16),
              ),
              
              const SizedBox(height: 30),

              // 2. Kartu Utama (Tombol Scan)
              InkWell(
                onTap: () {
                  // Navigasi ke halaman kamera (ScanPage)
                  Navigator.push(
                    context,
                    MaterialPageRoute(builder: (context) => const ScanPage()),
                  );
                },
                child: Container(
                  width: double.infinity,
                  height: 180,
                  decoration: BoxDecoration(
                    gradient: const LinearGradient(
                      colors: [Color(0xFF4CAF50), Color(0xFF2E7D32)],
                      begin: Alignment.topLeft,
                      end: Alignment.bottomRight,
                    ),
                    borderRadius: BorderRadius.circular(20),
                    boxShadow: [
                      BoxShadow(
                        color: Colors.green.withOpacity(0.4),
                        blurRadius: 15,
                        offset: const Offset(0, 8),
                      ),
                    ],
                  ),
                  child: const Column(
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: [
                      Icon(Icons.center_focus_strong, size: 60, color: Colors.white),
                      SizedBox(height: 12),
                      Text(
                        "Mulai Diagnosa",
                        style: TextStyle(
                          color: Colors.white, 
                          fontSize: 22, 
                          fontWeight: FontWeight.bold
                        ),
                      ),
                      Text(
                        "Ketuk untuk membuka kamera",
                        style: TextStyle(color: Colors.white70, fontSize: 14),
                      ),
                    ],
                  ),
                ),
              ),

              const SizedBox(height: 30),

              // 3. Fitur Ringkas (Opsional - Pemanis)
              const Text(
                "Fitur Unggulan",
                style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
              ),
              const SizedBox(height: 15),
              
              // Grid Menu Kecil
              Row(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: [
                  _buildMiniCard(Icons.document_scanner, "AI Scanner", Colors.blue),
                  _buildMiniCard(Icons.health_and_safety, "Solusi", Colors.orange),
                  _buildMiniCard(Icons.timeline, "Progress", Colors.purple),
                ],
              )
            ],
          ),
        ),
      ),
    );
  }

  Widget _buildMiniCard(IconData icon, String label, Color color) {
    return Container(
      width: 100,
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(16),
        boxShadow: [
          BoxShadow(color: Colors.grey.withOpacity(0.1), blurRadius: 10)
        ],
      ),
      child: Column(
        children: [
          Icon(icon, color: color, size: 30),
          const SizedBox(height: 8),
          Text(label, style: const TextStyle(fontWeight: FontWeight.w500, fontSize: 12))
        ],
      ),
    );
  }
}