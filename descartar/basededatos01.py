
from flask import Flask, request, jsonify, render_template

from flask_cors import CORS

import mysql.connector

from werkzeug.utils import secure_filename

import os
import time

app = Flask(__name__)
CORS(app) 


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
            codigo INT,
            descripcion VARCHAR(255) NOT NULL,
            cantidad INT NOT NULL,
            precio DECIMAL(10, 2) NOT NULL,
            imagen_url VARCHAR(255))
                            ''')
        self.conn.commit()

        self.cursor.execute('''CREATE TABLE IF NOT EXISTS platillos (
            codigo INT,
            descripcion VARCHAR(255) NOT NULL,
            cantidad INT NOT NULL,
            precio DECIMAL(10, 2) NOT NULL,
            imagen_url VARCHAR(255))
                            ''')
        self.conn.commit()

        self.cursor.execute('''CREATE TABLE IF NOT EXISTS clientes (
            codigo INT,
            nombre VARCHAR(255) NOT NULL,
            apellido VARCHAR(255) NOT NULL,
            mail VARCHAR(255) NOT NULL)
                            ''')
        self.conn.commit()


        self.cursor.close()
        self.cursor = self.conn.cursor(dictionary=True)
#-----------------------------------------------------------------------------------
# Funciones para agregar, borrar y seleccionar productos----------------------------

    def agregar_bebida(self, codigo, descripcion, cantidad, precio, imagen):
        # Verificamos si ya existe un producto con el mismo código
        self.cursor.execute(f"SELECT * FROM bebidas WHERE codigo = {codigo}")
        producto_existe = self.cursor.fetchone()
        if producto_existe:
            return False

        sql = "INSERT INTO bebidas (codigo, descripcion, cantidad, precio, imagen_url) VALUES (%s, %s, %s, %s, %s)"
        valores = (codigo, descripcion, cantidad, precio, imagen)

        self.cursor.execute(sql, valores)        
        self.conn.commit()
        return True

    def agregar_platillo(self, codigo, descripcion, cantidad, precio, imagen):
        self.cursor.execute(f"SELECT * FROM bebidas WHERE codigo = {codigo}")
        producto_existe = self.cursor.fetchone()
        if producto_existe:
            return False

        sql = "INSERT INTO platillos (codigo, descripcion, cantidad, precio, imagen_url) VALUES (%s, %s, %s, %s, %s)"
        valores = (codigo, descripcion, cantidad, precio, imagen)

        self.cursor.execute(sql, valores)        
        self.conn.commit()
        return True
    
    def agregar_cliente(self, codigo, nombre, apellido, mail):
        self.cursor.execute(f"SELECT * FROM bebidas WHERE codigo = {codigo}")
        producto_existe = self.cursor.fetchone()
        if producto_existe:
            return False

        sql = "INSERT INTO clientes (codigo, nombre, apellido, mail) VALUES (%s, %s, %s, %s)"
        valores = (codigo, nombre, apellido, mail)

        self.cursor.execute(sql, valores)        
        self.conn.commit()
        return True


#----------------------------------------------------------------
    def consultar_bebida(self, codigo):
        self.cursor.execute(f"SELECT * FROM bebidas WHERE codigo = {codigo}")
        return self.cursor.fetchone()

    def consultar_platillo(self, codigo):
        self.cursor.execute(f"SELECT * FROM platillos WHERE codigo = {codigo}")
        return self.cursor.fetchone()
    
    def consultar_cliente(self, codigo):
        self.cursor.execute(f"SELECT * FROM clientes WHERE codigo = {codigo}")
        return self.cursor.fetchone()

#------------------------------------------------------------------------
    def modificar_bebida(self, codigo, nueva_descripcion, nueva_cantidad, nuevo_precio, nueva_imagen):
        sql = "UPDATE bebidas SET descripcion = %s, cantidad = %s, precio = %s, imagen_url = %s WHERE codigo = %s"
        valores = (nueva_descripcion, nueva_cantidad, nuevo_precio, nueva_imagen, codigo)
        self.cursor.execute(sql, valores)
        self.conn.commit()
        return self.cursor.rowcount > 0

    def modificar_platillo(self, codigo, nueva_descripcion, nueva_cantidad, nuevo_precio, nueva_imagen):
        sql = "UPDATE platillos SET descripcion = %s, cantidad = %s, precio = %s, imagen_url = %s WHERE codigo = %s"
        valores = (nueva_descripcion, nueva_cantidad, nuevo_precio, nueva_imagen, codigo)
        self.cursor.execute(sql, valores)
        self.conn.commit()
        return self.cursor.rowcount > 0
    
    def modificar_cliente(self, codigo, nuevo_nombre, nuevo_apellido, nuevo_mail):
        sql = "UPDATE clientes SET nombre = %s, apllido = %s, mail = %s WHERE codigo = %s"
        valores = (nuevo_nombre, nuevo_apellido, nuevo_mail, codigo)
        self.cursor.execute(sql, valores)
        self.conn.commit()
        return self.cursor.rowcount > 0

#--------------------------------------------------------------------------------------------
    def eliminar_bebida(self, codigo):
        self.cursor.execute(f"DELETE FROM bebidas WHERE codigo = {codigo}")
        self.conn.commit()
        return self.cursor.rowcount > 0

    def eliminar_platillo(self, codigo):
        self.cursor.execute(f"DELETE FROM platillos WHERE codigo = {codigo}")
        self.conn.commit()
        return self.cursor.rowcount > 0
    
    def eliminar_cliente(self, codigo):
        self.cursor.execute(f"DELETE FROM clientes WHERE codigo = {codigo}")
        self.conn.commit()
        return self.cursor.rowcount > 0

#------------------------------------------------------------------------------------------------
    def mostrar_bebida(self, codigo):
        bebida = self.consultar_bebida(codigo)
        if bebida:
            print("-" * 40)
            print(f"Código.....: {bebida['codigo']}")
            print(f"Descripción: {bebida['descripcion']}")
            print(f"Cantidad...: {bebida['cantidad']}")
            print(f"Precio.....: {bebida['precio']}")
            print(f"Imagen.....: {bebida['imagen_url']}")
            print("-" * 40)
        else:
            print("Bebida no encontrado.")

    def mostrar_platillo(self, codigo):
        platillo = self.consultar_platillo(codigo)
        if platillo:
            print("-" * 40)
            print(f"Código.....: {platillo['codigo']}")
            print(f"Descripción: {platillo['descripcion']}")
            print(f"Cantidad...: {platillo['cantidad']}")
            print(f"Precio.....: {platillo['precio']}")
            print(f"Imagen.....: {platillo['imagen_url']}")
            print("-" * 40)
        else:
            print("Platillo no encontrado.")

    def mostrar_cliente(self, codigo):
        cliente = self.consultar_cliente(codigo)
        if cliente:
            print("-" * 40)
            print(f"Código.....: {cliente['codigo']}")
            print(f"Nombre.....: {cliente['nombre']}")
            print(f"Apellido...: {cliente['apellido']}")
            print(f"Mail.......: {cliente['mail']}")
            print("-" * 40)
        else:
            print("Platillo no encontrado.")

#--------------------------------------------------------------------------------------
Pedido = Pedido(host='address:guillelorex.mysql.pythonanywhere-services.com', user='guillelorex', password='nomade123', database='guillelorex$nomade_db')
RUTA_DESTINO = './static/imagenes/'
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

#--------------------------------------------------------------------------------------

@app.route("/bebidas/<int:codigo>", methods=["GET"]) #definir página HECHO
def mostrar_bebida(codigo):
    bebida = Pedido.consultar_bebida(codigo)
    if bebida:
        return jsonify(bebida), 201
    else:
        return "Bebida no encontrada", 404

@app.route("/platillos/<int:codigo>", methods=["GET"]) #definir página HECHO
def mostrar_platillo(codigo):
    platillo = Pedido.consultar_platillo(codigo)
    if platillo:
        return jsonify(platillo), 201
    else:
        return "Platillo no encontrado", 404
    

@app.route("/clientes/<int:codigo>", methods=["GET"]) #definir página HECHO
def mostrar_cliente(codigo):
    cliente = Pedido.consultar_cliente(codigo)
    if cliente:
        return jsonify(cliente), 201
    else:
        return "Cliente no encontrado", 404
    
#--------------------------------------------------------------------------------------------

@app.route("/bebidas", methods=["POST"]) # definir página HECHO
def agregar_bebida():
    codigo = request.form['codigo']   # definir formulario
    descripcion = request.form['descripcion']
    cantidad = request.form['cantidad']
    precio = request.form['precio'] 
    imagen = request.files['imagen']

    
    bebida = Pedido.consultar_bebida(codigo)
    if not bebida: # 
        nombre_imagen = secure_filename(imagen.filename) #definir imagenes y rutas
        nombre_base, extension = os.path.splitext(nombre_imagen)
        nombre_imagen = f"{nombre_base}_{int(time.time())}{extension}"

    if Pedido.agregar_bebida(codigo, descripcion, cantidad, precio, nombre_imagen):
        imagen.save(os.path.join(RUTA_DESTINO, nombre_imagen)) # Definir Ruta  DEFINIDA EN LA VAR PRINCIPAL  204
        return jsonify({"mensaje": "Bebida agregada"}), 201
    else:
        return jsonify({"mensaje": "Bebida ya existe"}), 400
    

@app.route("/platillos", methods=["POST"]) # definir página HECHO
def agregar_platillo():
    codigo = request.form['codigo']   # definir formulario
    descripcion = request.form['descripcion']
    cantidad = request.form['cantidad']
    precio = request.form['precio'] 
    imagen = request.files['imagen']

    
    platillo = Pedido.consultar_platillo(codigo)
    if not platillo: # 
        nombre_imagen = secure_filename(imagen.filename) #definir imagenes y rutas
        nombre_base, extension = os.path.splitext(nombre_imagen)
        nombre_imagen = f"{nombre_base}_{int(time.time())}{extension}"

    if Pedido.agregar_platillo(codigo, descripcion, cantidad, precio, nombre_imagen):
        imagen.save(os.path.join(RUTA_DESTINO, nombre_imagen)) # Definir Ruta DEFINIDA EN LA VAR PRINCIPAL  204
        return jsonify({"mensaje": "Platillo agregado"}), 201
    else:
        return jsonify({"mensaje": "Platillo ya existe"}), 400
    


@app.route("/clientes", methods=["POST"]) # definir página HECHO
def agregar_cliente():
    codigo = request.form['codigo']   # definir formulario
    nombre = request.form['nombre']
    apellido = request.form['apellido']
    mail = request.form['mail'] 

    cliente = cliente = Pedido.consultar_cliente(codigo)  # saque la parte de imagenes, no se porque no me toma el cliente como variable si no le pongo el if cliente, no entiendo como funciona CREO QUE LO ARREGLE
    if Pedido.agregar_cliente(codigo, nombre, apellido, mail):
        return jsonify({"mensaje": "Cliente agregado"}), 201
    else:
        return jsonify({"mensaje": "Cliente ya existe"}), 400
    
#----------------------------------------------------------------------------------

@app.route("/bebidas/<int:codigo>", methods=["PUT"]) #Definir página  HECHO
def modificar_bebida(codigo):
    #Recojo los datos del form
    nueva_descripcion = request.form.get("descripcion") #Definir formulario
    nueva_cantidad = request.form.get("cantidad")
    nuevo_precio = request.form.get("precio")
    imagen = request.files['imagen']

    # Procesamiento de la imagen
    nombre_imagen = secure_filename(imagen.filename)
    nombre_base, extension = os.path.splitext(nombre_imagen)
    nombre_imagen = f"{nombre_base}_{int(time.time())}{extension}"
    imagen.save(os.path.join(RUTA_DESTINO, nombre_imagen)) #Definir ruta e imagen DEFINIDA EN LA VAR PRINCIPAL  204

    
    bebida = bebida = Pedido.consultar_bebida(codigo)
    if bebida: 
        imagen_vieja = bebida["imagen_url"]
        ruta_imagen = os.path.join(RUTA_DESTINO, imagen_vieja) #Definir imagen y ruta DEFINIDA EN LA VAR PRINCIPAL  204

        if os.path.exists(ruta_imagen):
            os.remove(ruta_imagen)
    
    if Pedido.modificar_bebida(codigo, nueva_descripcion, nueva_cantidad, nuevo_precio, nombre_imagen):
        return jsonify({"mensaje": "Bebida modificada"}), 200
    else:
        return jsonify({"mensaje": "Bebida no encontrada"}), 403



@app.route("/platillos/<int:codigo>", methods=["PUT"]) #Definir página HECHO
def modificar_platillo(codigo):
    nueva_descripcion = request.form.get("descripcion") #Definir formulario
    nueva_cantidad = request.form.get("cantidad")
    nuevo_precio = request.form.get("precio")
    imagen = request.files['imagen']

    nombre_imagen = secure_filename(imagen.filename)
    nombre_base, extension = os.path.splitext(nombre_imagen)
    nombre_imagen = f"{nombre_base}_{int(time.time())}{extension}"
    imagen.save(os.path.join(RUTA_DESTINO, nombre_imagen)) #Definir ruta e imagen DEFINIDA EN LA VAR PRINCIPAL  204

    
    platillo = platillo = Pedido.consultar_platillo(codigo)
    if platillo: 
        imagen_vieja = platillo["imagen_url"]
        ruta_imagen = os.path.join(RUTA_DESTINO, imagen_vieja) #Definir imagen y ruta DEFINIDA EN LA VAR PRINCIPAL  204

        if os.path.exists(ruta_imagen):
            os.remove(ruta_imagen)
    
    if Pedido.modificar_platillo(codigo, nueva_descripcion, nueva_cantidad, nuevo_precio, nombre_imagen):
        return jsonify({"mensaje": "Platillo modificado"}), 200
    else:
        return jsonify({"mensaje": "Platillo no encontrado"}), 403
    
@app.route("/clientes/<int:codigo>", methods=["PUT"]) #Definir página HECHO
def modificar_cliente(codigo):
    nuevo_nombre = request.form.get("descripcion") #Definir formulario
    nuevo_apellido = request.form.get("cantidad")
    nuevo_mail = request.form.get("precio")

    
    cliente = cliente = Pedido.consultar_cliente(codigo)  # no entiendo este muy bien CREO QUE LO ARREGLE 
    if Pedido.modificar_cliente(codigo, nuevo_nombre, nuevo_apellido, nuevo_mail):
        return jsonify({"mensaje": "Cliente modificado"}), 200
    else:
        return jsonify({"mensaje": "Cliente no encontrado"}), 403
    
#---------------------------------------------------------------------

@app.route("/bebidas/<int:codigo>", methods=["DELETE"]) #Definir ruta
def eliminar_bebida(codigo):
    bebida = bebida = Pedido.consultar_bebida(codigo)
    if bebida:
        imagen_vieja = bebida["imagen_url"]
        ruta_imagen = os.path.join(RUTA_DESTINO, imagen_vieja) #Definir ruta e imagen DEFINIDA EN LA VAR PRINCIPAL  204

        if os.path.exists(ruta_imagen):
            os.remove(ruta_imagen)

    if Pedido.eliminar_bebida(codigo):
        return jsonify({"mensaje": "Bebida eliminada"}), 200
    else:
        return jsonify({"mensaje": "Error al eliminar la bebida"}), 500
    

@app.route("/platillos/<int:codigo>", methods=["DELETE"]) #Definir ruta HECHO
def eliminar_platillo(codigo):
    platillo = platillo = Pedido.consultar_bebida(codigo)
    if platillo:
        imagen_vieja = platillo["imagen_url"]
        ruta_imagen = os.path.join(RUTA_DESTINO, imagen_vieja) #Definir ruta e imagen DEFINIDA EN LA VAR PRINCIPAL  204

        if os.path.exists(ruta_imagen):
            os.remove(ruta_imagen)

    if Pedido.eliminar_platillo(codigo):
        return jsonify({"mensaje": "Platillo eliminado"}), 200
    else:
        return jsonify({"mensaje": "Error al eliminar el platillo"}), 500
    
@app.route("/cliente/<int:codigo>", methods=["DELETE"]) #Definir ruta HECHO
def eliminar_cliente(codigo):
    cliente = cliente = Pedido.consultar_cliente(codigo)
    if Pedido.eliminar_cliente(codigo):
        return jsonify({"mensaje": "Cliente eliminado"}), 200
    else:
        return jsonify({"mensaje": "Error al eliminar el cliente"}), 500
#-----------------------------------------------------------------------------------------------

#ESto no se para que es, pero por las dudas lo agrego, esta en el ejemplo
if __name__ == "__main__":
    app.run(debug=True)