import 'package:flutter/material.dart';
import 'package:gui/widgets/flutter_map_custom.dart';
import 'package:flutter_dotenv/flutter_dotenv.dart';
import 'package:gui/widgets/traffic_light_properties.dart';
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
  List<dynamic> trafficUpdates = [];
  bool isContainerVisible = false;
  String selectedButton = '';

  Future<void> fetchData(String buttonLabel) async {
    try {
      List<dynamic> data = await ApiService.fetchTrafficUpdates();

      setState(() {
        selectedButton = buttonLabel;
        trafficUpdates = data;
        isContainerVisible = true;
      });
    } catch (e) {
      setState(() {
        trafficUpdates = ['Error $e'];
        isContainerVisible = true;
      });
    }
  }

  void closeContainer() {
    setState(() {
      isContainerVisible = false;
      selectedButton = '';
      trafficUpdates = [];
    });
  }

  
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Row(
        children: [
          Column(
            children: [
              Placeholder(),
            ],
          ),
          Expanded(child: FlutterMapCustom(onButtonPressed: fetchData,)),
          if (isContainerVisible)
          TrafficLightProperties(selectedButton: selectedButton, trafficData: trafficUpdates, onClose: closeContainer),
        ],
      ),
    );
  }
}
