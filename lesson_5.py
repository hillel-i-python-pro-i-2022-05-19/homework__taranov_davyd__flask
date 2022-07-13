import sqlite3

from flask import Flask
from webargs import fields
from webargs.flaskparser import use_args

from settings import DB_PATH

app = Flask(__name__)


class Connection:
    def __init__(self):
        self._connection: sqlite3.Connection | None = None

    def __enter__(self):
        self._connection = sqlite3.connect(DB_PATH)
        self._connection.row_factory = sqlite3.Row
        return self._connection

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._connection.close()


@app.route('/users/read-all')
def users__read_all():
    with Connection() as connection:
        users = connection.execute("SELECT * FROM users;").fetchall()
    # !!!
    return '<br>'.join([f'''{user['pk']}: {user['name']} - {user['age']}''' for user in users])


@app.route('/users/create')
@use_args({"name": fields.Str(required=True), "age": fields.Int(required=True)}, location="query")
def users__create(args):
    with Connection() as connection:
        with connection:
            connection.execute(
                'INSERT INTO users (name, age) VALUES (:name, :age);',
                {'name': args['name'], 'age': args['age']}
            )
        # connection.commit()
    return 'OK'


@app.route('/users/delete/<int:pk>')
def users__delete(pk: int):
    with Connection() as connection:
        with connection:
            connection.execute(
                'DELETE FROM users WHERE (pk=:pk);',
                {'pk': pk}
            )
        # connection.commit()
    return 'OK'


@app.route('/users/update/<int:pk>')
@use_args({"age": fields.Int(required=True)}, location="query")
def users__update(args, pk):
    with Connection() as connection:
        with connection:
            connection.execute(
                'UPDATE users '
                'SET age=:age '
                'WHERE pk=:pk;',
                {'age': args['age'], 'pk': pk}
            )
    return 'OK'


@app.route('/')
def hello_world():
    return '<h1>Hello World!</h1>'


if __name__ == '__main__':
    app.run()
