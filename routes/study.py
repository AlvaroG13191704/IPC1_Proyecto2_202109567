import json
from flask import Blueprint, request, jsonify, Response
from bson import json_util
from flask_pymongo import PyMongo
from datetime import datetime, timedelta
import time
import app

Study=Blueprint("study",__name__)

#Ver cuartos disponibles
@Study.route("/study", methods = ['GET'])
def study():
    #Iniciar mongo
    mongo = PyMongo(app.app) 
    #Mostrar cuartos
    cuartos = mongo.db.rooms.find()
    response = json_util.dumps(cuartos)
    return Response(response, mimetype='application/json'), 200 

#Reservar un cuarto
@Study.route("/study/rent", methods = ['POST'])
def rent():
    #Iniciar mongo
    mongo = PyMongo(app.app)
    #Recibir id y fecha 
    id_room = request.json["id_room"]
    dateToUse = request.json["fecha_de_uso"]
    #Agregar función que cuando vea que la fecha de retorno es igual a la de hoy, entonces que la elimine
    room = mongo.db.rooms.find_one({"id_room": id_room})
    datenow = str(datetime.now().strftime("%d/%m/%Y"))
    fecha_actual = time.strptime(datenow, "%d/%m/%Y")
    fecha_retorno = time.strptime(room["return_date"], "%d/%m/%Y")
    if fecha_actual > fecha_retorno and room["return_date"]:
        print("Ya se paso la fecha")
        #Entonces eliminar retorno 
        mongo.db.rooms.update_one({"id_room":room["id_room"]},{
            '$set': {
                'id_room': id_room,
                'available': 'YES',
                'not_availabe': 'NO',
                'return_date': ""
            }
        })
    else:
        print("No se ha pasado")
    #Funcion
    if id_room and dateToUse:
        #Revisar que sea el id correcto
        if mongo.db.rooms.find_one({"id_room": id_room}):
            #Traer el cuarto
            room = mongo.db.rooms.find_one({"id_room": id_room})
            #Ver que no este ocupado
            if 'YES' == room['not_availabe']:
                #Si es igual entonces no se puede reservar el cuarto
                return jsonify({"msg":"Cuarto ocupado"})
            #Sino esta ocupado entonces reservar con fecha y actualizar 
            mongo.db.rooms.update_one({"id_room":id_room},{
                '$set':{
                    'id_room': id_room,
                    'available': 'NO',
                    'not_availabe': 'YES',
                    'return_date': dateToUse
                }
                
            })
            return jsonify({
                'AVISO CUARTO RESERVADO': 'Cuarto reservado'
            })
        return jsonify({"msg":"id incorrecto"})
    return jsonify({"msg":"Valores insuficientes"})

