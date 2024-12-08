from flask import Blueprint, request, jsonify
from persistencia.Empleado import Empleado
import os

empleadoControl = Blueprint('empleadoControl', __name__)

@empleadoControl.route('/registrarEmpleado', methods=['POST'])
def registrarEmpleado():
    if not request.is_json:
        return jsonify({'status': 'error', 'message': 'Content-type must be application/json'}), 400
    
    data = request.get_json()

    nombres = data.get('nombres')
    apellidos = data.get('apellidos')
    correo = data.get('correo')
    telefono = data.get('telefono')
    usuario = data.get('usuario')
    contrasena = data.get('contrasena')

    empleado = Empleado(
        nombres=nombres,
        apellidos=apellidos,
        correo=correo,
        telefono=telefono,
        usuario=usuario,
        contrasena=contrasena
    )

    result = empleado.registrar()

    if result.get('status') == 'success':
        return jsonify(result), 200
    else:
        return jsonify(result), 500
    

@empleadoControl.route('/loginEmpleado', methods=['POST'])
def login():
    if not request.is_json:
        return jsonify({'status': 'error', 'message': 'Content-type must be application/json'}), 400
    
    data = request.get_json()

    usuario = data.get('usuario')
    contrasena = data.get('contrasena')

    empleado = Empleado(
        usuario=usuario,
        contrasena=contrasena
    )

    result = empleado.login()

    if result.get('status') == 'success':
        return jsonify(result), 200
    elif result.get('status') == 'login_error':
        return jsonify(result), 200
    else:
        return jsonify(result), 500