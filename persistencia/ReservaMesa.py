from db import get_db

class ReservaMesa:
    def __init__(self, idReserva=0, idCliente=0, numPersonas=0, numMesa=0, fecha="", estado="Pendiente"):
        self.idReserva = idReserva
        self.idCliente = idCliente
        self.numPersonas = numPersonas
        self.numMesa = numMesa
        self.fecha = fecha
        self.estado = estado

    def registrarReserva(self):
        try:
            conn = get_db()
            with conn.cursor() as cursor:
                params = (
                    self.idCliente,
                    self.numPersonas,
                    self.numMesa,
                    self.fecha,
                    self.estado,
                    0 
                )
                cursor.callproc('registrarReserva', params)
                cursor.execute("SELECT @_registrarReserva_5 AS idReserva;")
                result = cursor.fetchone()
                self.idReserva = result['idReserva']
                conn.commit()
                return {'status': 'success', 'idReserva': self.idReserva}
        except Exception as e:
            return {'status': 'error', 'error': str(e)}
        finally:
            if conn:
                conn.close()

    def actualizarReserva(self):
        try:
            conn = get_db()
            with conn.cursor() as cursor:
                params = (
                    self.idReserva,
                    self.fecha,
                    self.numPersonas,
                    self.numMesa,
                    self.estado
                )
                cursor.callproc('ActualizarReservaMesa', params)
                conn.commit()
                return {'status': 'success', 'message': 'Reserva actualizada correctamente'}
        except Exception as e:
            return {'status': 'error', 'error': str(e)}
        finally:
            if conn:
                conn.close()

    @staticmethod
    def obtenerReservas():
        try:
            conn = get_db()
            with conn.cursor() as cursor:
                cursor.callproc('ObtenerReservas')
                result = cursor.fetchall()
                return {'status': 'success', 'reservas': result}
        except Exception as e:
            return {'status': 'error', 'error': str(e)}
        finally:
            if conn:
                conn.close()

    @staticmethod
    def obtenerReservasPorFecha(fecha):
        try:
            conn = get_db()
            with conn.cursor() as cursor:
                params = (fecha,)
                cursor.callproc('ObtenerReservasPorFecha', params)
                result = cursor.fetchall()
                return {'status': 'success', 'reservas': result}
        except Exception as e:
            return {'status': 'error', 'error': str(e)}
        finally:
            if conn:
                conn.close()


    @staticmethod
    def obtenerMesasReservasPorFecha(fecha):
        try:
            conn = get_db()
            with conn.cursor() as cursor:
                params = (fecha,)
                cursor.callproc('ObtenerMesasReservasPorFecha', params)
                result = cursor.fetchall()
                return {'status': 'success', 'reservas': result}
        except Exception as e:
            return {'status': 'error', 'error': str(e)}
        finally:
            if conn:
                conn.close()

    
    @staticmethod
    def obtenerReservasPorCliente(idCliente):
        try:
            conn = get_db()
            with conn.cursor() as cursor:
                params = (idCliente,)
                cursor.callproc('ObtenerReservasPorCliente', params)
                result = cursor.fetchall()
                return {'status': 'success', 'reservas': result}
        except Exception as e:
            return {'status': 'error', 'error': str(e)}
        finally:
            if conn:
                conn.close()

