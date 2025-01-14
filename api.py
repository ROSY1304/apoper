from flask import Flask, jsonify, request, send_from_directory, render_template
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

            accuracy_results = []
            decision_tree_result = None
            for index, cell in enumerate(notebook_content.cells):
                if cell.cell_type == 'code':
                    for output in cell.outputs:
                        if 'text' in output:
                            lines = output['text'].split('\n')
                            for line in lines:
                                if 'accuracy' in line.lower():
                                    accuracy_results.append(line.strip())
                                if nombre == 'decision_tree.ipynb' and index == 38:
                                    if 'image/png' in output['data']:
                                        decision_tree_result = output['data']['image/png']
            
            if nombre == 'decision_tree.ipynb' and decision_tree_result:
                return jsonify({'resultado': decision_tree_result}), 200
            elif not accuracy_results:
                return jsonify({'mensaje': 'No se encontraron resultados de accuracy en el notebook'}), 404
            else:
                return jsonify(accuracy_results), 200
        else:
            return jsonify({'mensaje': 'Archivo no encontrado o formato incorrecto'}), 404
    except Exception as e:
        return jsonify({'mensaje': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
