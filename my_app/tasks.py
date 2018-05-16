from google.appengine.api import mail


def enviar_email(subject, destiny, body):
    message = mail.EmailMessage(
        sender='adriana.moya@ubate.org',
        subject=subject
    )

    message.to = destiny
    message.body = body

    message.send()

