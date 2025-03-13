
import "package:flutter_dotenv/flutter_dotenv.dart";
import "package:mysql_client/mysql_client.dart";
import "package:http/http.dart" as http;


Future connect(params) async {
    final conn  = await MySQLConnection.createConnection(host: dotenv.env['DBHOST'], port: dotenv.env['DBPORT'] as int, userName:  dotenv.env['DBUSER']!, password: dotenv.env['DBPASSWORD']!, databaseName: dotenv.env['DBNAME'] );

    return conn;
}

Future read(params) async {
    
    
}
