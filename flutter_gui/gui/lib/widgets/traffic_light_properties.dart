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

  int findDataId() {
    switch (selectedButton) {
      case 'LA':
        return 1;
      case 'LB':
        return 2;
      case 'LC':
        return 3;
      case 'LD':
        return 4;
      default:
        return -1;
    }
  }

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
                IconButton(icon: Icon(Icons.close), onPressed: onClose),
              ],
            ),
            Divider(),
            Expanded(
              flex: 1,
              child: Column(
                children: [
                  PropCard(
                    title: 'Id de Fase',
                    propItem:
                        trafficData.isNotEmpty
                            ? trafficData[trafficData.length -
                                    findDataId()]['phase_id']
                                .toString()
                            : 'Phase not found',
                  ),
                  PropCard(
                    title: 'Tempo de Ciclo',
                    propItem:
                        trafficData.isNotEmpty
                            ? '${trafficData[trafficData.length - findDataId()]['cycle_time'].toStringAsFixed(2)} s'
                            : 'Cycle not found',
                  ),
                  PropCard(
                    title: 'Tempo de Verde',
                    propItem:
                        trafficData.isNotEmpty
                            ? '${trafficData[trafficData.length - findDataId()]['green_time'].toStringAsFixed(2)} s'
                            : 'Green time not found',
                  ),
                ],
              ),
            ),
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                Text(
                  'Comandos',
                  style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
                ),
              ],
            ),
            Divider(),
            SendData(),
          ],
        ),
      ),
    );
  }
}

class PropCard extends StatelessWidget {
  final String title;
  final String propItem;

  const PropCard({super.key, required this.title, required this.propItem});

  @override
  Widget build(BuildContext context) {
    return Card(
      color: Colors.green[200],
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(10)),
      child: ListTile(
        title: Text(
          title,
          style: TextStyle(fontWeight: FontWeight.bold, color: Colors.white),
        ),
        subtitle: Text(
          propItem,
          style: TextStyle(
            color: const Color.fromARGB(255, 0, 0, 0),
            fontWeight: FontWeight.bold,
          ),
        ),
      ),
    );
  }
}

class SendData extends StatelessWidget {
  const SendData({super.key});

  @override
  Widget build(BuildContext context) {
    return Expanded(
      flex: 2,
      child: Column(
        mainAxisSize: MainAxisSize.max,
        children: [
          TextFormField(
            decoration: InputDecoration(
              border: OutlineInputBorder(),
              hintText: 'fase',
            ),
          ),
          SizedBox(height: 15),
          TextFormField(
            decoration: InputDecoration(
              border: OutlineInputBorder(),
              hintText: 'tempo',
            ),
          ),
        ],
      ),
    );
  }
}

class MyCustomForm extends StatefulWidget {
  const MyCustomForm({super.key});

  @override
  MyCustomFormState createState() {
    return MyCustomFormState();
  }
}


class MyCustomFormState extends State<MyCustomForm> {
  // Create a global key that uniquely identifies the Form widget
  // and allows validation of the form.
  //
  // Note: This is a GlobalKey<FormState>,
  // not a GlobalKey<MyCustomFormState>.
  final _formKey = GlobalKey<FormState>();

  @override
  Widget build(BuildContext context) {
    // Build a Form widget using the _formKey created above.
    return Form(
      key: _formKey,
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          TextFormField(
            // The validator receives the text that the user has entered.
            validator: (value) {
              if (value == null || value.isEmpty) {
                return 'Please enter some text';
              }
              return null;
            },
          ),
          Padding(
            padding: const EdgeInsets.symmetric(vertical: 16),
            child: ElevatedButton(
              onPressed: () {
                // Validate returns true if the form is valid, or false otherwise.
                if (_formKey.currentState!.validate()) {
                  // If the form is valid, display a snackbar. In the real world,
                  // you'd often call a server or save the information in a database.
                  ScaffoldMessenger.of(context).showSnackBar(
                    const SnackBar(content: Text('Processing Data')),
                  );
                }
              },
              child: const Text('Submit'),
            ),
          ),
        ],
      ),
    );
  }
}
