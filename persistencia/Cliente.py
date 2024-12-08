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
                params = (
                    self.usuario,
                    self.contrasena,
                    self.nombres,
                    self.apellidos,
                    self.correo,
                    self.telefono, 
                    self.direccion,
                    0
                )
                cursor.callproc('registrarCliente', params)
                cursor.execute("SELECT @_registrarCliente_7 AS idCliente;")
                result = cursor.fetchone()
                self.id = result['idCliente']
                conn.commit()
                return {'status': 'success', 'idCliente': self.id}
        except Exception as e:
             return {'status': 'error', 'error': str(e)}
        finally:
            if conn:
                conn.close()


    def actualizar(self):
        try:
            conn = get_db()
            with conn.cursor() as cursor:
                params = (
                    self.id,
                    self.nombres,
                    self.apellidos,
                    self.correo,
                    self.telefono,
                    self.direccion
                )
                cursor.callproc('actualizarCliente', params)
                conn.commit()
                return {'status': 'success', 'message': 'Cliente actualizado exitosamente'}
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
                    self.contrasena,)
                cursor.callproc('loginCliente', params)
                cliente = cursor.fetchall();
                if not cliente:
                    return {'status': 'login_error', 'message': 'Usuario o contraseña incorrectos'}
                
                return {'status': 'success', 'message': 'Cliente logeado exitosamente', 'cliente': cliente}
        except Exception as e:
            return {'status': 'error', 'error': str(e)}
        finally:
            if conn:
                conn.close()