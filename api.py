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
                            elif 'data' in output:
                                # Revisar si hay salida de imagen u otro tipo de datos
                                if 'image/png' in output['data']:
                                    salidas.append({
                                        'tipo': 'imagen',
                                        'contenido': output['data']['image/png']
                                    })
                                elif 'application/json' in output['data']:
                                    salidas.append({
                                        'tipo': 'json',
                                        'contenido': output['data']['application/json']
                                    })
                                elif 'text/html' in output['data']:
                                    salidas.append({
                                        'tipo': 'html',
                                        'contenido': output['data']['text/html']
                                    })

            # Caso para "arboles.ipynb" - Solo mostrar el gráfico (imagen)
            elif nombre.lower() == "arboles.ipynb":
                for cell in notebook_content.cells:
                    if cell.cell_type == 'code':
                        # Solo procesar las salidas de imagen (gráfico)
                        for output in cell.outputs:
                            if 'data' in output and 'image/png' in output['data']:
                                salidas.append({
                                    'tipo': 'imagen',
                                    'contenido': output['data']['image/png']
                                })

            # Si no hay salidas relevantes
            if not salidas:
                return jsonify({'mensaje': 'No se encontraron salidas relevantes o de gráficos.'}), 404

            return jsonify(salidas), 200
        else:
            return jsonify({'mensaje': 'Archivo no encontrado o formato incorrecto'}), 404
    except Exception as e:
        return jsonify({'mensaje': str(e)}), 500
