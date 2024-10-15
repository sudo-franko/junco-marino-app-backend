from db import get_db

class Platillo:
    def __init__(self, id=0, nombre="", descripcion="", precio=0.0, disponible=True, categoria=""):
        self.id = id
        self.nombre = nombre
        self.descripcion = descripcion
        self.precio = precio
        self.disponible = disponible
        self.categoria = categoria

    def listar(self):
        try:
            conn = get_db()
            with conn.cursor() as cursor:
                sql = "CALL ObtenerTodosLosPlatillos()"
                cursor.execute(sql)
                platillos = cursor.fetchall()
                return platillos
        except Exception as e:
            return e
        finally:
            if conn:
                conn.close()
