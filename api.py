from flask import Flask, jsonify, send_from_directory
import os
from flask_cors import CORS

app = Flask(__name__, static_folder='static')

# Habilitar CORS para la aplicación completa
CORS(app)

# Directorio donde están los documentos .ipynb
DOCUMENTS_FOLDER = 'documentos'
app.config['DOCUMENTS_FOLDER'] = DOCUMENTS_FOLDER

@app.route('/')
def home():
    return send_from_directory('static', 'index.html')

@app.route('/documentos', methods=['GET'])
def obtener_documentos():
    try:
        archivos = [f for f in os.listdir(DOCUMENTS_FOLDER) if f.endswith('.ipynb')]
        
        if not archivos:
            return jsonify({"mensaje": "No hay archivos .ipynb en el directorio."}), 404
        
        return jsonify(archivos), 200
    except FileNotFoundError:
        return jsonify({"mensaje": "No se encontró el directorio de documentos"}), 404

@app.route('/documentos/contenido/<nombre>', methods=['GET'])
def ver_contenido_documento(nombre):
    try:
        # Caso especial: Mostrar solo la imagen para "Arboles de decision.ipynb"
        if nombre.lower() == "arboles de decision.ipynb":
            ruta_imagen = '/static/grafico.png'  # Ruta relativa a la carpeta estática
            return jsonify({
                'tipo': 'imagen',
                'contenido': ruta_imagen
            }), 200

        # Para otros notebooks, devolver mensaje de no procesado
        return jsonify({'mensaje': 'No se procesa este archivo.'}), 404

    except Exception as e:
        return jsonify({'mensaje': str(e)}), 500


# Iniciar la aplicación
if __name__ == '__main__':
    app.run(debug=True)
