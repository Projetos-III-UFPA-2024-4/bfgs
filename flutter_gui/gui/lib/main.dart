import 'package:flutter/material.dart';
import 'package:flutter_map/flutter_map.dart';
import 'package:latlong2/latlong.dart';
import 'package:xterm/xterm.dart';

void main() {
  runApp(MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      theme: ThemeData(
        primaryColor: Colors.green[200],
        scaffoldBackgroundColor: Colors.green[50],
        appBarTheme: AppBarTheme(backgroundColor: Colors.green[300]),
        listTileTheme: ListTileThemeData(
          iconColor: Colors.green[600],
          textColor: Colors.green[900],
        ),
      ),
      home: MapScreen(),
    );
  }
}

class MapScreen extends StatefulWidget {
  const MapScreen({super.key});

  @override
  _MapScreenState createState() => _MapScreenState();
}

class _MapScreenState extends State<MapScreen> {
  final LatLng _initialPosition = LatLng(-1.45502, -48.5024);

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Row(
        children: [
          Expanded(
            child: FlutterMap(
              options: MapOptions(initialCenter: _initialPosition),
              children: [
                TileLayer(
                  urlTemplate: 'https://tile.openstreetmap.org/{z}/{x}/{y}.png',
                  userAgentPackageName: 'com.example.app',
                ),
              ],
            ),
          ),

          Container(
            width: 250,
            color: Colors.green[100],
            child: ListView(
              children: List.generate(
                5,
                (index) => ListTile(
                  leading: Icon(Icons.place, color: Colors.green[700]),
                  title: Text(
                    'Local $index',
                    style: TextStyle(color: Colors.green[900]),
                  ),
                  onTap: () {
                    print('Clicou no Local $index');
                  },
                ),
              ),
            ),
          ),

          BottomAppBar(
            // child: TerminalView()
          ),
        ],
      ),
    );
  }
}
