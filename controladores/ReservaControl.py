from flask import Blueprint, request, jsonify, send_from_directory, current_app
from persistencia.ReservaMesa import ReservaMesa
import os
import qrcode

reservaControl = Blueprint('reservaControl', __name__)

def generarQR(idReserva, data):
    qr_data = {'idReserva': idReserva, **data}
    qr = qrcode.QRCode(
        version=4, 
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=10,
        border=2,
    )
    qr.add_data(qr_data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    path = os.path.join(current_app.config['QR_FOLDER'], f'Reserva-{idReserva}.png')
    img.save(path)
    return 'Codigo guardado'


def buscarQR(id):
    filepath = os.path.join(current_app.config['QR_FOLDER'], f'Reserva-{id}.png')
    if os.path.exists(filepath):
        return f'Reserva-{id}.png'
    return False


@reservaControl.route('/registrarReserva', methods=['POST'])
def registrarReserva():
    if not request.is_json:
        return jsonify({'status': 'error', 'message': 'Content-type must be application/json'}), 400

    data = request.get_json()

    idCliente = data.get('idCliente')
    numPersonas = data.get('numPersonas')
    numMesa = data.get('numMesa')
    fecha = data.get('fecha')
    estado = data.get('estado')

    if not (numPersonas and numMesa and fecha and estado):
        return jsonify({'status': 'error', 'message': 'Faltan datos requeridos'}), 400

    reserva = ReservaMesa(
        idCliente=idCliente,
        numPersonas=numPersonas,
        numMesa=numMesa,
        fecha=fecha,
        estado=estado
    )

    result = reserva.registrarReserva()

    if result.get('status') == 'success':
        idReserva = result.get('idReserva')
        generarQR(idReserva, data)
        return jsonify({'status': 'success', 'message': 'Reserva registrada correctamente', 'idReserva': idReserva}), 200
    else:
        error_message = result.get('error', 'Error desconocido')
        return jsonify({'status': 'error', 'message': error_message}), 500


@reservaControl.route('/actualizarReserva', methods=['PUT'])
def actualizar_reserva():
    if not request.is_json:
        return jsonify({'status': 'error', 'message': 'Content-type must be application/json'}), 400

    data = request.get_json()
    idReserva = data.get('idReserva')
    fecha = data.get('fecha')
    numPersonas = data.get('numPersonas')
    numMesa = data.get('numMesa')
    estado = data.get('estado')

    if not idReserva:
        return jsonify({'status': 'error', 'message': 'El campo idReserva es requerido'}), 400

    reserva = ReservaMesa(
        idReserva=idReserva,
        numPersonas=numPersonas,
        numMesa=numMesa,
        fecha=fecha,
        estado=estado
    )

    result = reserva.actualizarReserva()
    return jsonify(result)


@reservaControl.route('/listarReservas', methods=['GET'])
def listar_reservas():
    result = ReservaMesa.obtenerReservas()
    return jsonify(result)


@reservaControl.route('/listarReservasPorCliente/<int:id_cliente>', methods=['GET'])
def listar_reservas_por_cliente(id_cliente):
    result = ReservaMesa.obtenerReservasPorCliente(id_cliente)
    return jsonify(result)


@reservaControl.route('/listarReservasPorFecha', methods=['GET'])
def listar_reservas_por_fecha():
    fecha = request.args.get('fecha')
    if not fecha:
        return jsonify({'status': 'error', 'message': 'El parámetro fecha es requerido'}), 400

    result = ReservaMesa.obtenerReservasPorFecha(fecha)
    return jsonify(result)


@reservaControl.route('/listarMesasReservasPorFecha', methods=['GET'])
def listar_mesas_reservas_por_fecha():
    fecha = request.args.get('fecha')
    if not fecha:
        return jsonify({'status': 'error', 'message': 'El parámetro fecha es requerido'}), 400

    result = ReservaMesa.obtenerMesasReservasPorFecha(fecha)
    return jsonify(result)


@reservaControl.route('/obtenerQRReserva/<int:id_qr>', methods=['GET'])
def obtenerQR(id_qr):
    filename = buscarQR(id_qr)
    if filename:
        return send_from_directory(current_app.config['QR_FOLDER'], filename)
    else:
        return jsonify({'error': 'Imagen de QR no encontrado'}), 404

