from main import app
from flask import render_template, request
import json
import logging
from models import Usuario, Solicitud

# Flask views
@app.route('/')
def index():
    return '<a href="/admin/">Solicitar un nuevo credito</a>'

@app.route('/_ah/warmup')
def warmup():
    #TODO: Warmup
    return 'Warming Up...'


@app.route('/registrar', methods=['GET', 'POST'])
def registrar_usuario():
    if request.method == "POST":
        json_request = request.get_json(force=True)
        logging.info(json_request)

        response = {}

        if Usuario.query(Usuario.identificacion == int(json_request['id'])).get():
            response['status'] = '403'
            response['message'] = 'El usuario ya se encuentra registrado'
        else:
            nuevo_usuario = Usuario()
            nuevo_usuario.identificacion = int(json_request['id'])
            nuevo_usuario.nombre = json_request['nombre']
            nuevo_usuario.apellido = json_request['apellido']
            nuevo_usuario.put()

            response['status'] = '200'
            response['message'] = 'El usuario fue registrado satisfactoriamente'



        return json.dumps(response)

    return "error"


@app.route('/solicitar', methods=['GET', 'POST'])
def solicitar_prestamo():
    if request.method == "POST":
        json_request = request.get_json(force=True)
        logging.info(json_request)
        response = {}

        solicitud = Solicitud()
        solicitud.id_usuario = int(json_request['id'])

        if int(json_request['salario']) > 800000:
            solicitud.status = 'APROBADO'
            if int(json_request['salario']) <= 1000000:
                solicitud.valor_aprobado = 5000000
            elif int(json_request['salario']) > 1000000 and int(json_request['salario']) < 4000000:
                solicitud.valor_aprobado = 20000000
            else:
                solicitud.valor_aprobado = 50000000
        else:
            solicitud.status = 'RECHAZADO'
            solicitud.valor_aprobado = 0

        solicitud.put()

        response['status'] = '200'
        response['status_solicitud'] = solicitud.status
        response['valor_aprobado'] = solicitud.valor_aprobado

        return json.dumps(response)

    return "error"