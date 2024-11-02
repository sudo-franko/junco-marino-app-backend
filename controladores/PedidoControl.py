from flask import Blueprint, request, jsonify, send_from_directory, current_app
from persistencia.Pedido import Pedido
import os

pedidoControl = Blueprint('pedidoControl', __name__)

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

    return jsonify(result)


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

    return jsonify(result)