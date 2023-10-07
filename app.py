from flask import Flask, url_for, render_template, redirect, request, Response, session
import os
from flask_mysqldb import MySQL, MySQLdb
from werkzeug.utils import secure_filename
import mysql.connector
from mysql.connector import IntegrityError
from flask_socketio import SocketIO, emit


app = Flask(__name__, template_folder="Template", static_url_path='/static')
socketio = SocketIO(app)

# -------- Conexion a bases de datos ------------
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'tg_prime'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql = MySQL(app)
# ----------------------------------------------


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/admin')
def admin():
    return render_template('admin.html')

# ------------------ Login  -----------------


@app.route('/acceso_login', methods=["GET", "POST"])
def login():
    if request.method == 'POST' and 'USER' in request.form and 'CLAVE':
        _correo = request.form['USER']
        _clave = request.form['CLAVE']

        cur = mysql.connection.cursor()
        cur.execute(
            'SELECT ID, Nombre, Apellido,id_Programa, id_rol FROM tb_usuarios WHERE Email_Usa = %s AND Contrasena = %s', (_correo, _clave,))
        account = cur.fetchone()

        if account:
            session['logeado'] = True
            session['ID'] = account['ID']
            session['id_rol'] = account['id_rol']
            session['id_Programa'] = account['id_Programa']
            session['user_name'] = f"{account['Nombre']} {account['Apellido']}"

            if session['id_rol'] == 1:
                return render_template("admin.html")
            elif session['id_rol'] == 2:
                return render_template("menu.html")

            return render_template("admin.html")
        else:
            return render_template("index.html", mensaje="Usuario o contraseña Incorrecta")


@app.route('/logout')
def logout():
    # Elimina las variables de sesión para cerrar la sesión del usuario
    session.pop('logeado', None)
    session.pop('ID', None)
    session.pop('id_rol', None)
    session.pop('user_name', None)
    # Redirige al usuario a la página de inicio de sesión o a donde desees
    return render_template('index.html')

# ------------------------------------------------------------------

# -------------------- Registrar nuevo Usuario----------------------


@app.route('/registro')
def registro():
    return render_template('user/crear_usuario.html')


@app.route('/crear_registro', methods=["GET", "POST"])
def crear_registro():
    nombre = request.form['NombreC']
    apellido = request.form['Apellido']
    correoUsa = request.form['CorreoUSA']
    correo = request.form['CorreoA']
    telefono = request.form['telefono']
    contrasena = request.form['contrasena']

    if not nombre or not apellido or not correoUsa or not correo or not telefono or not contrasena:
        return render_template("user/crear_usuario.html", mensaje3="Todos los campos son obligatorios")

    cur = mysql.connection.cursor()
    cur.execute('INSERT INTO tb_usuarios (Nombre,Apellido, Email_Usa, Email_alterno, Telefono, id_Programa, id_rol, Contrasena) VALUES (%s,%s, %s, %s, %s, %s, %s, %s)',
                (nombre, apellido, correoUsa, correo, telefono, "2", "3", contrasena))

    mysql.connection.commit()

    return render_template("user/crear_usuario.html", mensaje2="Usuario Registrado Exitosamente")


@app.route('/modificar/<int:id>', methods=['GET', 'POST'])
def modificar_usuario(id):
    # Recupera el usuario con el ID proporcionado desde la base de datos.
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM tb_usuarios WHERE ID = %s', (id,))
    usuario = cur.fetchone()
    cur.close()

    if request.method == 'POST':
        # Obtén los datos del formulario de edición.
        nombre = request.form['NombreC']
        apellido = request.form['Apellido']
        correoUsa = request.form['CorreoUSA']
        correo = request.form['CorreoA']
        telefono = request.form['telefono']
        contrasena = request.form['contrasena']

        print("Valores del formulario:")
        print(f"ID: {id}")
        print(f"Nombre: {nombre}")
        print(f"Apellido: {apellido}")
        print(f"Correo USA: {correoUsa}")
        print(f"Correo Alterno: {correo}")
        print(f"Teléfono: {telefono}")
        print(f"Contraseña: {contrasena}")

        # Actualiza los datos del usuario en la base de datos.
        cur = mysql.connection.cursor()
        cur.execute('UPDATE tb_usuarios SET Nombre=%s, Apellido=%s, Email_Usa=%s, Email_alterno=%s, Telefono=%s, Contrasena=%s WHERE ID=%s',
                    (nombre, apellido, correoUsa, correo, telefono, contrasena, id))
        mysql.connection.commit()
        cur.close()

        print("Datos actualizados correctamente")

        # Redirige a alguna página de confirmación o a donde desees después de la edición.
        return render_template('user/lista_usuarios.html', mensaje="Se actualizo correctamente")

    return render_template('user/modificar_usuario.html', usuario=usuario)


