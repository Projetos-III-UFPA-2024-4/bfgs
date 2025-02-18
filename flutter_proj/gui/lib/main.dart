import 'dart:io';

void main() async {
  try {
    final socket = await Socket.connect('localhost', 2000); // Connect to server
    print('Connected to server');

    // Send data to the server
    socket.write("0xa4");

    // Listen for responses from the server
    socket.listen(
      (data) {
        print(String.fromCharCodes(data).trim());
        print(data);
      },
      onDone: () {
        print('Connection closed by server');
        socket.destroy();
      },
      onError: (error) {
        print('Error: $error');
      },
    );

    // Close the connection after sending a message
    await Future.delayed(Duration(seconds: 2));
    // socket.close();
  } catch (e) {
    print('Unable to connect: $e');
  }
}
