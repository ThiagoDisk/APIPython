from flask import Flask
from flask_restful import Api, Resource, reqparse
import werkzeug

app = Flask(__name__)
api = Api(app)


class HelloWorld(Resource):
    def get(self):
        return "Hello World"

    def post(self):
        parse = reqparse.RequestParser()
        parse.add_argument('file', type=werkzeug.datastructures.FileStorage, location='files')
        args = parse.parse_args()
        file = args['file']
        file.save("first_file.jpg")
        return {"data": "Posted"}


api.add_resource(HelloWorld, "/helloworld")

if __name__ == "__main__":
    app.run(debug=True)
