from flask import Blueprint, request, jsonify, send_from_directory, current_app
from persistencia.Pedido import Pedido
import os
import qrcode

pedidoControl = Blueprint('pedidoControl', __name__)

def generarQR(data):
    qr = qrcode.QRCode(
        version=4, 
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=10,
        border=2,
    )
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    path = os.path.join(current_app.config['QR_FOLDER'], f'{data}.png')
    img.save(path)
    return 'Codigo guardado'

def buscarQR(id):
    filepath = os.path.join(current_app.config['QR_FOLDER'], f'{id}.png')
    if os.path.exists(filepath):
        return f'{id}.png'
    return False



@pedidoControl.route('/registrarPedidoAnonimo', methods=['POST'])
def registrarPedidoAnonimo():
    if not request.is_json:
        return jsonify({'status': 'error', 'message': 'Content-type must be application/json'}), 400

    data = request.get_json()

    nombreCliente = data.get('nombreCliente')
    telefonoCliente = data.get('telefonoCliente')
    direccionCliente = data.get('direccionCliente')
    notas = data.get('notas', '')
    tipoEntrega = data.get('tipoEntrega')
    tipoPago = data.get('tipoPago')
    monto = data.get('monto')
    detallePedido = data.get('detallePedido', [])

    pedido = Pedido(
        nombreCliente=nombreCliente,
        telefonoCliente=telefonoCliente,
        direccionCliente=direccionCliente,
        notas=notas,
        tipoEntrega=tipoEntrega,
        tipoPago=tipoPago,
        monto=monto,
        detallePedido=detallePedido
    )

    result = pedido.registrarPedidoAnonimo()
    
    if result.get('status') == 'success':
        idPedido = result.get('idPedido')
        generarQR(idPedido)
        return jsonify({'status': 'success', 'message': 'Pedido registrado correctamente', 'idPedido': idPedido}), 200
    else:
        error_message = result.get('error', 'Error desconocido')
        return jsonify({'status': 'error', 'message': error_message}), 500


@pedidoControl.route('/registrarPedidoCliente', methods=['POST'])
def registrarPedidoCliente():
    if not request.is_json:
        return jsonify({'status': 'error', 'message': 'Content-type must be application/json'}), 400

    data = request.get_json()

    idCliente = data.get('idCliente')
    nombreCliente = data.get('nombreCliente')
    telefonoCliente = data.get('telefonoCliente')
    direccionCliente = data.get('direccionCliente')
    notas = data.get('notas', '')
    tipoEntrega = data.get('tipoEntrega')
    tipoPago = data.get('tipoPago')
    monto = data.get('monto')
    detallePedido = data.get('detallePedido', [])

    pedido = Pedido(
        idCliente=idCliente,
        nombreCliente=nombreCliente,
        telefonoCliente=telefonoCliente,
        direccionCliente=direccionCliente,
        notas=notas,
        tipoEntrega=tipoEntrega,
        tipoPago=tipoPago,
        monto=monto,
        detallePedido=detallePedido
    )

    result = pedido.registrarPedidoCliente()

    if result.get('status') == 'success':
        idPedido = result.get('idPedido')
        generarQR(idPedido)
        return jsonify({'status': 'success', 'message': 'Pedido registrado correctamente', 'idPedido': idPedido}), 200
    else:
        error_message = result.get('error', 'Error desconocido')
        return jsonify({'status': 'error', 'message': error_message}), 500
    

@pedidoControl.route('/obtenerQRPedido/<int:id_qr>', methods=['GET'])
def obtenerQR(id_qr):
    filename = buscarQR(id_qr)
    if filename:
        return send_from_directory(current_app.config['QR_FOLDER'], filename)
    else:
        return jsonify({'error': 'Imagen de QR no encontrado'}), 404
    

@pedidoControl.route('/obtenerPedido/<int:idPedido>', methods=['GET'])
def obtenerPedido(idPedido):
    pedido = Pedido(id=idPedido)
    result = pedido.obtenerPedidoPorId()
    return jsonify(result)


@pedidoControl.route('/obtenerEstadoPedido/<int:idPedido>', methods=['GET'])
def obtenerEstadoPedido(idPedido):
    pedido = Pedido(id=idPedido)
    result = pedido.obtenerEstadoPedidoPorId()
    return jsonify(result)


@pedidoControl.route('/listarPedidosPorCliente/<int:idCliente>', methods=['GET'])
def listar_pedidos_por_cliente(idCliente):
    pedido = Pedido()
    result = pedido.listarPedidosPorCliente(idCliente)
    return jsonify(result)


@pedidoControl.route('/listarPedidosPorAtender', methods=['GET'])
def listarPedidosPorAtender():
    pedido = Pedido()
    result = pedido.listarPedidosPorAtender()
    return jsonify(result)

