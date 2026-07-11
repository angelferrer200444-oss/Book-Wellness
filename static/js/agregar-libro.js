document.addEventListener('DOMContentLoaded', () => {

    // Obtener categoría de la URL
    const params = new URLSearchParams(window.location.search);
    const categoria = params.get('categoria') || 'pendiente';

    document.querySelector('.save-book-btn').addEventListener('click', async () => {

        const titulo = document.getElementById('book-title').value.trim();
        const autor = document.getElementById('book-author').value.trim();

        if (!titulo || !autor) {
            alert('El título y el autor son obligatorios.');
            return;
        }

        const formData = new FormData();
        formData.append('titulo', titulo);
        formData.append('autor', autor);
        formData.append('descripcion', document.getElementById('book-subtitle-field').value);
        formData.append('paginas', document.getElementById('book-pages').value);
        formData.append('capitulos', document.getElementById('book-chapters').value);
        formData.append('anio', document.getElementById('book-published').value);
        formData.append('genero', document.getElementById('book-genres').value);
        formData.append('formato', document.getElementById('book-type').value);
        formData.append('categoria', categoria);

        const portada = document.getElementById('book-cover').files[0];
        if (portada) {
            formData.append('portada', portada);
        }

        try {
            const respuesta = await fetch('/api/agregar_libro_manual', {
                method: 'POST',
                body: formData
            });

            const resultado = await respuesta.json();

            if (respuesta.status === 201) {
                alert('¡Libro agregado correctamente!');
                window.location.href = '/';
            } else {
                alert(resultado.error || 'Error al agregar el libro.');
            }

        } catch (error) {
            alert('No hay conexión con el servidor.');
        }
    });
});