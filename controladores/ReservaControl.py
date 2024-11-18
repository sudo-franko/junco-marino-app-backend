from flask import Blueprint, request, jsonify, send_from_directory, current_app
from persistencia.ReservaMesa import ReservaMesa
import os

reservaControl = Blueprint('reservaControl', __name__)

@reservaControl.route('/registrarReserva', methods=['POST'])
def registrarReserva():
    if not request.is_json:
        return jsonify({'status': 'error', 'message': 'Content-type must be application/json'}), 400

    data = request.get_json()

    idCliente = data.get('idCliente')
    numPersonas = data.get('numPersonas')
    numMesa = data.get('numMesa')
    fecha = data.get('fecha')  # Debe estar en formato 'YYYY-MM-DD'

    if not (numPersonas and numMesa and fecha):
        return jsonify({'status': 'error', 'message': 'Faltan datos requeridos'}), 400

    reserva = ReservaMesa(
        idCliente=idCliente,
        numPersonas=numPersonas,
        numMesa=numMesa,
        fecha=fecha
    )

    result = reserva.registrarReserva()
    return jsonify(result)