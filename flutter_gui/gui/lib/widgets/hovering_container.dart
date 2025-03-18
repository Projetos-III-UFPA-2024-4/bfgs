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
              // Header with Close Button
              Container(
                padding: EdgeInsets.all(12),
                decoration: BoxDecoration(
                  color: Colors.blue,
                  borderRadius: BorderRadius.vertical(top: Radius.circular(12)),
                ),
                child: Row(
                  mainAxisAlignment: MainAxisAlignment.spaceBetween,
                  children: [
                    Text(
                      "Traffic Alerts",
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

              // Notification List
              Expanded(
                child:
                    trafficData.isEmpty
                        ? Center(child: Text("No notifications available"))
                        : ListView.builder(
                          padding: EdgeInsets.all(8),
                          itemCount: trafficData.length,
                          itemBuilder: (context, index) {
                            var item = trafficData[index];
                            String message = item['message'] ?? 'Unknown event';
                            String category = item['category'] ?? 'info';
                            String timestamp = item['timestamp'] ?? 'No time';

                            return NotificationCard(
                              message: message,
                              category: category,
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
  final String category;
  final String timestamp;

  const NotificationCard({
    super.key,
    required this.message,
    required this.category,
    required this.timestamp,
  });

  IconData _getIcon() {
    switch (category) {
      case 'alert':
        return Icons.warning_amber_rounded;
      case 'info':
        return Icons.info;
      case 'success':
        return Icons.check_circle;
      case 'error':
        return Icons.error;
      default:
        return Icons.notifications;
    }
  }

  Color _getColor() {
    switch (category) {
      case 'alert':
        return Colors.orange;
      case 'info':
        return Colors.blue;
      case 'success':
        return Colors.green;
      case 'error':
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
