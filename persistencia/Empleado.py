from db import get_db

class Empleado:
    def __init__(self, id=0, nombres="", apellidos="", correo="", telefono="", direccion="", 
                 idUsuario=0, usuario="", contrasena=""):
        self.id = id
        self.nombres = nombres
        self.apellidos = apellidos
        self.correo = correo
        self.telefono = telefono
        self.idUsuario = idUsuario
        self.usuario = usuario
        self.contrasena = contrasena
    

    def registrar(self):
        try:
            conn = get_db()
            with conn.cursor() as cursor:
                params = (
                    self.usuario,
                    self.contrasena,
                    self.nombres,
                    self.apellidos,
                    self.correo,
                    self.telefono, 
                    0
                )
                cursor.callproc('registrarEmpleado', params)
                cursor.execute("SELECT @_registrarEmpleado_6 AS idEmpleado;")
                result = cursor.fetchone()
                self.id = result['idEmpleado']
                conn.commit()
                return {'status': 'success', 'idEmpleado': self.id}
        except Exception as e:
             return {'status': 'error', 'error': str(e)}
        finally:
            if conn:
                conn.close()

    def login(self):
        try:
            conn = get_db()
            with conn.cursor() as cursor:
                params = (
                    self.usuario,
                    self.contrasena,
                )
                cursor.callproc('loginEmpleado', params)
                empleado = cursor.fetchall()
                if not empleado:
                    return {'status': 'login_error', 'message': 'Usuario o contraseña incorrectos'}
                
                return {'status': 'success', 'message': 'Empleado logeado exitosamente', 'empleado': empleado}
    
        except Exception as e:
            return {'status': 'error', 'error': str(e)}
        finally:
            if conn:
                conn.close()