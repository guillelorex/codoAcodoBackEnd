# Instalar con pip install Flask IMPORTANTE ISTALAR EN BASH ESTAS COSAS
from flask import Flask, request, jsonify, render_template
# Instalar con pip install flask-cors
from flask_cors import CORS
# Instalar con pip install mysql-connector-python
import mysql.connector
# Si es necesario, pip install Werkzeug
from werkzeug.utils import secure_filename

import os
import time

app = Flask(__name__)
CORS(app)

@app.route('/')
def hello():
    return 'gola soy una pagina'

# Creo la BD------------------------------------------
class Pedido:
    def __init__(self, host, user, password, database):
        self.conn = mysql.connector.connect(
            host= host,
            user=user,
            password=password
        )
        self.cursor = self.conn.cursor()

        try:
            self.cursor.execute(f"USE {database}")
        except mysql.connector.Error as err:
            if err.errno == mysql.connector.errorcode.ER_BAD_DB_ERROR:
                self.cursor.execute(f"CREATE DATABASE {database}")
                self.conn.database = database
            else:
                raise err
 #--------------------------------------------------------------------
    # Creo las tablas----------------------------------------------------

        self.cursor.execute('''CREATE TABLE IF NOT EXISTS bebidas (
            idBebida INT primary key NOT NULL,
            nombre VARCHAR(50) NOT NULL,
            precio DECIMAL(10, 2) NOT NULL,
            imagen VARCHAR(200))
                            ''')
        self.conn.commit()

        self.cursor.execute('''CREATE TABLE IF NOT EXISTS platillos (
            idPlatillo INT primary key NOT NULL,
            nombre VARCHAR(50) NOT NULL,
            precio DECIMAL(10, 2) NOT NULL,
            imagen VARCHAR(200))
                            ''')
        self.conn.commit()

        self.cursor.execute('''CREATE TABLE IF NOT EXISTS clientes (
            idCliente INT primary key NOT NULL,
            nombre VARCHAR(50) NOT NULL,
            apellido VARCHAR(50),
            mail VARCHAR(100),
            TipoUsuario CHAR(1))
                            ''')
        self.conn.commit()

        self.cursor.execute('''CREATE TABLE IF NOT EXISTS reservas (
            idReserva INT primary key NOT NULL,
            idCliente INT NOT NULL,
            foreign key (idCliente) references clientes(idCliente),
            fecha DATE NOT NULL,
            cantPersonas INT)
                            ''')
        self.conn.commit()

        self.cursor.execute('''CREATE TABLE IF NOT EXISTS reservasPlatillos (
            idReservaPlatillo INT auto_increment primary key,
            idReserva INT,
            foreign key (idReserva) references reservas(idReserva),
            idPlatillo INT,
            foreign key (idPlatillo) references platillos(idPlatillo))
                            ''')
        self.conn.commit()

        self.cursor.execute('''CREATE TABLE IF NOT EXISTS reservasBebidas (
            idReservaPlatillo INT auto_increment primary key,
            idReserva INT,
            foreign key (idReserva) references reservas(idReserva),
            idBebida INT,
            foreign key (idBebida) references bebidas(idBebida))
                            ''')
        self.conn.commit()

        self.cursor.close()
        self.cursor = self.conn.cursor(dictionary=True)
