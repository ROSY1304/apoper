document.addEventListener('DOMContentLoaded', () => {
    const notebooksList = document.getElementById('notebooks-list');
    const contentDiv = document.getElementById('content');

    async function obtenerDocumentos() {
        try {
            const response = await fetch('/documentos');
            const documentos = await response.json();

            if (!response.ok) {
                notebooksList.innerHTML = `<li>${documentos.mensaje}</li>`;
                return;
            }

            notebooksList.innerHTML = '';

            documentos.forEach(doc => {
                const listItem = document.createElement('li');
                listItem.innerText = doc;
                listItem.onclick = () => cargarContenidoNotebook(doc);
                notebooksList.appendChild(listItem);
            });
        } catch (error) {
            console.error('Error obteniendo documentos:', error);
        }
    }

    async function cargarContenidoNotebook(nombre) {
        try {
            const response = await fetch(`/documentos/contenido/${nombre}`);
            const contenido = await response.json();
            contentDiv.innerHTML = '';

            if (!response.ok) {
                contentDiv.innerHTML = `<p>${contenido.mensaje}</p>`;
                return;
            }

            contenido.forEach(cell => {
                const resultDiv = document.createElement('div');
                resultDiv.className = 'result';

                if (cell.tipo === 'texto') {
                    resultDiv.innerText = cell.contenido;
                } else if (cell.tipo === 'imagen') {
                    const img = document.createElement('img');
                    img.src = 'data:image/png;base64,' + cell.contenido;
                    img.className = 'image';
                    resultDiv.appendChild(img);
                } else if (cell.tipo === 'html') {
                    resultDiv.innerHTML = cell.contenido;
                }

                contentDiv.appendChild(resultDiv);
            });
        } catch (error) {
            console.error(`Error cargando el contenido del notebook ${nombre}:`, error);
        }
    }

    // Llama a la función para obtener los documentos al cargar la página
    obtenerDocumentos();
});
