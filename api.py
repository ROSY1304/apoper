from flask import Flask, jsonify, request, send_from_directory
import os
import nbformat
from flask_cors import CORS

app = Flask(__name__, static_folder='static')

CORS(app)

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

            # Filtrar celdas específicas
            celdas_interes = [113, 126]
            resultados_accuracy = []

            for idx, cell in enumerate(notebook_content.cells, start=1):
                if idx in celdas_interes and cell.cell_type == 'code':
                    for output in cell.outputs:
                        if 'text' in output and 'Accuracy' in output['text']:
                            resultados_accuracy.append(output['text'].strip())

            if not resultados_accuracy:
                return jsonify({'mensaje': 'No se encontraron valores de Accuracy en las celdas seleccionadas.'}), 404

            return jsonify(resultados_accuracy), 200
        else:
            return jsonify({'mensaje': 'Archivo no encontrado o formato incorrecto'}), 404
    except Exception as e:
        return jsonify({'mensaje': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
