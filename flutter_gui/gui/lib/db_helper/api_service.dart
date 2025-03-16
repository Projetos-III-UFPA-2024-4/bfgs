import 'dart:convert';
import 'package:http/http.dart' as http;

class ApiService {
  static const String baseUrl = 'http://localhost:5000';

  static Future<List<dynamic>> fetchTrafficUpdates() async {
    try {
      final response = await http.get(Uri.parse('$baseUrl/traffic-state'));
      return json.decode(response.body);

    } catch(e) {
      print("Exception deets: $e");
      return [];
    }  
  }
}
