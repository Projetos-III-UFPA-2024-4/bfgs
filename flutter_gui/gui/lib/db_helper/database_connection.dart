
import "package:flutter_dotenv/flutter_dotenv.dart";
import "package:mysql_client/mysql_client.dart";
import "package:http/http.dart" as http;



class DatabaseConnection {


    
    







    static Future createConnection() async {

        final conn  = await MySQLConnection.createConnection(host: dotenv.env['DBHOST'], port: dotenv.env['DBPORT'] as int, userName:  dotenv.env['DBUSER']!, password: dotenv.env['DBPASSWORD']!, databaseName: dotenv.env['DBNAME'] );
        
        conn.connect();

        return conn;
    }

    static Future read(MySQLConnection connection) async {
        var result = await connection.execute('SELECT * FROM ${dotenv.env['DBNAME']}');

        for (var value in result.rows) {
            Map data = value.assoc();

            print(
                'Id: ${data['id']}'
            );
        }
    }




}





