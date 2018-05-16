from protorpc import messages, message_types
import endpoints

SOLICITUD_REQUEST = endpoints.ResourceContainer(
    id_usuario=messages.IntegerField(1),
    email=messages.StringField(2)
)


class SolicitudMessage(messages.Message):
    id_usuario = messages.IntegerField(1)
    status = messages.StringField(2)
    valor_aprobado = messages.IntegerField(3)
    fecha_solicitud = message_types.DateTimeField(4)


class SolicitudList(messages.Message):
    items = messages.MessageField(SolicitudMessage, 1, repeated=True)
