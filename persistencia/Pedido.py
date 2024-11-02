from db import get_db
import json

class Pedido:
    def __init__(self, id=0, idCliente=0, nombreCliente="", telefonoCliente="", direccionCliente="", notas="",
                 tipoEntrega="", tipoPago="", fecha="", monto=0, estado="", calificacion="", comentario="",
                 detallePedido=None):
        self.id = id
        self.idCliente = idCliente
        self.nombreCliente = nombreCliente
        self.telefonoCliente = telefonoCliente
        self.direccionCliente = direccionCliente
        self.notas = notas
        self.tipoEntrega = tipoEntrega
        self.tipoPago = tipoPago
        self.fecha = fecha
        self.monto = monto
        self.estado = estado
        self.calificacion = calificacion
        self.comentario = comentario
        self.detallePedido = detallePedido if detallePedido else []

    def registrarPedidoAnonimo(self):
        try:
            conn = get_db()
            with conn.cursor() as cursor:
                detallePedido_json = json.dumps(self.detallePedido)
                cursor.callproc('registrarPedidoAnonimo', (
                    self.nombreCliente,
                    self.telefonoCliente,
                    self.direccionCliente,
                    self.notas,
                    self.tipoEntrega,
                    self.tipoPago,
                    self.monto,
                    detallePedido_json
                ))
                conn.commit()
                cursor.execute("SELECT LAST_INSERT_ID() AS idPedido;")
                result = cursor.fetchone()
                self.id = result['idPedido']
                return {'status': 'success', 'idPedido': self.id}
        except Exception as e:
             return {'status': 'error', 'error': str(e)}
        finally:
            if conn:
                conn.close()

    
    def registrarPedidoCliente(self):
        try:
            conn = get_db()
            with conn.cursor() as cursor:
                detallePedido_json = json.dumps(self.detallePedido)
                cursor.callproc('registrarPedidoCliente', (
                    self.idCliente,
                    self.nombreCliente,
                    self.telefonoCliente,
                    self.direccionCliente,
                    self.notas,
                    self.tipoEntrega,
                    self.tipoPago,
                    self.monto,
                    detallePedido_json
                ))
                conn.commit()
                cursor.execute("SELECT LAST_INSERT_ID() AS idPedido;")
                result = cursor.fetchone()
                self.id = result['idPedido']
                return {'status': 'success', 'idPedido': self.id}
        except Exception as e:
             return {'status': 'error', 'error': str(e)}
        finally:
            if conn:
                conn.close()