from flask import Flask, jsonify, request, send_from_directory
import os
import nbformat
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
        notebook_path = os.path.join(DOCUMENTS_FOLDER, nombre)

        if os.path.exists(notebook_path) and nombre.endswith('.ipynb'):
            with open(notebook_path, 'r', encoding='utf-8') as f:
                notebook_content = nbformat.read(f, as_version=4)

            contenido = []
            # Recolectar todos los resultados sin mostrar código
            for cell in notebook_content.cells:
                if cell.cell_type == 'code':
                    for output in cell.outputs:
                        if 'text' in output:
                            contenido.append({
                                'titulo': 'Resultado (Texto)',
                                'tipo': 'texto',
                                'contenido': output['text']
                            })
                        elif 'data' in output:
                            if 'text/plain' in output['data']:
                                contenido.append({
                                    'titulo': 'Resultado (Texto)',
                                    'tipo': 'texto',
                                    'contenido': output['data']['text/plain']
                                })
                            if 'image/png' in output['data']:
                                contenido.append({
                                    'titulo': 'Resultado (Imagen)',
                                    'tipo': 'imagen',
                                    'contenido': output['data']['image/png']
                                })

            return jsonify(contenido), 200
        else:
            return jsonify({'mensaje': 'Archivo no encontrado o formato incorrecto'}), 404
    except Exception as e:
        return jsonify({'mensaje': str(e)}), 500

# Iniciar la aplicación
if __name__ == '__main__':
    app.run(debug=True)
