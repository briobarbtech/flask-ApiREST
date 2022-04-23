### Importamos todas las librearias necesarias para desarrollar la ApiRest ###

from pyparsing import empty
from config import config
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from http import HTTPStatus as http
from marshmallow import fields
from sqlalchemy import desc

app = Flask(__name__)                                                                               ### Instanciamos a Flask en la variable app


db = SQLAlchemy(app)                                                                                ### Le pasamos la configuración de app al ORM SQLAlchemy para que este pueda comunicarse con la db
ma = Marshmallow(app)                                                                               ### instanciamos el esquema Marshmallow y le pasamos la instancia de app 


class Task(db.Model):                                                                               ### Definimos la clase de tareas con los atributos id, titulo y descripción
    id = db.Column(db.Integer, primary_key=True)                                                    ### Definimos que le id es un entero y la llave primaria
    title= db.Column(db.String(70), unique=True)                                                    ### definimos que el titulo será un String de un max-lenght 70, y le decimos que sea unico
    description = db.Column(db.String(255))                                                         ### Definimos que la descripción de tipo String con un max-lenght 255
    
    def __init__(self,title,description):                                                           ### definimos en el constructor un init que se ejecuta cada vez que se instancia la clase
        self.title = title                                                                          ### donde definimos que el parametro title se establecera en el title
        self.description = description                                                              ### y description se agrega al atributo description

db.create_all()                                                                                     ### ejecutamos el metodo de SQLAlchemy create_all que lee toda la clase y crea todas las tablos

class TaskSchema(ma.Schema):                                                                        ### Vamos a crear un esquema que nos ayude interactuar más facilmente con la db                                                                 ### Definimos la clase Meta donde definimos los campos que vamos a querer llamar
    id = fields.Integer(dump_only=True)
    title = fields.String()
    description = fields.String()

        
task_Schema = TaskSchema()                                                                          ### instanciamos el Schema creado recientemente para poder llamar una tarea
tasks_Schema = TaskSchema(many=True)                                                                ### instanciamos el Schema creado recientemente para poder llamar todas las tareas


######################################### ACÁ EMPEZAMOS A DEFINIR LOS ENDPOINTS #########################################

### TRAER TODAS LAS TAREAS DE LA DB ###
@app.route('/tasks')                                                                                ### Establecemos la ruta para traer todas las recestas y el método HTTP con el que se va a enviar la petición
def get_tasks():                                                                                    ### Definimos la función que se va a ejecutar 
    all_tasks = Task.query.all()                                                                    ### hacemos una petición que va a serán igual a instancias de Task
    result = tasks_Schema.dump(all_tasks)                                                           ### le damos formato de esquema con Schema
    if len(all_tasks) == 0:
        return jsonify({'message': 'No hay recetas aún, crea una para verla aquí'}), http.OK        ### si la lista está vacía devolvemos un mensaje diciendo que está vacío
    return jsonify(result), http.OK                                                                 ### finalmente devolvemos cada tarea como un JSON y un status HTTP OK 200

@app.route('/tasks/<int:id_task>', methods=['GET'])                                                
def get_task(id_task):
    task = Task.query.get(id_task)                                                                  ### hacemos una petición que va a ser igual a una instancia de Task, pero, vamos a traer solo el que coincida con el campo id_task especificado
    if not task:                                                                                        ### en el caso de no encontrar la tarea, le decimos que nos devuelva un NOT_FOUND
        return jsonify({'message':'Task NOT FOUND'}), http.NOT_FOUND
    return task_Schema.jsonify(task), http.OK                                                       ### devolvemos la tarea que trajo desde la DB como un json, lo pasamos por task_schema para darle un formato reconocible para mostrar


@app.route('/tasks', methods=['POST'])                                                              
def create_task():                                                                                  
    titulo = request.json['title']                                                                  ### Traemos desde el cuerpo de la petición el título
    descripcion = request.json['description']                                                       ### y la descripción

    new_Task = Task(titulo, descripcion)                                                            ### Instanciamos la clase Task con los valores traidos desde el cuerpo de la petición

    db.session.add(new_Task)                                                                        ### usamos una función del orm (SQLAlchemy) para agregar esa nueva tarea a la base de datos
    db.session.commit()                                                                             ### para confirmar esta acción commiteamos el cambio con otra función del orm

    return task_Schema.jsonify(new_Task), http.CREATED


@app.route('/tasks/<int:id_task>', methods=['PUT'])
def update_task(id_task):

    task = Task.query.get(id_task)
    if not task:                                                                                   
        return jsonify({'message':'Task NOT FOUND'}), http.NOT_FOUND

    titulo = request.json['title']                                                                   
    descripcion = request.json['description']

    task.title = titulo                                                                             ### seteamos los valores de la tarea traida de la DB con los valores respectivos del cuerpo de la petición
    task.description = descripcion

    db.session.commit()                                                                             

    return task_Schema.jsonify(task), http.OK

@app.route('/tasks/<int:id_task>', methods=['DELETE'])
def delete_task(id_task):
    task = Task.query.get(id_task)
    if not task:
        return jsonify({'message':'Task NOT FOUND'}), http.NOT_FOUND
    db.session.delete(task)                                                                         ### usamos la función delete del orm para eliminar la tarea traida desde la DB
    db.session.commit()
    return task_Schema.jsonify(task), http.NO_CONTENT


if __name__=='__main__':                                                                            ### llamamos un objeto con las configuraciones de la app
    app.config.from_object(config['development'])
    app.run()