#-----------------------------------------------------------------------------------
# Funciones para agregar, borrar y seleccionar objetos----------------------------

    def agregar_bebida(self, idBebida, nombre, precio, imagen):
        # Verificamos si ya existe un objeto con el mismo id
        self.cursor.execute(f"SELECT * FROM bebidas WHERE idBebida = {idBebida}")
        objeto_existe = self.cursor.fetchone()
        if objeto_existe:
            return False

        sql = "INSERT INTO bebidas (idBebida, nombre, precio, imagen) VALUES (%s, %s, %s, %s)"
        valores = (idBebida, nombre, precio, imagen)

        self.cursor.execute(sql, valores)
        self.conn.commit()
        return True

    def agregar_platillo(self, idPlatillo, nombre, precio, imagen):
        self.cursor.execute(f"SELECT * FROM platillos WHERE idPlatillo = {idPlatillo}")
        objeto_existe = self.cursor.fetchone()
        if objeto_existe:
            return False

        sql = "INSERT INTO platillos (idPlatillo, nombre, precio, imagen VALUES (%s, %s, %s, %s)"
        valores = (idPlatillo, nombre, precio, imagen)

        self.cursor.execute(sql, valores)
        self.conn.commit()
        return True

    def agregar_cliente(self, idCliente, nombre, apellido, mail, tipoUsuario):
        self.cursor.execute(f"SELECT * FROM clientes WHERE idCliente = {idCliente}")
        objeto_existe = self.cursor.fetchone()
        if objeto_existe:
            return False

        sql = "INSERT INTO clientes (idCliente, nombre, apellido, mail, tipoUsuario) VALUES (%s, %s, %s, %s, %s)"
        valores = (idCliente, nombre, apellido, mail, tipoUsuario)

        self.cursor.execute(sql, valores)
        self.conn.commit()
        return True

    def agregar_reserva(self, idReserva, idCliente, fecha, cantPersonas):
        self.cursor.execute(f"SELECT * FROM reservas WHERE idReserva = {idReserva}")
        objeto_existe = self.cursor.fetchone()
        if objeto_existe:
            return False

        sql = "INSERT INTO reservas (idReserva, idCliente, fecha, cantPersonas) VALUES (%s, %s, %s, %s)"
        valores = (idReserva, idCliente, fecha, cantPersonas)

        self.cursor.execute(sql, valores)
        self.conn.commit()
        return True

#----------------------------------------------------------------
    def consultar_bebida(self, idBebida):
        self.cursor.execute(f"SELECT * FROM bebidas WHERE idBebida = {idBebida}")
        return self.cursor.fetchone()

    def consultar_platillo(self, idPlatillo):
        self.cursor.execute(f"SELECT * FROM platillos WHERE idPlatillo = {idPlatillo}")
        return self.cursor.fetchone()

    def consultar_cliente(self, idCliente):
        self.cursor.execute(f"SELECT * FROM clientes WHERE idCliente = {idCliente}")
        return self.cursor.fetchone()

    def consultar_reserva(self, idReserva):
        self.cursor.execute(f"SELECT * FROM reservas WHERE idReserva = {idReserva}")
        return self.cursor.fetchone()
#------------------------------------------------------------------------
    def modificar_bebida(self, idBebida, nuevo_nombre, nuevo_precio, nueva_imagen):
        sql = "UPDATE bebidas SET nombre = %s, precio = %s, imagen = %s WHERE idBebida = %s"
        valores = (nuevo_nombre, nuevo_precio, nueva_imagen, idBebida)
        self.cursor.execute(sql, valores)
        self.conn.commit()
        return self.cursor.rowcount > 0

    def modificar_platillo(self, idPlatillo, nuevo_nombre, nuevo_precio, nueva_imagen):
        sql = "UPDATE platillos SET nombre = %s, precio = %s, imagen = %s WHERE idPlatillo = %s"
        valores = (nuevo_nombre, nuevo_precio, nueva_imagen, idPlatillo)
        self.cursor.execute(sql, valores)
        self.conn.commit()
        return self.cursor.rowcount > 0

    def modificar_cliente(self, idCliente, nuevo_nombre, nuevo_apellido, nuevo_mail, nuevo_tipoUsuario):
        sql = "UPDATE clientes SET nombre = %s, apellido = %s, mail = %s, tipoUsuario= %s, WHERE idCliente = %s"
        valores = (nuevo_nombre, nuevo_apellido, nuevo_mail, nuevo_tipoUsuario, idCliente)
        self.cursor.execute(sql, valores)
        self.conn.commit()
        return self.cursor.rowcount > 0

    def modificar_reserva(self, idReserva, idCliente, fecha, cantPersonas):
        sql = "UPDATE reservas SET idCliente = %s, fecha = %s, cantPersonas = %s WHERE idReserva = %s"
        valores = (idCliente, fecha, cantPersonas, idReserva)
        self.cursor.execute(sql, valores)
        self.conn.commit()
        return self.cursor.rowcount > 0


