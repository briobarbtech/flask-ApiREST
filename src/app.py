### Importamos todas las librearias necesarias para desarrollar la ApiRest ###

from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from http import HTTPStatus as http

app = Flask(__name__)                                                                               ### Instanciamos a Flask en la variable app

app.config['SQL_ALCHEMY_DATABASE_URI']='mysql+pymsql://root@127.0.0.1/flaskmysql'              ### Pasamos la configuración de donde está la base de datos a la app
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False                                               ### desactivamos los alerts que vienen por defecto

db = SQLAlchemy(app)
ma = Marshmallow(app)


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(70), unique=True)
    description = db.Column(db.String(100))

    def __init__(self, title, description):
        self.title = title
        self.description = description

db.create_all()

class TaskSchema(ma.Schema):
    class Meta:
        fields = ('id', 'title', 'description')


task_schema = TaskSchema()
tasks_schema = TaskSchema(many=True)

@app.route('/tasks', methods=['POST'])
def create_task():
  title = request.json['title']
  description = request.json['description']

  new_task= Task(title, description)

  db.session.add(new_task)
  db.session.commit()

  return task_schema.jsonify(new_task)


if __name__=='__main__':                                                                            ### Ejecutamos nuestra app con el depurador activado para poder refrescar en el momento cualquier cambio
    app.run(debug=True)