@app.route('/formulario', methods=['GET'])
def formulario():
    cur = mysql.connection.cursor()

    # Obtén los datos de la tabla programas
    cur.execute('SELECT id_programa, descripcion FROM programas')
    opciones = cur.fetchall()

    cur.close()

    print(opciones)  # Agrega esto para depuración

    return render_template('user/crear_usuario.html', opciones=opciones)


@app.route('/crear_registroLo', methods=["POST"])
def crear_registroLo():
    # Obtén los valores del formulario
    nombre = request.form['NombreC']
    apellido = request.form['Apellido']
    correoUsa = request.form['CorreoUSA']
    correo = request.form['CorreoA']
    telefono = request.form['telefono']
    contrasena = request.form['contrasena']

    # Comprueba si alguno de los campos está vacío
    if not nombre or not apellido or not correoUsa or not correo or not telefono or not contrasena:
        return render_template("index.html", mensaje3="Todos los campos son obligatorios")

    # Si todos los campos están completos, procede con la inserción en la base de datos
    cur = mysql.connection.cursor()
    cur.execute('INSERT INTO tb_usuarios (Nombre, Apellido, Email_Usa, Email_alterno, Telefono, id_Programa, id_rol, Contrasena) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)',
                (nombre, apellido, correoUsa, correo, telefono, "2", "3", contrasena))

    mysql.connection.commit()

    return render_template("index.html", mensaje2="Usuario Registrado Exitosamente")


# -----------------------------------------------------------------------------------------------------------------------


@app.route('/modificar')
def modificar():
    return render_template('user/modificar_usuario.html')


@app.route('/eliminar')
def eliminar():
    return render_template('user/eliminar_usuario.html')


@app.route('/lista', methods=["GET", "POST"])
def lista():
    cur = mysql.connection.cursor()

    # Realiza una consulta SQL que une las tablas tb_usuarios y programas en función de id_Programa
    cur.execute("SELECT u.ID, u.Nombre,u.Apellido, u.Email_Usa, u.Email_alterno, u.Telefono, p.descripcion \
                 FROM tb_usuarios u \
                 JOIN programas p ON u.id_Programa = p.id_Programa")

    usuarios = cur.fetchall()
    cur.close()

    return render_template('user/lista_usuarios.html', usuarios=usuarios)



# ------------------------- Cargar Trabajos ------------------------------------------
@app.route('/cargarT')
def cargarT():
    return render_template('trabajo/CargarT.html')

app.config['UPLOAD_FOLDER'] = os.path.abspath('GP_Usa\\static\\assets\\pdf')

@app.route('/crear_trabajo', methods=['POST'])
def crear_trabajo():
    
    nombre_trabajo = request.form['NombreTrabajo']
    tipo_trabajo = request.form['TipoTrabajo']
    observacion = request.form['Observaciones']
    id_usuario = session['ID']
    id_programa = session['id_Programa']  # Obtén el ID del programa del estudiante
    cur = mysql.connection.cursor()

    # Verifica si se ha enviado un archivo PDF
    if 'pdf' in request.files:
        pdf = request.files['pdf']

        # Verifica si el archivo tiene una extensión válida
        if pdf.filename != '' and pdf.filename.endswith('.pdf'):
            # Genera un nombre de archivo seguro
            filename = secure_filename(pdf.filename)
            # Guarda el archivo PDF en la carpeta configurada
            pdf.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            # Intenta insertar el trabajo en la base de datos
            try:
                sql = "INSERT INTO trabajos (id_estudiante, id_programa, Nombre_trabajo, tipo_trabajo, adjunto, observaciones) VALUES (%s, %s, %s, %s, %s, %s)"
                val = (id_usuario, id_programa, nombre_trabajo, tipo_trabajo, filename, observacion)
                cur.execute(sql, val)
                mysql.connection.commit()
                cur.close()

                return render_template('trabajo/CargarT.html', mensaje1="Se cargo correctamente.")
            except MySQLdb.IntegrityError as e:
                return render_template('trabajo/CargarT.html', mensaje2="Ya existe registro.")

    return render_template('trabajo/CargarT.html', mensaje2="Error al cargar el archivo PDF o el formato no es válido.")


@app.route('/eliminarT')
def eliminarT():
    return render_template('trabajo/EliminarT.html')