#--------------------------------------------------------------------------------------------
    def eliminar_bebida(self, idBebida):
        self.cursor.execute(f"DELETE FROM bebidas WHERE idBebida = {idBebida}")
        self.conn.commit()
        return self.cursor.rowcount > 0

    def eliminar_platillo(self, idPlatillo):
        self.cursor.execute(f"DELETE FROM platillos WHERE idPlatillo = {idPlatillo}")
        self.conn.commit()
        return self.cursor.rowcount > 0

    def eliminar_cliente(self, idCliente):
        self.cursor.execute(f"DELETE FROM clientes WHERE idCliente = {idCliente}")
        self.conn.commit()
        return self.cursor.rowcount > 0

    def eliminar_reserva(self, idReserva):
        self.cursor.execute(f"DELETE FROM reservas WHERE idReserva = {idReserva}")
        self.conn.commit()
        return self.cursor.rowcount > 0

#------------------------------------------------------------------------------------------------
# Estas funciones no se si son necesarias, pero las dejo por las dudas
    def mostrar_bebida(self, idBebida):
        bebida = self.consultar_bebida(idBebida)
        if bebida:
            print("-" * 40)
            print(f"Código: {bebida['idBebida']}")
            print(f"Nombre: {bebida['nombre']}")
            print(f"Precio: {bebida['precio']}")
            print(f"Imagen: {bebida['imagen']}")
            print("-" * 40)
        else:
            print("Bebida no encontrado.")

    def mostrar_platillo(self, idPlatillo):
        platillo = self.consultar_platillo(idPlatillo)
        if platillo:
            print("-" * 40)
            print(f"Código: {platillo['idPlatillo']}")
            print(f"Nombre: {platillo['nombre']}")
            print(f"Precio: {platillo['precio']}")
            print(f"Imagen: {platillo['imagen']}")
            print("-" * 40)
        else:
            print("Platillo no encontrado.")

    def mostrar_cliente(self, idCliente):
        cliente = self.consultar_cliente(idCliente)
        if cliente:
            print("-" * 40)
            print(f"Código.....: {cliente['idCliente']}")
            print(f"Nombre.....: {cliente['nombre']}")
            print(f"Apellido...: {cliente['apellido']}")
            print(f"Mail.......: {cliente['mail']}")
            print(f"tipoUsuario: {cliente['tipoUsuario']}")
            print("-" * 40)
        else:
            print("Cliente no encontrado.")

    def mostrar_reserva(self, idReserva):
        reserva = self.consultar_reserva(idReserva)
        if reserva:
            print("-" * 40)
            print(f"Código......: {reserva['idReserva']}")
            print(f"Fecha.......: {reserva['fecha']}")
            print(f"CantPersonas: {reserva['cantPersonas']}")
            print("-" * 40)
        else:
            print("Reserva no encontrado.")

#------------------------------------------------------------------------------------------------

    def listar_bebidas(self):
        self.cursor.execute("SELECT * FROM bebidas")
        return self.cursor.fetchall()

    def listar_platillos(self):
        self.cursor.execute("SELECT * FROM platillos")
        return self.cursor.fetchall()

    def listar_clientes(self):
        self.cursor.execute("SELECT * FROM clientes")
        return self.cursor.fetchall()

    def listar_reservas(self):
        self.cursor.execute("SELECT * FROM reservas")
        return self.cursor.fetchall()
#--------------------------------------------------------------------------------------
Pedido = Pedido(host='guillelorex.mysql.pythonanywhere-services.com', user='guillelorex', password='nomade123', database='guillelorex$nomade_db')
RUTA_DESTINO = './static/imagenes/'

