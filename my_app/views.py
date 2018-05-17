from main import app
from flask import render_template, request
import json
import logging
from models import Usuario, Solicitud
from google.appengine.api import mail
from tasks import enviar_email
from google.appengine.ext import deferred
from helpers import CloudStorageHelper


BUCKET = 'platzi-test-001.appspot.com'
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
                apellido=json_request['apellido'],
                email=json_request['email']
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
            nit=int(json_request['nit']),
            valor_aprobado=valor_aprobado
        )

        response['status'] = '200'
        response['status_solicitud'] = status
        response['valor_aprobado'] = valor_aprobado

        return json.dumps(response)

    return "error"


@app.route('/entregar_email')
def entregar_email():
    message = mail.EmailMessage(
        sender="adriana.moya@ubate.org",
        subject="Your account has been approved")

    message.to = "Albert Johnson <Albert.Johnson@example.com>"
    message.body = """Dear Albert:"""

    message.send()

    return True


@app.route('/entregar_reporte')
def entregar_reporte():
    solicitudes = Solicitud.consultar_ultimas_solicitudes()

    for solicitud in solicitudes:
        usuario = Usuario.obtener_usuario_por_id(solicitud.id_usuario)

        body = 'Le fue aprobado un prestamo por el valor de ' + str(solicitud.valor_aprobado)

        deferred.defer(enviar_email,
                       subject='Detalle solicitud de prestamo',
                       destiny=usuario.email,
                       body=body,
                       _queue='mail-queue'
        )

    return "Reportes entregados"

@app.route('/lista_de_objetos')
def listar_objetos():

    gcs = CloudStorageHelper()
    archivos_disponibles = gcs.list_buckets()

    response = {}
    links = []

    for item in archivos_disponibles:
        name_file = 'https://' + BUCKET + '/' + item['name']
        links.append(name_file)

    return "Archivos"


@app.route('/listar_documentos', methods=['GET', 'POST'])
def solicitar_documentos():
    gcs = CloudStorageHelper()
    archivos_disponibles = gcs.list_buckets()

    response = {}
    links = []


    for item in archivos_disponibles:
        name_file = 'https://storage.googleapis.com/' + BUCKET + '/' + item['name']
        object = {
            'name': item['name'],
            'link': name_file
        }
        links.append(object)


    response['status'] = '200'
    response['total_archivos'] = len(archivos_disponibles)
    response['items'] = links


    return json.dumps(response)