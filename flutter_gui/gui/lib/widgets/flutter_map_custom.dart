import 'package:flutter_map/flutter_map.dart';
import 'package:flutter/material.dart';
import 'package:latlong2/latlong.dart';

class FlutterMapCustom extends StatelessWidget {
  FlutterMapCustom({
      super.key, 
      required this.onButtonPressed, 
      required this.trafficData, 
      required this.trafficLightState
    });


  final LatLng _initialCenter = LatLng(-1.412163, -48.442363);
  final String trafficLightState;
  final Function(String) onButtonPressed;
  final List<dynamic> trafficData;


  void selectColor(int id) {
    print(trafficLightState.characters);
  }

  @override
  Widget build(BuildContext context) {
    return Expanded(
      flex: 4,
      child: FlutterMap(
        options: MapOptions(initialCenter: _initialCenter, initialZoom: 19.0),
        children: [
          TileLayer(
            urlTemplate: 'https://tile.openstreetmap.org/{z}/{x}/{y}.png',
            userAgentPackageName: 'com.example.app',
          ),
          MarkerLayer(
            markers: [      
              Marker(
                child: ElevatedButton(
                  onPressed: () => onButtonPressed('LA'),
                  style: ElevatedButton.styleFrom(
                    backgroundColor: Colors.red,
                  ),
                  child: Text('LA', style:  TextStyle(fontWeight: FontWeight.bold, color: Colors.white),),
                ),
                point: LatLng(-1.411914, -48.442602), //-1.412062/-48.442478
                width: 80,
                height: 80,
              ),
              Marker(
                child: ElevatedButton(
                  onPressed: () {
                    onButtonPressed('LB');
                  },
                  style: ElevatedButton.styleFrom(
                    backgroundColor: Colors.red,
                  ),
                  child: const Text("LB", style:  TextStyle(fontWeight: FontWeight.bold, color: Colors.white)),
                ),
                point: LatLng(-1.412311, -48.442248), // -1.412373/-48.442162
                width: 80,
                height: 80,
              ),
              Marker(
                child: ElevatedButton(
                  onPressed: () {
                    onButtonPressed('LC');
                  },
                  style: ElevatedButton.styleFrom(
                    backgroundColor: Colors.green,
                  ),
                  child: const Text('LC', style:  TextStyle(fontWeight: FontWeight.bold, color: Colors.white)),
                ),
                point: LatLng(-1.411852, -48.442191), // -1.412029/-48.442248
                width: 80,
                height: 80,
              ),
              Marker(
                child: ElevatedButton(
                  onPressed: () {
                    onButtonPressed('LD');
                  },
                  style: ElevatedButton.styleFrom(
                    backgroundColor: Colors.green,
                  ),
                  child: const Text('LD', style:  TextStyle(fontWeight: FontWeight.bold, color: Colors.white)),
                ),
                
                point: LatLng(-1.412394, -48.442586), // -1.412359/-48.442626
                width: 80,
                height: 80,
              ),
            ],
          ),
        ],
      ),
    );
  }
}