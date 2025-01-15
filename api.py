from flask import Flask, jsonify, request, send_from_directory, url_for
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

            salidas = []
            # Caso para "regresion.ipynb" - Filtrar solo las salidas relacionadas con accuracy
            if nombre.lower() == "regresion.ipynb":
                for cell in notebook_content.cells:
                    if cell.cell_type == 'code':
                        # Procesar las salidas de la celda de código y buscar "accuracy"
                        for output in cell.outputs:
                            if 'text' in output and 'accuracy' in output['text'].lower():
                                salidas.append({
                                    'tipo': 'texto',
                                    'contenido': output['text']
                                })

            # Caso para "Arboles de decision.ipynb" - Mostrar todas las salidas y la imagen
            elif nombre.lower() == "arboles de decision.ipynb":
                for cell in notebook_content.cells:
                    if cell.cell_type == 'code':
                        # Procesar todas las salidas de la celda de código
                        for output in cell.outputs:
                            if 'text' in output:
                                salidas.append({
                                    'tipo': 'texto',
                                    'contenido': output['text']
                                })
                # Agregar la imagen como parte de la respuesta
                ruta_imagen = '/static/grafico.png'  # Ruta relativa a la carpeta estática
                salidas.append({
                    'tipo': 'imagen',
                    'contenido': ruta_imagen
                })

            # Si no hay salidas relevantes
            if not salidas:
                return jsonify({'mensaje': 'No se encontraron salidas relevantes o de accuracy.'}), 404

            return jsonify(salidas), 200
        else:
            return jsonify({'mensaje': 'Archivo no encontrado o formato incorrecto'}), 404
    except Exception as e:
        return jsonify({'mensaje': str(e)}), 500


# Iniciar la aplicación
if __name__ == '__main__':
    app.run(debug=True)
