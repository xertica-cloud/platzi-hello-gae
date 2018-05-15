import logging
from google.appengine.ext import ndb
from endpoints_proto_datastore.ndb.model import EndpointsModel, EndpointsAliasProperty


class TodoModel(EndpointsModel):
    title = ndb.StringProperty()
    completed = ndb.BooleanProperty()

class Usuario(EndpointsModel):
    identificacion = ndb.IntegerProperty()
    nombre = ndb.StringProperty()
    apellido = ndb.StringProperty()
    email = ndb.StringProperty()

class Solicitud(EndpointsModel):
    fecha_solicitud = ndb.DateTimeProperty(auto_now=True)
    id_usuario = ndb.IntegerProperty()
    nit = ndb.IntegerProperty()
    salario = ndb.IntegerProperty()
    fecha_ingreso_compania = ndb.IntegerProperty()
    status = ndb.StringProperty()
    valor_aprobado = ndb.IntegerProperty()