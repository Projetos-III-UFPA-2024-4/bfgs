import 'package:flutter/material.dart';
import 'package:gui/wigets/flutter_map_custom.dart';
import 'package:flutter_dotenv/flutter_dotenv.dart';
import './db_helper/api_service.dart';

main() {
  dotenv.load(fileName: ".env");
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

class MyAppState extends ChangeNotifier {
  // todo: estados arquivados no db
}

class MapScreen extends StatefulWidget {
  const MapScreen({super.key});

  @override
  State<MapScreen> createState() => _MapScreenState();
}

class _MapScreenState extends State<MapScreen> {
  List trafficUpdates = [];

  @override
  void initState() {
    super.initState();
    _loadTrafficUpdates();
  }

  Future<void> _loadTrafficUpdates() async {
    trafficUpdates = await ApiService.fetchTrafficUpdates();
    setState(() {
      
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Row(
        children: [
          Expanded(child: FlutterMapCustom()),
          Container(
            width: 250,
            color: Colors.green[100],
            child: ListView.builder(
              itemCount: trafficUpdates.length,
              itemBuilder: (context, index) {
                return ListTile(
                  title: Text("${trafficUpdates[index]['traffic_light_id']}"),
                  subtitle: Text("Lost time: ${trafficUpdates[index]['lost_time']}"),
                );
              },
            ),
          ),
        ],
      ),
    );
  }
}
