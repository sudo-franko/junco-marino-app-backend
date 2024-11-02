from flask import Blueprint, request, jsonify, send_from_directory, current_app
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

    return jsonify(result)
