import 'dart:convert';
import 'package:http/http.dart' as http;

class ApiService {
  static const String baseUrl = 'http://localhost:5000';

  static Future<List<dynamic>> fetchTrafficUpdates() async {
    final response = await http.get(Uri.parse('$baseUrl/traffic-state'));

    if (response.statusCode == 200) {
      return jsonDecode(response.body);
    } else {
      throw Exception("Falha ao recuperar a tabela");
    }
  }
}
