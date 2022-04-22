### Importamos todas las librearias necesarias para desarrollar la ApiRest ###

from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from http import HTTPStatus as http
from marshmallow import fields

app = Flask(__name__)                                                                               ### Instanciamos a Flask en la variable app

app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://root@localhost/flaskmysql'                   ### Pasamos la configuración de donde está la base de datos a la app
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False                                               ### desactivamos los alerts que vienen por defecto

db = SQLAlchemy(app)                                                                                ### Le pasamos la configuración de app al ORM SQLAlchemy para que este pueda comunicarse con la db
ma = Marshmallow(app)                                                                               ###  instanciamos el scheme Marshmallow y le pasamos la instancia de app 


class Task(db.Model):                                                                               ### Definimos la clase de tareas con los atributos id, titulo y descripción
    id = db.Column(db.Integer, primary_key=True)                                                    ### Definimos que le id es un entero y la llave primaria
    title= db.Column(db.String(70), unique=True)                                                    ### definimos que el titulo será un String de un max-lenght 70, y le decimos que sea unico
    description = db.Column(db.String(255))                                                         ### Definimos que la descripción de tipo String con un max-lenght 255
    
    def __init__(self,title,description):                                                           ### definimos en el constructor un init que se ejecuta cada vez que se instancia la clase
        self.title = title                                                                          ### donde definimos que el parametro title se establecera en el title
        self.description = description                                                              ### y description se agrega al atributo description

db.create_all()                                                                                     ### ejecutamos el metodo de SQLAlchemy create_all que lee toda la clase y crea todas las tablos

class TaskSchema(ma.Schema):                                                                        ### Vamos a crear un schema que nos ayude interactuar más facilmente con la db                                                                 ### Definimos la clase Meta donde definimos los campos que vamos a querer llamar
    id = fields.Integer(dump_only=True)
    title = fields.String()
    description = fields.String()

        
task_Schema = TaskSchema()                                                                          ### instanciamos el Schema creado recientemente para poder llamar una tarea
tasks_Schema = TaskSchema(many=True)                                                                ### instanciamos el Schema creado recientemente para poder llamar todas las tareas

@app.route('/tasks', methods=['POST'])                                                              ### Establecemos la ruta para postear una tarea y el método HTTP con el que se va a enviar la petición
def create_task():                                                                                  ### Definimos la función que se va a ejecutar 
                                                                                                    ### Mostramos en la consola la respuesta que nos devuelve el servidor                                                      ### y mostramos un mensaje custom de 'received'
    titulo = request.json['title']                                                                   ### y mostramos un mensaje custom de 'received'
    descripcion = request.json['description']

    new_Task = Task(titulo, descripcion)

    db.session.add(new_Task)
    db.session.commit()

    return task_Schema.jsonify(new_Task)
if __name__=='__main__':                                                                            ### Ejecutamos nuestra app con el depurador activado para poder refrescar en el momento cualquier cambio
    app.run(debug=True)