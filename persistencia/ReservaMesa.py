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
                    0  # Valor de salida para idReserva
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