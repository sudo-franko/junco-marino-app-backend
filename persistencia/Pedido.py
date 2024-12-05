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
                params = (
                    self.nombreCliente,
                    self.telefonoCliente,
                    self.direccionCliente,
                    self.notas,
                    self.tipoEntrega,
                    self.tipoPago,
                    self.monto,
                    detallePedido_json,
                    0
                )
                cursor.callproc('registrarPedidoAnonimo', params)
                cursor.execute("SELECT @_registrarPedidoAnonimo_8 AS idPedido;")
                result = cursor.fetchone()
                self.id = result['idPedido']
                conn.commit()
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
                params = (
                    self.idCliente,
                    self.nombreCliente,
                    self.telefonoCliente,
                    self.direccionCliente,
                    self.notas,
                    self.tipoEntrega,
                    self.tipoPago,
                    self.monto,
                    detallePedido_json,
                    0
                )
                cursor.callproc('registrarPedidoCliente', params)
                cursor.execute("SELECT @_registrarPedidoCliente_9 AS idPedido;")
                result = cursor.fetchone()
                self.id = result['idPedido']
                conn.commit()
                return {'status': 'success', 'idPedido': self.id}
        except Exception as e:
             return {'status': 'error', 'error': str(e)}
        finally:
            if conn:
                conn.close()

    def obtenerPedidoPorId(self):
        try:
            conn = get_db()
            with conn.cursor() as cursor:
                params = (self.id,)
                cursor.callproc('obtenerPedidoPorId', params)
                
                pedido_result = cursor.fetchone()
                cursor.nextset()
                detalle_result = cursor.fetchall()

                if not pedido_result:
                    return {'status': 'error', 'message': 'Pedido no encontrado'}
                
                pedido = {
                    'id': pedido_result['id'],
                    'idCliente': pedido_result['idCliente'],
                    'nombreCliente': pedido_result['nombreCliente'],
                    'telefonoCliente': pedido_result['telefonoCliente'],
                    'direccionCliente': pedido_result['direccionCliente'],
                    'notas': pedido_result['notas'],
                    'tipoEntrega': pedido_result['tipoEntrega'],
                    'tipoPago': pedido_result['tipoPago'],
                    'fecha': pedido_result['fecha'],
                    'monto': pedido_result['monto'],
                    'estado': pedido_result['estado'],
                    'calificacion': pedido_result['calificacion'],
                    'comentario': pedido_result['comentario'],
                    'detallePedido': detalle_result
                }
                return {'status': 'success', 'pedido': pedido}

        except Exception as e:
            return {'status': 'error', 'error': str(e)}
        finally:
            if conn:
                conn.close()


    def obtenerEstadoPedidoPorId(self):
        try:
            conn = get_db()
            with conn.cursor() as cursor:
                params = (self.id,)
                cursor.callproc('obtenerEstadoPedidoPorId', params)
                result = cursor.fetchall()
                
                pedidos = []
                for row in result:
                    pedidos.append({
                        'estado': row['estado'],
                        'calificacion': row['calificacion'],
                        'comentario': row['comentario']
                    })
                
                return {'status': 'success', 'pedidos': pedidos}
        except Exception as e:
            return {'status': 'error', 'error': str(e)}
        finally:
            if conn:
                conn.close()


    def listarPedidosPorCliente(self, idCliente):
        try:
            conn = get_db()
            with conn.cursor() as cursor:
                params = (idCliente,)
                cursor.callproc('listarPedidosPorCliente', params)
                result = cursor.fetchall()
                
                pedidos = []
                for row in result:
                    pedidos.append({
                        'id': row['id'],
                        'fecha': row['fecha'],
                        'estado': row['estado'],
                        'monto': row['monto']
                    })
                
                return {'status': 'success', 'pedidos': pedidos}
        except Exception as e:
            return {'status': 'error', 'error': str(e)}
        finally:
            if conn:
                conn.close()


    def listarPedidosPorAtender(self):
        try:
            conn = get_db()
            with conn.cursor() as cursor:
                cursor.callproc('listarPedidosPorAtender')
                
                pedidos_result = cursor.fetchall()

                if not pedidos_result:
                    return {'status': 'success', 'pedidos': []}
                
                pedidos = [
                    {
                        'id': pedido['id'],
                        'fecha': pedido['fecha'],
                        'estado': pedido['estado'],
                        'monto': pedido['monto']
                    }
                    for pedido in pedidos_result
                ]
                return {'status': 'success', 'pedido': pedidos}

        except Exception as e:
            return {'status': 'error', 'error': str(e)}
        finally:
            if conn:
                conn.close()