import logging
from google.appengine.ext import endpoints
from protorpc import remote
from my_app.models import TodoModel
from my_app.models import Solicitud

from api_messages import SOLICITUD_REQUEST, SolicitudMessage, SolicitudList

@endpoints.api(
    name='solicitudesApi', title='solicitudesApi',version='v1', description=''
)
class SolicitudesAPI(remote.Service):

    @endpoints.method(
        SOLICITUD_REQUEST, SolicitudList,
        path='listar_solicitudes',
        name='listar_solicitudes',
        http_method='GET'
    )
    def listar_solicitudes(self, request):

        listado = []
        solicitudes_usuario = Solicitud.listar_solicitudes_usuario(id=request.id)

        for item in solicitudes_usuario:
            entidad = SolicitudMessage(
                id_usuario=request.id_usuario,
                status=item.status,
                valor_aprobado=item.valor_aprobado,
                fecha_solicitud=item.fecha_solicitud
            )
            listado.append(entidad)

        return SolicitudList(items=listado)

    @Solicitud.method(
        path='insertar_solicitud',
        name='insertar_solicitud',
        http_method='POST'
    )
    def insertar_solicitud(self, solicitud_entity):
        solicitud_entity.put().get()
        logging.info("Se inserto la entidad")
        return solicitud_entity

    @Solicitud.query_method(
        path='listar_solicitudes_simple',
        name='listar_solicitudes_simple',
        query_fields=('id_usuario','limit', 'order', 'pageToken')
    )
    def listar_por_usuario_simple(self, query):
        return query
