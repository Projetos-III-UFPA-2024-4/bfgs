import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Flutter + SUMO',
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(seedColor: Colors.deepPurple),
      ),
      home: const MyHomePage(title: 'Flutter + SUMO Integration'),
    );
  }
}

class MyHomePage extends StatefulWidget {
  const MyHomePage({super.key, required this.title});
  final String title;

  @override
  State<MyHomePage> createState() => _MyHomePageState();
}

class _MyHomePageState extends State<MyHomePage> {
  String responseMessage = "Aguardando resposta...";

  /// 🔹 Função para iniciar a simulação no SUMO via Flask
  Future<void> startSimulation() async {
    final url = Uri.parse('http://127.0.0.1:5000/getNumberCars'); // URL do Flask

    try {
      final response = await http.get(url); // Faz a requisição HTTP GET

      if (response.statusCode == 200) {
        var data = jsonDecode(response.body); // Converte JSON para Map
        setState(() {
          responseMessage = data["message"]; // Exibe resposta na tela
        });
      } else {
        setState(() {
          responseMessage = "Erro: ${response.statusCode}";
        });
      }
    } catch (e) {
      setState(() {
        responseMessage = "Erro ao conectar: $e";
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        backgroundColor: Theme.of(context).colorScheme.inversePrimary,
        title: Text(widget.title),
      ),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: <Widget>[
            Text(
              responseMessage, // Exibe o status da simulação
              style: Theme.of(context).textTheme.headlineMedium,
            ),
            const SizedBox(height: 20),
            ElevatedButton(
              onPressed: startSimulation, // Chama a API ao clicar
              child: const Text("Iniciar Simulação"),
            ),
          ],
        ),
      ),
    );
  }
}
