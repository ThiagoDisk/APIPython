from flask import Flask, jsonify
from flask_cors import CORS, cross_origin
from flask_restful import Api, Resource, reqparse
import werkzeug
import pyodbc;
from check_doc_content import verificar_documento

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
api = Api(app)


class ValidateFile(Resource):
    @cross_origin()
    def post(self):
        parse = reqparse.RequestParser()
        parse.add_argument('file', type=werkzeug.datastructures.FileStorage, location='files')
        args = parse.parse_args()
        file = args['file']
        file.save(file.filename)
        return jsonify({'resultData': verificar_documento(file.filename)})

    def db_connection(self):
        conn = pyodbc.connect('Driver={SQL Server};'
                              'Server=DESKTOP-0CVQI3R;'
                              'Database=Northwind;'
                              'Trusted_Connection=yes;')

        cursor = conn.cursor()
        cursor.execute('SELECT * FROM Customers')

        for row in cursor:
            print(row);


api.add_resource(ValidateFile, "/validatefile")

if __name__ == "__main__":
    app.run(debug=True)
