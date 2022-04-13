
import json
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, Response, Blueprint
from bson import json_util
import uuid
from datetime import datetime, timedelta
from flask_pymongo import PyMongo

import app

prestamo=Blueprint("prestamo",__name__)
#----------------------PRESTAMOS---------------------------#
@prestamo.route('/loan',methods = ['GET','POST'])
def loan():
    if request.method == 'GET':
        mongo = PyMongo(app.app)
        loanList = request.get_json()
        print(loanList)
        #Recibir datos
        id_loan = None
        if "id_loan" in loanList:
            id_loan = loanList["id_loan"]
            if mongo.db.prestamos.find({"id_loan": id_loan}):
                loan = mongo.db.prestamo.find_one({"id_loan": id_loan})
                return jsonify({
                    "id_loan": loan["id_loan"],
                    "id_book": loan["id_book"],
                    "loan_date": loan["loan_date"],
                    "return_date": loan["return_date"],
                    "id_user": loan["id_user"],
                }),200
            else:
                return jsonify({'msg': 'Prestamo no registrado'}), 400
        else:
            return jsonify({'msg': 'No se recibieron datos'}), 400

    elif request.method == 'POST':
        #inciar mongo
        mongo = PyMongo(app.app)
        #Recibir datos
        id_book = request.json['id_book']
        id_user = request.json['id_user']
        #Verificar que existan en la base de datos
        if mongo.db.users.find({"id_user":id_user}) and mongo.db.biblioteca.find({'id_book':id_book}):
            #Traer el el usuario y libro
            user = mongo.db.users.find_one({"id_user":id_user})
            id_user = user['id_user']
            user_display_name = user['user_display_name']
            user_career = user['user_career']
            user_carnet = user['user_carnet']
            book = mongo.db.biblioteca.find_one({"id_book":id_book})
            id_book = book['id_book']
            book_title = book['book_title']
            book_type = book['book_type']
            author = book['author']
            book_year = book['book_year']
            book_editorial = book['book_editorial']
            #Fechas
            loan_date = datetime.now().strftime("%d/%m/%Y")
            return_date = (datetime.now() + timedelta(days=7)).strftime("%d/%m/%Y")
            id_loan = str(uuid.uuid4())
            #Crear prestamo
            mongo.db.prestamo.insert_one({
                "id_loan": id_loan,
                "id_book": id_book,
                "book_title": book_title,
                "book_type": book_type,
                "author": author,
                "book_year": book_year,
                "book_editorial": book_editorial,
                #Fechas
                "loan_date": str(loan_date),
                "return_date": str(return_date),
                "id_user": id_user,
                "user_display_name": user_display_name,
                "user_career": user_career,
                "user_carnet": user_carnet,
            })
            #Retornar prestamo
            response = json_util.dumps(mongo.db.prestamo.find_one({"id_loan": id_loan }))
            return Response(response, mimetype='application/json')
        else:
            return jsonify({"message":"No existe el usuario o libro"}),400
            
            
        
#Calcular multa
@prestamo.route('/loan/penalty',methods = ['GET','POST'])
def penalty():
    if request.method == 'POST':
        #Inicar base
        mongo = PyMongo(app.app)
        #Recibir datos
        id_loan = request.json['id_loan']  
        #Verificar que exista en la base de datos
        if mongo.db.prestamo.find({"id_loan":id_loan}):
            #Traer prestamo
            loan = mongo.db.prestamo.find_one({"id_loan":id_loan})
            #Fechas
            loan_date = datetime.strptime(loan['loan_date'], '%d/%m/%Y')
            return_date = datetime.strptime(loan['return_date'], '%d/%m/%Y')
            #Calcular multa
            if return_date < datetime.now():
                multa = (datetime.now() - return_date).days * 2
                #Actualizar prestamo
                mongo.db.prestamo.update_one({"id_loan":id_loan},{
                    "$set":{"penalty_fee":multa}
                })
                #Retornar prestamo
                response = json_util.dumps(mongo.db.prestamo.find_one({"id_loan": id_loan }))
                return Response(response, mimetype='application/json')
            else:
                return jsonify({"message":"Prestamo vigente"}),400
        else:
            return jsonify({"message":"No existe el prestamo"}),400








#----------------------ENDPRESTAMOS---------------------------#