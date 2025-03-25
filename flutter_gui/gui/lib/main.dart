import 'package:flutter/material.dart';
import 'package:gui/widgets/flutter_map_custom.dart';
import 'package:gui/widgets/hovering_container.dart';
import 'package:gui/widgets/traffic_light_properties.dart';
import './db_helper/api_service.dart';

main() {
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
  State<MapScreen> createState() => _MapScreenState();
}

class _MapScreenState extends State<MapScreen> {
  List<dynamic> trafficUpdates = [];
  List<dynamic> trafficNotifications = [];
  bool isTrafficPropsVisible = false;
  bool isNotificationsVisible = false;
  String selectedButton = '';
  String trafficLightState = '';


  Future<void> fetchData(String buttonLabel) async {
    try {
      List<dynamic> data = await ApiService.fetchTrafficUpdates();

      setState(() {
        selectedButton = buttonLabel;
        trafficUpdates = data;
        isTrafficPropsVisible = true;
      });
    } catch (e) {
      setState(() {
        trafficUpdates = ['Erro 01: $e'];
        isTrafficPropsVisible = true;
      });
    }

    print(trafficLightState);
  }

  Future<void> fetchTrafficLightState() async {
    try {
      List<dynamic> data = await ApiService.fetchTrafficUpdates();

      setState(() {
        trafficLightState = data[0]['States'];
      });

    } catch (e) {
      print('Error while fetching traffic lights update on main');
      setState(() {
        trafficLightState = 'no states found';
      });
    }
  }

  Future<void> fetchNotifications() async {
    try {

    final response = await ApiService.fetchNotifications();

    setState(() {
      trafficNotifications = response;
      isNotificationsVisible = true;
    });

    } catch (e) {
      setState(() {
        trafficNotifications = ['Erro 02: $e'];
        isNotificationsVisible = false;
      });
    }
  }

  void closeContainer() {
    setState(() {
      isTrafficPropsVisible = false;
      selectedButton = '';
      trafficUpdates = [];
    });
  }

  void closeNotifications() {
    setState(() {
      isNotificationsVisible = false;
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Stack(
        children: [ 
          Row(
            children: [
              FlutterMapCustom(onButtonPressed: fetchData, trafficData: trafficUpdates, trafficLightState: trafficLightState),
              if (isTrafficPropsVisible)
                TrafficLightProperties(
                  selectedButton: selectedButton,
                  trafficData: trafficUpdates,
                  onClose: closeContainer,
                ),
            ],
        ),
        if (isNotificationsVisible)
            HoveringContainer(
              trafficData: trafficNotifications,
              onClose: closeNotifications,
            ),
        FloatingActionButton(onPressed: fetchNotifications, splashColor: const Color.fromARGB(255, 205, 245, 206), backgroundColor: Colors.green[100], child: Icon(Icons.notifications, color: Colors.green,), ),
        
        ],
      ),
    );
  }
}
