#Imports
from flask import  request, jsonify, Response, Blueprint
from bson import json_util
from flask_pymongo import PyMongo
import app

biblioteca=Blueprint("biblioteca",__name__)


#--------------------LIBRO------------------------------#
#VER LIBRO
@biblioteca.route("/get_book", methods = ['GET', 'POST'])	
def get_book():
    #Iinciar mongo
    mongo = PyMongo(app.app)
    
    list_book = request.get_json()
    #Recibir datos
    id_book = None
    if "id_book" in list_book:
        id_book = list_book["id_book"]
    book_title = None
    if "book_title" in list_book:
        book_title = list_book["book_title"]
    book_type = None
    if "book_type" in list_book:
        book_type = list_book["book_type"]
    #Combinaciones
    if id_book and book_title and book_type:
        book = mongo.db.biblioteca.find_one({"id_book": id_book, "book_title": book_title, "book_type": book_type})
        response = json_util.dumps(book)
        return Response(response, mimetype='application/json'), 200
    elif id_book and book_title:
        book = mongo.db.biblioteca.find({"id_book": id_book, "book_title": book_title})
        response = json_util.dumps(book)
        return Response(response, mimetype='application/json'), 200
    elif id_book and book_type:
        book = mongo.db.biblioteca.find({"id_book": id_book, "book_type": book_type})
        response = json_util.dumps(book)
        return Response(response, mimetype='application/json'), 200
    elif book_title and book_type:
        book = mongo.db.biblioteca.find({"book_title": book_title, "book_type": book_type})
        response = json_util.dumps(book)
        return Response(response, mimetype='application/json'), 200
    elif id_book:
        if mongo.db.biblioteca.find({"id_book": id_book}):
            book = mongo.db.biblioteca.find_one({"id_book": id_book})
            response = json_util.dumps(book)
            return Response(response, mimetype='application/json'), 200
        else:
            return jsonify({'msg': 'Libro no registrado'}), 400
    elif book_title:
        book = mongo.db.biblioteca.find({"book_title": book_title})
        response = json_util.dumps(book)
        return Response(response, mimetype='application/json'), 200
    elif book_type:
        book = mongo.db.biblioteca.find({"book_type": book_type})
        response = json_util.dumps(book)
        return Response(response, mimetype='application/json'), 200
    else:
        return jsonify({'msg': 'El libro no existe'}), 400
 
#CREAR LIBRO
@biblioteca.route('/book',methods=['POST'])
def create_book():
    #Iinciar mongo
    mongo = PyMongo(app.app)
    #Recibir los datos
    id_book = request.json["id_book"]
    book_title = request.json["book_title"]
    book_type = request.json["book_type"]
    author = request.json["author"]
    book_count = request.json["book_count"]
    book_available = request.json["book_available"]
    book_not_available = request.json["book_not_available"]
    book_year = request.json["book_year"]
    book_editorial = request.json["book_editorial"]

    #Verificar que el ID no este repetido
    if id_book and book_title and book_type and author and book_count and book_available and book_year and book_editorial:
        if mongo.db.biblioteca.find_one({"id_book":id_book}):
            return jsonify({'msg': 'El id_book ya existe'}), 400
        else:
            mongo.db.biblioteca.insert_one({
                "id_book": id_book,
                "book_title": book_title,
                "book_type": book_type,
                "author": author,
                "book_count": book_count,
                "book_available": book_available,
                "book_not_available": book_not_available,
                "book_year": book_year,
                "book_editorial": book_editorial
            })
        response = jsonify({"status": 200, "msg": "response"})
        response.status_code = 200
        return response
    else: 
        response = jsonify({"status": 400, "msg": "Datos insuficientes"})
        response.status_code = 400
        return response
#Actualizar libro
@biblioteca.route('/book',methods=['PUT'])
def book_update():
    #Iinciar mongo
    mongo = PyMongo(app.app)
    #Recibir los datos
    id_book = request.json["id_book"]
    book_title = request.json["book_title"]
    book_type = request.json["book_type"]
    author = request.json["author"]
    book_count = request.json["book_count"]
    book_available = request.json["book_available"]
    book_not_available = request.json["book_not_available"]
    book_year = request.json["book_year"]
    book_editorial = request.json["book_editorial"]
    #Verificar que el ID exista
    
    if mongo.db.biblioteca.find_one({'id_book':id_book}):
        mongo.db.biblioteca.update_one({'id_book':id_book},{
            '$set':{
                "book_title": book_title,
                "book_type": book_type,
                "author": author,
                "book_count": book_count,
                "book_available": book_available,
                "book_not_available": book_not_available,
                "book_year": book_year,
                "book_editorial": book_editorial
            }
        })
        response = jsonify({"status": 200, "msg": "response"})
        response.status_code = 200
        return response
    else: 
        return jsonify({'msg': 'El id_book no existe'}), 400
# #--------------------ENDLIBRO--------------------------#  

"""
#Registrar un libro
    {
        "id_book":"asdf2",
        "book_title":"Titulo del libro",
        "book_type":"Tipo de libro",
        "author":"USAC",
        "book_count":140,
        "book_available":20,
        "book_not_available":2,
        "book_year": 2021,
        "book_editorial":"Universidad de San Carlos"
    }
#Actualizar un libro
    {
        "id_book":"asdf2",
        "book_title":"Titulo del libro",
        "book_type":"Tipo de libro",
        "author":"USAC",
        "book_count":140,
        "book_available":20,
        "book_not_available":2,
        "book_year": 2021,
        "book_editorial":"Universidad de San Carlos"
    }
"Buscar libro
    {
        "id_book":"asdf2",
        "book_title":"Titulo del libro",
        "book_type":"Tipo de libro",
    }
"""