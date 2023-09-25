from flask import Flask
from flask_mail import Mail, Message

app = Flask(__name__)

# Configuración de Flask-Mail
app.config['MAIL_SERVER'] = 'smtp.example.com'  # Reemplaza con tu servidor SMTP
app.config['MAIL_PORT'] = 587  # Puerto SMTP
app.config['MAIL_USERNAME'] = 'tu_correo@example.com'  # Tu correo electrónico
app.config['MAIL_PASSWORD'] = 'tu_contraseña'  # Tu contraseña de correo electrónico
app.config['MAIL_USE_TLS'] = True  # Usar TLS (True/False según corresponda)
app.config['MAIL_USE_SSL'] = False  # Usar SSL (True/False según corresponda)

mail = Mail(app)

@correo.route('/usuario')
def enviar_correo_confirmacion(correo_usuario):
    msg = Message('Confirmación de Registro', sender='tu_correo@example.com', recipients=[correo_usuario])
    msg.body = 'Gracias por registrarte en nuestra aplicación. Tu cuenta ha sido creada con éxito.'
    
    try:
        mail.send(msg)
        return True
    except Exception as e:
        print(str(e))
        return False
