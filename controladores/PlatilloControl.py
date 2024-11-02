from flask import Blueprint, request, jsonify, send_from_directory, current_app
from persistencia.Platillo import Platillo
import os

platilloControl = Blueprint('platilloControl', __name__)


def find_file(id, folder):
    if folder == 'categorias':
        filepath = os.path.join(current_app.config['CATEGORIA_FOLDER'], f'{id}.png')
        if os.path.exists(filepath):
            return f'{id}.png'
        return False
    else:
        filepath = os.path.join(current_app.config['IMAGEN_FOLDER'], f'{id}.png')
        if os.path.exists(filepath):
            return f'{id}.png'
        return False


@platilloControl.route('/listarPlatillos')
def listar():
    platillo = Platillo()
    platillos = platillo.listar()
    if platillos:
        if isinstance(platillos, str):
            return jsonify({'error': platillos}), 500
        else:
            return jsonify({'platillos': platillos}), 200
    else:
        return jsonify({'mensaje': 'No hay productos registrados'}), 400


@platilloControl.route('/listarCategorias')
def listarCategorias():
    platillo = Platillo()
    categorias = platillo.listarCategorias()
    if categorias:
        if isinstance(categorias, str):
            return jsonify({'error': categorias}), 500
        else:
            return jsonify({'categorias': categorias}), 200
    else:
        return jsonify({'mensaje': 'No hay productos registrados'}), 400


@platilloControl.route('/imagenPlatillo/<int:platillo_id>', methods=['GET'])
def obtenerImagen(platillo_id):
    filename = find_file(platillo_id, 'platillos')
    if filename:
        return send_from_directory(current_app.config['IMAGEN_FOLDER'], filename)
    else:
        return jsonify({'error': 'Imagen de platillo no encontrado'}), 404


@platilloControl.route('/imagenCategoria/<int:cat_id>', methods=['GET'])
def obtenerImagenCat(cat_id):
    filename = find_file(cat_id, 'categorias')
    if filename:
        return send_from_directory(current_app.config['CATEGORIA_FOLDER'], filename)
    else:
        return jsonify({'error': 'Imagen de platillo no encontrado'}), 404