# o este host='guillelorex.pythonanywhere.com'
# host='guillelorex.mysql.pythonanywhere-services.com'
# host: Es el que nos proporcionó el sitio. Lo podemos ver en la pestaña "Databases"
# user: Es el usuario de la base de datos,
# password: Es el password que elegimos para la base de datos
# database: El nombre de la base de datos, generalmente tu_usuario$base_de_datos
#--------------------------------------------------------------------------------------

@app.route("/bebidas", methods=["GET"]) #definir página HECHO
def listar_bebidas():
    bebidas = Pedido.listar_bebidas()
    return jsonify(bebidas)


@app.route("/platillos", methods=["GET"]) #definir página HECHO
def listar_platillos():
    platillos = Pedido.listar_platillos()
    return jsonify(platillos)


@app.route("/clientes", methods=["GET"]) #definir página HECHO
def listar_clientes():
    clientes = Pedido.listar_clientes()
    return jsonify(clientes)

@app.route("/reservas", methods=["GET"]) #definir página HECHO
def listar_reservas():
    reservas = Pedido.listar_reservas()
    return jsonify(reservas)

#--------------------------------------------------------------------------------------

@app.route("/bebidas/<int:idBebida>", methods=["GET"]) #definir página HECHO
def mostrar_bebida(idBebida):
    bebida = Pedido.consultar_bebida(idBebida)
    if bebida:
        return jsonify(bebida), 201
    else:
        return "Bebida no encontrada", 404

@app.route("/platillos/<int:idPlatillo>", methods=["GET"]) #definir página HECHO
def mostrar_platillo(idPlatillo):
    platillo = Pedido.consultar_platillo(idPlatillo)
    if platillo:
        return jsonify(platillo), 201
    else:
        return "Platillo no encontrado", 404

@app.route("/clientes/<int:idCliente>", methods=["GET"]) #definir página HECHO
def mostrar_cliente(idCliente):
    cliente = Pedido.consultar_cliente(idCliente)
    if cliente:
        return jsonify(cliente), 201
    else:
        return "Cliente no encontrado", 404

@app.route("/reservas/<int:idReserva>", methods=["GET"]) #definir página HECHO
def mostrar_reserva(idReserva):
    reserva = Pedido.consultar_reserva(idReserva)
    if reserva:
        return jsonify(reserva), 201
    else:
        return "Reserva no encontrado", 404

#--------------------------------------------------------------------------------------------

@app.route("/bebidas", methods=["POST"]) # definir página HECHO
def agregar_bebida():
    idBebida = request.form['idBebida']   # definir formulario
    nombre = request.form['nombre']
    precio = request.form['precio']
    imagen = request.files['imagen']


    bebida = Pedido.consultar_bebida(idBebida)
    if not bebida:
        nombre_imagen = secure_filename(imagen.filename) #definir imagenes y rutas
        nombre_base, extension = os.path.splitext(nombre_imagen)
        nombre_imagen = f"{nombre_base}_{int(time.time())}{extension}"

    if Pedido.agregar_bebida(idBebida, nombre, precio, nombre_imagen):
        imagen.save(os.path.join(RUTA_DESTINO, nombre_imagen)) # Definir Ruta  DEFINIDA EN LA VAR PRINCIPAL  204
        return jsonify({"mensaje": "Bebida agregada"}), 201
    else:
        return jsonify({"mensaje": "Bebida ya existe"}), 400

@app.route("/platillos", methods=["POST"]) # definir página HECHO
def agregar_platillo():
    idPlatillo = request.form['idPlatillo']   # definir formulario
    nombre = request.form['nombre']
    precio = request.form['precio']
    imagen = request.files['imagen']


    platillo = Pedido.consultar_platillo(idPlatillo)
    if not platillo:
        nombre_imagen = secure_filename(imagen.filename) #definir imagenes y rutas
        nombre_base, extension = os.path.splitext(nombre_imagen)
        nombre_imagen = f"{nombre_base}_{int(time.time())}{extension}"

    if Pedido.agregar_platillo(idPlatillo, nombre, precio, nombre_imagen):
        imagen.save(os.path.join(RUTA_DESTINO, nombre_imagen)) # Definir Ruta DEFINIDA EN LA VAR PRINCIPAL  204
        return jsonify({"mensaje": "Platillo agregado"}), 201
    else:
        return jsonify({"mensaje": "Platillo ya existe"}), 400

