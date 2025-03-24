import 'package:flutter/material.dart';

class HoveringContainer extends StatelessWidget {
  final List<dynamic> trafficData;
  final VoidCallback onClose;

  const HoveringContainer({
    super.key,
    required this.trafficData,
    required this.onClose,
  });

  @override
  Widget build(BuildContext context) {
    return Positioned(
      left: 20,
      top: 100,
      child: Material(
        elevation: 8,
        borderRadius: BorderRadius.circular(12),
        child: Container(
          width: 300,
          height: 600,
          decoration: BoxDecoration(
            color: Colors.white,
            borderRadius: BorderRadius.circular(12),
            boxShadow: [
              BoxShadow(
                color: Colors.black26,
                blurRadius: 10,
                spreadRadius: 2,
                offset: Offset(0, 5),
              ),
            ],
          ),
          child: Column(
            children: [
              Container(
                padding: EdgeInsets.all(12),
                decoration: BoxDecoration(
                  color: Colors.green[200],
                  borderRadius: BorderRadius.vertical(top: Radius.circular(12)),
                ),
                child: Row(
                  mainAxisAlignment: MainAxisAlignment.spaceBetween,
                  children: [
                    Text(
                      "Alertas de Tráfego",
                      style: TextStyle(
                        color: Colors.white,
                        fontSize: 16,
                        fontWeight: FontWeight.bold,
                      ),
                    ),
                    IconButton(
                      icon: Icon(Icons.close, color: Colors.white),
                      onPressed: onClose,
                    ),
                  ],
                ),
              ),

              Expanded(
                child:
                    trafficData.isEmpty
                        ? Center(child: Text("No notifications available"))
                        : ListView.builder(
                          padding: EdgeInsets.all(8),
                          itemCount: trafficData.length,
                          itemBuilder: (context, index) {
                            var item = trafficData[index];
                            String message = item['Message'] ?? 'Unknown event';
                            String timestamp = item['Timestamp'] ?? 'No time';

                            return NotificationCard(
                              message: message,
                              timestamp: timestamp,
                            );
                          },
                        ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}

// Notification Card Widget
class NotificationCard extends StatelessWidget {
  final String message;
  final String timestamp;

  const NotificationCard({
    super.key,
    required this.message,
    required this.timestamp,
  });

  IconData _getIcon() {
    switch (message) {
      case 'Pouco Congestionado':
        return Icons.warning_amber_rounded;
      case 'Normal':
        return Icons.check_circle;
      case 'Muito Congestionado':
        return Icons.error;
      default:
        return Icons.notifications;
    }
  }

  Color _getColor() {
    switch (message) {
      case 'Pouco Congestionado':
        return Colors.orange;
      case 'Normal':
        return Colors.green;
      case 'Muito Congestionado':
        return Colors.red;
      default:
        return Colors.grey;
    }
  }

  @override
  Widget build(BuildContext context) {
    return Card(
      color: _getColor().withOpacity(0.2),
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(10)),
      child: ListTile(
        leading: Icon(_getIcon(), color: _getColor()),
        title: Text(message, style: TextStyle(fontWeight: FontWeight.bold)),
        subtitle: Text(timestamp, style: TextStyle(color: Colors.grey[600])),
      ),
    );
  }
}

