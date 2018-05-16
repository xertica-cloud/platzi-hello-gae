from main import app
from flask import render_template, request
import json
import logging
from models import Usuario, Solicitud
from google.appengine.api import mail

# Flask views
@app.route('/')
def index():
    return '<a href="/admin/">Solicitar un nuevo credito</a>'


@app.route('/registrar', methods=['GET', 'POST'])
def registrar_usuario():
    if request.method == "POST":
        json_request = request.get_json(force=True)
        logging.info(json_request)

        response = {}

        # Consultar usuario por identificacion
        usuario = Usuario.obtener_usuario_por_id(int(json_request['id']))

        if usuario:
            response['status'] = '403'
            response['message'] = 'El usuario ya se encuentra registrado'
        else:
            # Registrar usuario en datastore
            nuevo_usuario = Usuario.registrar_nuevo_usuario(
                identificacion=int(json_request['id']),
                nombre=json_request['nombre'],
                apellido=json_request['apellido']
            )

            response['status'] = '200'
            response['message'] = 'El usuario fue registrado satisfactoriamente'

        # Retornar respuesta
        return json.dumps(response)

    return "error"


@app.route('/solicitar', methods=['GET', 'POST'])
def solicitar_prestamo():
    if request.method == "POST":
        json_request = request.get_json(force=True)
        logging.info(json_request)
        response = {}

        status = ''
        valor_aprobado = 0

        if int(json_request['salario']) > 800000:
            status = 'APROBADO'
            if int(json_request['salario']) <= 1000000:
                valor_aprobado = 5000000
            elif int(json_request['salario']) > 1000000 and int(json_request['salario']) < 4000000:
                valor_aprobado = 20000000
            else:
                valor_aprobado = 50000000
        else:
            status = 'RECHAZADO'
            valor_aprobado = 0

        solicitud = Solicitud.registrar_solicitud(
            id_usuario=int(json_request['id']),
            salario=int(json_request['salario']),
            status=status,
            valor_aprobado=valor_aprobado
        )

        response['status'] = '200'
        response['status_solicitud'] = status
        response['valor_aprobado'] = valor_aprobado

        return json.dumps(response)

    return "error"


@app.route('/entregar_reporte')
def entregar_reporte():
    message = mail.EmailMessage(
        sender="adriana.moya@ubate.org",
        subject="Your account has been approved")

    message.to = "Albert Johnson <Albert.Johnson@example.com>"
    message.body = """Dear Albert:"""

    message.send()

    return True