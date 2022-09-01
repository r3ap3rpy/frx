from flask import Flask
from flask_restx import Api, Resource, reqparse

app = Flask(__name__)
api = Api(app)

parser = reqparse.RequestParser()
parser.add_argument('name',type = str, help = 'The name of whatnot!')
parser.add_argument('age',type = int, help = 'The age of whatnot!')

@api.route("/<string:name>")
class HelloWorld(Resource):
    def get(self,name):
        return f"Flask-RestX is cool! Name: {name}"
    def post(self):
        return "Post is also working!"

@api.route("/queryparam")
class Query(Resource):
    @api.doc(parser = parser)
    def post(self):
        args = parser.parse_args()
        return f"Hello name: {args['name']} and age: {args['age']}"


if __name__ == '__main__':
    app.run()