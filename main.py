from flask import Flask
from flask_cors import CORS
import os
import platform
from controladores.PlatilloControl import platilloControl

app = Flask(__name__)
CORS(app)

sistema_operativo = platform.system()

if sistema_operativo == 'Windows':
    ruta_completa = r'C:\ArchivosAPI'
    ruta_imagen = r'C:\ArchivosAPI\imagenes'
    ruta_categorias = r'C:\ArchivosAPI\categorias'
    ruta_qr = r'C:\ArchivosAPI\qr'
else:
    ruta_completa = os.path.join(os.path.expanduser('~'), 'ArchivosAPI')
    ruta_imagen = os.path.join(ruta_completa, 'imagenes')
    ruta_qr = os.path.join(ruta_completa, 'qr')
    ruta_categorias = os.path.join(ruta_completa, 'categorias')

app.config['UPLOAD_FOLDER'] = ruta_completa
app.config['IMAGEN_FOLDER'] = ruta_imagen
app.config['CATEGORIA_FOLDER'] = ruta_categorias
app.config['QR_FOLDER'] = ruta_qr


@app.route('/saludo')
def saludar():
    return "Hola"


app.register_blueprint(platilloControl)


if __name__ == '__main__':
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    if not os.path.exists(app.config['IMAGEN_FOLDER']):
        os.makedirs(app.config['IMAGEN_FOLDER'])
    if not os.path.exists(app.config['QR_FOLDER']):
        os.makedirs(app.config['QR_FOLDER'])

    app.run(host='0.0.0.0', debug=True, port=4000)

