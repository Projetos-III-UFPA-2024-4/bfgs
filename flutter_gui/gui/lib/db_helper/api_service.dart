import 'dart:convert';
import 'package:http/http.dart' as http;

class ApiService {
  static const String baseUrl = 'http://localhost:5000';

  static Future<List<dynamic>> fetchTrafficUpdates() async {
    try {
      final response = await http.get(Uri.parse('$baseUrl/traffic-state'));
      return json.decode(response.body);

    } catch(e) {
      print("Erro fetching traffic_updates: $e");
      return [];
    }
  }

  static Future<List<dynamic>> fetchNotifications() async {
    try {
      final response = await http.get(Uri.parse('$baseUrl/notifications'));

      return json.decode(response.body);
    } catch (e) {
      print('Error fetching notifications: $e');
      return [];
    }
  }
}