@app.route("/clientes", methods=["POST"]) # definir página HECHO
def agregar_cliente():
    idCliente = request.form['idCliente']   # definir formulario
    nombre = request.form['nombre']
    apellido = request.form['apellido']
    mail = request.form['mail']
    tipoUsuario = request.form['tipoUsuario']

    # saque la parte de imagenes, No va a tener imagen el cliente
    if Pedido.agregar_cliente(idCliente, nombre, apellido, mail, tipoUsuario):
        return jsonify({"mensaje": "Cliente agregado"}), 201
    else:
        return jsonify({"mensaje": "Cliente ya existe"}), 400

@app.route("/reservas", methods=["POST"]) # definir página HECHO
def agregar_reserva():
    idReserva = request.form['idReserva']   # definir formulario
    idCliente = request.form['idCliente']
    fecha = request.form['fecha']
    cantPersonas = request.form['cantPersonas']

    if Pedido.agregar_reserva(idReserva, idCliente, fecha, cantPersonas):
        return jsonify({"mensaje": "Reserva agregado"}), 201
    else:
        return jsonify({"mensaje": "Reserva ya existe"}), 400

#----------------------------------------------------------------------------------

@app.route("/bebidas/<int:idBebida>", methods=["PUT"]) #Definir página  HECHO
def modificar_bebida(idBebida):
    #Recojo los datos del form
    nuevo_nombre = request.form.get("nombre") #Definir formulario
    nuevo_precio = request.form.get("precio")
    imagen = request.files['imagen']

    # Procesamiento de la imagen
    nombre_imagen = secure_filename(imagen.filename)
    nombre_base, extension = os.path.splitext(nombre_imagen)
    nombre_imagen = f"{nombre_base}_{int(time.time())}{extension}"
    imagen.save(os.path.join(RUTA_DESTINO, nombre_imagen)) #Definir ruta e imagen DEFINIDA EN LA VAR PRINCIPAL  204


    bebida = bebida = Pedido.consultar_bebida(idBebida)
    if bebida:
        imagen_vieja = bebida["imagen_url"]
        ruta_imagen = os.path.join(RUTA_DESTINO, imagen_vieja) #Definir imagen y ruta DEFINIDA EN LA VAR PRINCIPAL  204

        if os.path.exists(ruta_imagen):
            os.remove(ruta_imagen)

    if Pedido.modificar_bebida(idBebida, nuevo_nombre, nuevo_precio, nombre_imagen):
        return jsonify({"mensaje": "Bebida modificada"}), 200
    else:
        return jsonify({"mensaje": "Bebida no encontrada"}), 403

@app.route("/platillos/<int:idPlatillo>", methods=["PUT"]) #Definir página HECHO
def modificar_platillo(idPlatillo):
    nuevo_nombre = request.form.get("descripcion") #Definir formulario
    nuevo_precio = request.form.get("precio")
    imagen = request.files['imagen']

    nombre_imagen = secure_filename(imagen.filename)
    nombre_base, extension = os.path.splitext(nombre_imagen)
    nombre_imagen = f"{nombre_base}_{int(time.time())}{extension}"
    imagen.save(os.path.join(RUTA_DESTINO, nombre_imagen)) #Definir ruta e imagen DEFINIDA EN LA VAR PRINCIPAL  204


    platillo = platillo = Pedido.consultar_platillo(idPlatillo)
    if platillo:
        imagen_vieja = platillo["imagen_url"]
        ruta_imagen = os.path.join(RUTA_DESTINO, imagen_vieja) #Definir imagen y ruta DEFINIDA EN LA VAR PRINCIPAL  204

        if os.path.exists(ruta_imagen):
            os.remove(ruta_imagen)

    if Pedido.modificar_platillo(idPlatillo, nuevo_nombre, nuevo_precio, nombre_imagen):
        return jsonify({"mensaje": "Platillo modificado"}), 200
    else:
        return jsonify({"mensaje": "Platillo no encontrado"}), 403

