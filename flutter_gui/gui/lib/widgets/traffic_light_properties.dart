import 'package:flutter/material.dart';

class TrafficLightProperties extends StatelessWidget {
  final String selectedButton;
  final List<dynamic> trafficData;
  final VoidCallback onClose;

  const TrafficLightProperties({
    super.key,
    required this.selectedButton,
    required this.trafficData,
    required this.onClose,
  });

  @override
  Widget build(BuildContext context) {
    return Expanded(
      flex: 2,
      child: Container(
        padding: EdgeInsets.all(16),
        color: Colors.blueGrey[100],
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                Text(
                  'Dados para: $selectedButton',
                  style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
                ),
                IconButton(
                  icon: Icon(Icons.close),
                  onPressed: onClose,
                ),
              ],
            ),
            Divider(),
            Expanded(
              child: ListView.builder(
                itemCount: trafficData.length,
                itemBuilder: (context, index) {
                  return ListTile(
                    title: Text(trafficData[index].toString()),
                  );
                },
              ),
            ),
          ],
        ),
      ),
    );
  }
}
