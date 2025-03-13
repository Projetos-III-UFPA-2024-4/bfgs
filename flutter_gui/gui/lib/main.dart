import 'package:flutter/material.dart';
import 'package:gui/wigets/flutter_map_custom.dart';
import 'package:flutter_dotenv/flutter_dotenv.dart';

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


  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Row(
        children: [
          Expanded(child: FlutterMapCustom()),
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
        ],
      ),
    );
  }
}
