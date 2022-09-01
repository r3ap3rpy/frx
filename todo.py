from pydoc import describe
from flask import Flask
from flask_restx import Api, Resource, fields
from werkzeug.middleware.proxy_fix import ProxyFix

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app)
api = Api(app, version = '1.0', title = 'ToDo app', description = 'A python demo!')

ns = api.namespace('todos', description = 'TODO operations')

todo = api.model('ToDo', {
    'id' : fields.Integer(readonly = True, description = 'The unique task id!'),
    'task' : fields.String(required = True, description = 'The task details!')
})

class TodoDAO(object):
    def __init__(self):
        self.counter = 0
        self.todos = []

    def get(self, id):
        for todo in self.todos:
            if todo['id'] == id:
                return todo
        api.abort(404, f"The specified todo {id} does not exist!")

    def create(self, data):
        todo = data
        todo['id'] = self.counter = self.counter + 1
        self.todos.append(todo)
        return todo
    def update(self, id, data):
        todo = self.get(id)
        todo.update(data)
        return todo
    def delete(self, id):
        todo = self.get(id)
        self.todos.remove(todo)

DAO = TodoDAO()
DAO.create({'task':'Build an API!'})
DAO.create({'task':'Build a python solution!'})
DAO.create({'task':'Build an ark!'})

@ns.route('/')
class TodoList(Resource):
    @ns.doc('list_todos')
    @ns.marshal_list_with(todo)
    def get(self):
        return DAO.todos

    @ns.doc('create_todo')
    @ns.expect(todo)
    @ns.marshal_with(todo, code = 201)
    def post(self):
        return DAO.create(api.payload),201

@ns.route('/<int:id>')
@ns.response(404,'Todo not found!')
@ns.param('id','The task identifier')
class Todo(Resource):
    @ns.doc('get_todo')
    @ns.marshal_with(todo)
    def get(selff, id):
        return DAO.get(id)

    @ns.doc('delete_todo')
    @ns.response(204, 'Todo deleted')
    def delete(self, id):
        DAO.delete(id)
        return '',204

    @ns.expect(todo)
    @ns.marshal_with(todo)
    def put(self, id):
        return DAO.update(id, api.payload)

if __name__ == '__main__':
    app.run(debug = True)