@app.route("/clientes/<int:idCliente>", methods=["PUT"]) #Definir página HECHO
def modificar_cliente(idCliente):
    nuevo_nombre = request.form.get("descripcion") #Definir formulario
    nuevo_apellido = request.form.get("cantidad")
    nuevo_mail = request.form.get("precio")
    nuevo_tipoUsuario = request.form.get("tipoUsuario")

    if Pedido.modificar_cliente(idCliente, nuevo_nombre, nuevo_apellido, nuevo_mail, nuevo_tipoUsuario):
        return jsonify({"mensaje": "Cliente modificado"}), 200
    else:
        return jsonify({"mensaje": "Cliente no encontrado"}), 403

@app.route("/reservas/<int:idReserva>", methods=["PUT"]) #Definir página HECHO
def modificar_reserva(idReserva):
    nueva_idCliente = request.form.get("idCliente") #Definir formulario
    nueva_fecha = request.form.get("fecha")
    nueva_cantPersonas = request.form.get("cantPersonas")

    if Pedido.modificar_reserva(idReserva, nueva_idCliente, nueva_fecha, nueva_cantPersonas):
        return jsonify({"mensaje": "Reserva modificado"}), 200
    else:
        return jsonify({"mensaje": "Reserva no encontrado"}), 403

#---------------------------------------------------------------------

@app.route("/bebidas/<int:idBebida>", methods=["DELETE"]) #Definir ruta
def eliminar_bebida(idBebida):
    bebida = bebida = Pedido.consultar_bebida(idBebida)
    if bebida:
        imagen_vieja = bebida["imagen_url"]
        ruta_imagen = os.path.join(RUTA_DESTINO, imagen_vieja) #Definir ruta e imagen DEFINIDA EN LA VAR PRINCIPAL  204

        if os.path.exists(ruta_imagen):
            os.remove(ruta_imagen)

    if Pedido.eliminar_bebida(idBebida):
        return jsonify({"mensaje": "Bebida eliminada"}), 200
    else:
        return jsonify({"mensaje": "Error al eliminar la bebida"}), 500


@app.route("/platillos/<int:idPlatillo>", methods=["DELETE"]) #Definir ruta HECHO
def eliminar_platillo(idPlatillo):
    platillo = platillo = Pedido.consultar_bebida(idPlatillo)
    if platillo:
        imagen_vieja = platillo["imagen_url"]
        ruta_imagen = os.path.join(RUTA_DESTINO, imagen_vieja) #Definir ruta e imagen DEFINIDA EN LA VAR PRINCIPAL  204

        if os.path.exists(ruta_imagen):
            os.remove(ruta_imagen)

    if Pedido.eliminar_platillo(idPlatillo):
        return jsonify({"mensaje": "Platillo eliminado"}), 200
    else:
        return jsonify({"mensaje": "Error al eliminar el platillo"}), 500

@app.route("/clientes/<int:idCliente>", methods=["DELETE"]) #Definir ruta HECHO
def eliminar_cliente(idCliente):

    if Pedido.eliminar_cliente(idCliente):
        return jsonify({"mensaje": "Cliente eliminado"}), 200
    else:
        return jsonify({"mensaje": "Error al eliminar el cliente"}), 500

@app.route("/reservas/<int:idReserva>", methods=["DELETE"]) #Definir ruta HECHO
def eliminar_reserva(idReserva):

    if Pedido.eliminar_reserva(idReserva):
        return jsonify({"mensaje": "Reserva eliminado"}), 200
    else:
        return jsonify({"mensaje": "Error al eliminar el reserva"}), 500
#-----------------------------------------------------------------------------------------------

