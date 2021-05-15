import os
import cloudinary as cloudinary
from flask import Flask, jsonify, render_template, request
from flask_cors import CORS, cross_origin
from flask_restful import Api, Resource, reqparse
import werkzeug
import cloudinary.uploader
import pyodbc
from check_doc_content import verificar_documento

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
api = Api(app)

class ValidateFile(Resource):
    def db_validate(self, people):
        conn = pyodbc.connect('Driver={SQL Server};'
                              'Server=GLADOS\MSSQLSERVER01;'
                              'Database=Northwind;'
                              'Trusted_Connection=yes;')

        for person in people:
            cursor = conn.cursor()
            row = cursor.execute('SELECT * FROM People where CPF = ' +person.cpf).fetchone()
            person.flagAutorizacao = row.flag_documento
            print(row)

        return [person.serialize() for person in people]

    @cross_origin()
    def post(self):
        parse = reqparse.RequestParser()
        parse.add_argument('file', type=werkzeug.datastructures.FileStorage, location='files')
        args = parse.parse_args()
        file = args['file']
        file.save(file.filename)
        return jsonify({'resultData':self.db_validate(verificar_documento(file.filename))})

    @app.route("/upload", methods=['POST'])
    def upload_file():
        app.logger.info('in upload route')
        cloudinary.config(cloud_name=os.getenv('CLOUD_NAME'), api_key=os.getenv('API_KEY'),
                          api_secret=os.getenv('API_SECRET'))
        upload_result = None
        if request.method == 'POST':
            file_to_upload = request.files['file']
            app.logger.info('%s file_to_upload', file_to_upload)
            if file_to_upload:
                upload_result = cloudinary.uploader.upload(file_to_upload)
                app.logger.info(upload_result)
                return jsonify(upload_result["url"])



api.add_resource(ValidateFile, "/validatefile")

if __name__ == "__main__":
    app.run(debug=True)