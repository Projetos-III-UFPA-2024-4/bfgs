import 'package:flutter_map/flutter_map.dart';
import 'package:flutter/material.dart';
import 'package:latlong2/latlong.dart';

class FlutterMapCustom extends StatelessWidget {
  FlutterMapCustom({super.key, required this.onButtonPressed});

  final LatLng _initialCenter = LatLng(-1.412163, -48.442363);

  final Function(String) onButtonPressed;


  @override
  Widget build(BuildContext context) {
    return FlutterMap(
      options: MapOptions(initialCenter: _initialCenter, initialZoom: 19.0),
      children: [
        TileLayer(
          urlTemplate: 'https://tile.openstreetmap.org/{z}/{x}/{y}.png',
          userAgentPackageName: 'com.example.app',
        ),
        MarkerLayer(
          markers: [
            //Marker(
            //  child: ElevatedButton(
            //    onPressed: () {
            //      print('l1');
            //    },
            //    child: null,
            //  ),
            //  point: LatLng(-1.412062, -48.442478), //-1.412062/-48.442478
            //  width: 80,
            // height: 80,
            // )
            Marker(
              child: ElevatedButton(
                onPressed: () => onButtonPressed('LA'),
                child: const Text('LA'),
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
                child: const Text("LB"),
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
                child: const Text('LC'),
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
                child: const Text('LD'),
              ),
              point: LatLng(-1.412394, -48.442586), // -1.412359/-48.442626
              width: 80,
              height: 80,
            ),
          ],
        ),
      ],
    );
  }
}
