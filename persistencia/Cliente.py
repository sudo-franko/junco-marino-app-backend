from db import get_db

class Cliente:
    def __init__(self, id=0, nombres="", apellidos="", correo="", telefono="", direccion="", 
                 idUsuario=0, usuario="", contrasena=""):
        self.id = id
        self.nombres = nombres
        self.apellidos = apellidos
        self.correo = correo
        self.telefono = telefono
        self.direccion = direccion
        self.idUsuario = idUsuario
        self.usuario = usuario
        self.contrasena = contrasena

    
    def registrar(self):
        try:
            conn = get_db()
            with conn.cursor() as cursor:
                cursor.callproc('registrarCliente', (
                    self.usuario,
                    self.contrasena,
                    self.nombres,
                    self.apellidos,
                    self.correo,
                    self.telefono, 
                    self.direccion
                ))
                conn.commit()
                cursor.execute("SELECT LAST_INSERT_ID() AS idCliente;")
                result = cursor.fetchone()
                self.id = result['idCliente']
                return {'status': 'success', 'idCliente': self.id}
        except Exception as e:
             return {'status': 'error', 'error': str(e)}
        finally:
            if conn:
                conn.close()
