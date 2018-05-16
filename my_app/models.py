import logging
from google.appengine.ext import ndb
from endpoints_proto_datastore.ndb.model import EndpointsModel, EndpointsAliasProperty

# TODO: Remove
class TodoModel(EndpointsModel):
    title = ndb.StringProperty()
    completed = ndb.BooleanProperty()


class Usuario(EndpointsModel):

    identificacion = ndb.IntegerProperty(indexed=True)
    nombre = ndb.StringProperty()
    apellido = ndb.StringProperty()
    email = ndb.StringProperty(indexed=True)

    @staticmethod
    def obtener_usuario_por_id(id):
        result = Usuario.query(Usuario.identificacion == id).get()
        return result

    @staticmethod
    def registrar_nuevo_usuario(identificacion, nombre, apellido, email):
        return Usuario(
            identificacion=identificacion,
            nombre=nombre,
            apellido=apellido,
            email=email
        ).put().get()


class Solicitud(EndpointsModel):
    fecha_solicitud = ndb.DateTimeProperty(auto_now=True)
    id_usuario = ndb.IntegerProperty()
    nit = ndb.IntegerProperty()
    salario = ndb.IntegerProperty()
    fecha_ingreso_compania = ndb.IntegerProperty()
    status = ndb.StringProperty()
    valor_aprobado = ndb.IntegerProperty()


    @staticmethod
    def consultar_ultimas_solicitudes():
        solicitudes = Solicitud.query().order(-Solicitud.fecha_solicitud).fetch(5)
        return solicitudes

    @staticmethod
    def registrar_solicitud(id_usuario, nit, salario, status, valor_aprobado):
        return Solicitud(
            id_usuario=id_usuario,
            nit=nit,
            salario=salario,
            status=status,
            valor_aprobado=valor_aprobado
        ).put().get()

    @staticmethod
    def listar_solicitudes_usuario(id):
        solicitudes = Solicitud.query(Solicitud.id_usuario == id).fetch()
        return solicitudes