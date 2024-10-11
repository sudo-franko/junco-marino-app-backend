from flask import Flask
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

app.config['UPLOAD_FOLDER'] = 'uploads'

@app.route('/saludo')
def saludar():
    return "Hola"

if __name__ == '__main__':
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])

    app.run(host='0.0.0.0', debug=True, port=4000)

