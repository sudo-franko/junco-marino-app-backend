from flask import Blueprint, request, jsonify
from persistencia.Cliente import Cliente
import os

clienteControl = Blueprint('clienteControl', __name__)

@clienteControl.route('/registrarCliente', methods=['POST'])
def registrarCliente():
    if not request.is_json:
        return jsonify({'status': 'error', 'message': 'Content-type must be application/json'}), 400
    
    data = request.get_json()

    nombres = data.get('nombres')
    apellidos = data.get('apellidos')
    correo = data.get('correo')
    telefono = data.get('telefono')
    direccion = data.get('direccion')
    usuario = data.get('usuario')
    contrasena = data.get('contrasena')

    cliente = Cliente(
        nombres=nombres,
        apellidos=apellidos,
        correo=correo,
        telefono=telefono,
        direccion=direccion,
        usuario=usuario,
        contrasena=contrasena
    )

    result = cliente.registrar()

    if result.get('status') == 'success':
        return jsonify(result), 200
    else:
        return jsonify(result), 500



@clienteControl.route('/actualizarCliente/<int:idCliente>', methods=['PUT'])
def actualizarCliente(idCliente):
    if not request.is_json:
        return jsonify({'status': 'error', 'message': 'Content-type must be application/json'}), 400
    
    data = request.get_json()

    nombres = data.get('nombres')
    apellidos = data.get('apellidos')
    correo = data.get('correo')
    telefono = data.get('telefono')
    direccion = data.get('direccion')

    cliente = Cliente(
        id=idCliente,
        nombres=nombres,
        apellidos=apellidos,
        correo=correo,
        telefono=telefono,
        direccion=direccion
    )

    result = cliente.actualizar()

    if result.get('status') == 'success':
        return jsonify(result), 200
    else:
        return jsonify(result), 500
    

@clienteControl.route('/loginCliente', methods=['POST'])
def login():
    if not request.is_json:
        return jsonify({'status': 'error', 'message': 'Content-type must be application/json'}), 400
    
    data = request.get_json()

    usuario = data.get('usuario')
    contrasena = data.get('contrasena')

    cliente = Cliente(
        usuario=usuario,
        contrasena=contrasena
    )

    result = cliente.login()

    if result.get('status') == 'success':
        return jsonify(result), 200
    elif result.get('status') == 'login_error':
        return jsonify(result), 200
    else:
        return jsonify(result), 500