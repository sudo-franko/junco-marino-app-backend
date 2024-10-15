from flask import Flask
from flask import request, jsonify, send_from_directory
from flask_cors import CORS
import os
import platform
from persistencia.Platillo import Platillo

app = Flask(__name__)
CORS(app)

sistema_operativo = platform.system()

if sistema_operativo == 'Windows':
    ruta_completa = r'C:\ArchivosAPI'
    ruta_imagen = r'C:\ArchivosAPI\imagenes'
    ruta_qr = r'C:\ArchivosAPI\qr'
else:
    ruta_completa = os.path.join(os.path.expanduser('~'), 'ArchivosAPI')
    ruta_imagen = os.path.join(ruta_completa, 'imagenes')
    ruta_qr = os.path.join(ruta_completa, 'qr')

app.config['UPLOAD_FOLDER'] = ruta_completa
app.config['IMAGEN_FOLDER'] = ruta_imagen
app.config['QR_FOLDER'] = ruta_qr

def find_file(id):
    filepath = os.path.join(app.config['IMAGEN_FOLDER'], f'{id}.png')
    if os.path.exists(filepath):
        return f'{id}.png'
    return False


@app.route('/saludo')
def saludar():
    return "Hola"


@app.route('/listarPlatillos')
def listar():
    platillo = Platillo()
    platillos = platillo.listar()
    if platillos:
        if isinstance(platillos, str):
            return jsonify({'error': platillos}), 500
        else:
            return jsonify({'productos': platillos}), 200
    else:
        return jsonify({'mensaje': 'No hay productos registrados'}), 400


@app.route('/imagenPlatillo/<int:platillo_id>', methods=['GET'])
def obtenerImagen(platillo_id):
    filename = find_file(platillo_id)
    if filename:
        return send_from_directory(app.config['IMAGEN_FOLDER'], filename)
    else:
        return jsonify({'error': 'Imagen de platillo no encontrado'}), 404


if __name__ == '__main__':
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    if not os.path.exists(app.config['IMAGEN_FOLDER']):
        os.makedirs(app.config['IMAGEN_FOLDER'])
    if not os.path.exists(app.config['QR_FOLDER']):
        os.makedirs(app.config['QR_FOLDER'])

    app.run(host='0.0.0.0', debug=True, port=4000)