@app.route('/modificar_trabajo/<int:id>', methods=['GET', 'POST'])
def modificar_trabajo(id):
    if request.method == 'POST':
        # Obtén los nuevos datos del formulario de modificación.
        nuevo_nombre_trabajo = request.form['NuevoNombreTrabajo']
        nuevo_tipo_trabajo = request.form['NuevoTipoTrabajo']
        nueva_observacion = request.form['NuevasObservaciones']

        cur = mysql.connection.cursor()

        # Verifica si se ha enviado un archivo PDF
        if 'nuevo_pdf' in request.files:
            nuevo_pdf = request.files['nuevo_pdf']

            # Verifica si el archivo tiene una extensión válida
            if nuevo_pdf.filename != '' and nuevo_pdf.filename.endswith('.pdf'):
                # Genera un nombre de archivo seguro
                nuevo_filename = secure_filename(nuevo_pdf.filename)
                # Guarda el nuevo archivo PDF en la carpeta configurada
                nuevo_pdf.save(os.path.join(app.config['UPLOAD_FOLDER'], nuevo_filename))

                # Intenta actualizar los datos del trabajo en la base de datos
                try:
                    sql = "UPDATE trabajos SET Nombre_trabajo = %s, tipo_trabajo = %s, adjunto = %s, observaciones = %s WHERE id = %s"
                    valores = (nuevo_nombre_trabajo, nuevo_tipo_trabajo, nuevo_filename, nueva_observacion, id)
                    cur.execute(sql, valores)
                    mysql.connection.commit()
                    cur.close()

                    return render_template('trabajo/ModificarT.html', mensaje1="Se modificó correctamente.")
                except MySQLdb.IntegrityError as e:
                    return render_template('trabajo/ModificarT.html', mensaje2="Error al modificar el trabajo.")


    # Recupera los datos actuales del trabajo para mostrarlos en el formulario de modificación.
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM trabajos WHERE id = %s', (id,))
    trabajo = cur.fetchone()
    cur.close()

    return render_template('trabajo/ModificarT.html', trabajo=trabajo)

# -------------------------------------
# ------------------- Nombre Usuario --------------


@app.route('/usuario')
def usuario():
    return render_template('trabajo/ModificarT.html')
# -------------------------------------
# ----------- Opciones ---------------


@app.route('/ActualizarD')
def ActualizarD():
    return render_template('opciones/ActualizarD.html')


@app.route('/InformacionU')
def InformacionU():
    return render_template('opciones/InformacionU.html')


@app.route('/CambioClave')
def CambioClave():
    return render_template('opciones/CambioClave.html')
# -------------------------------------
# ---------------Director---------------------


@app.route('/lista_trabajos')
def lista_trabajos():
    
    cur = mysql.connection.cursor()

    # Realiza una consulta SQL que une las tablas tb_usuarios y programas en función de id_Programa
    cur.execute("SELECT t.id, t.Nombre_trabajo, u.Nombre, u.Apellido, u.Email_Usa, u.Email_alterno, u.Telefono, p.descripcion \
             FROM trabajos t \
             JOIN tb_usuarios u ON t.id_estudiante = u.ID \
             JOIN programas p ON u.id_Programa = p.id_Programa")


    trabajos = cur.fetchall()
    cur.close()

    return render_template('user/lista_usuarios.html', trabajos=trabajos)

@app.route('/listaTutor', methods=["GET", "POST"])
def listaTutor():

    cur = mysql.connection.cursor()

    # Realiza una consulta SQL que une las tablas tb_usuarios y programas en función de id_Programa
    cur.execute("SELECT u.id, u.Nombre,u.Apellido, u.Correo, u.Telefono, p.Rol, u.Especialidad \
                 FROM administrativos u \
                 JOIN programas p ON u.id_Programa = p.id_Programa")

    usuarios = cur.fetchall()
    cur.close()

    return render_template('director/listaTutor.html', usuarios=usuarios)
# ------------------- Ayuda ----------------


@app.route('/contacto')
def contacto():
    return render_template('ayuda/contacto.html')

#------------------------- TUTOR --------------------------------

@app.route('/listaTutorias')
def listaTutorias():
    return render_template('tutor/tutoria.html')


#------------------chat --------------------- 

@app.route('/chat')
def chat():
    return render_template('chat/index.html')

@socketio.on('joined')
def handle_joined(data):
    emit('message', { 'message': 'Un usuario se ha unido al chat.' }, broadcast=True)

@socketio.on('send_message')
def handle_message(data):
    emit('message', { 'message': data['message'] }, broadcast=True)


# ------------------- Jurado ---------------------

@app.route('/jurado')
def jurado():
    return render_template('jurado/calificacion.html')


if __name__ == '__main__':
    app.secret_key = "julian"
    app.run(debug=True, host='0.0.0.0', port=5000, threaded=True)


