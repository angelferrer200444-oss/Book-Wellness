document.addEventListener('click', function(e) {
    if (e.target.classList.contains('btn-eliminar')) {
        const id_libro = e.target.getAttribute('data-id');
        eliminarLibro(id_libro);
    }
});

async function eliminarLibro(id_libro) {
    const id_usuario = localStorage.getItem('usuario_id');
    
    if (!confirm("¿Eliminar este libro de tu lista?")) return;

    try {
        const respuesta = await fetch('/api/eliminar_libro', {
            method: 'DELETE',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ id_libro, id_usuario })
        });

        if (respuesta.status === 200) {
            window.location.reload();
        } else {
            alert("Error al eliminar el libro.");
        }
    } catch (error) {
        alert("No hay conexión con el servidor.");
    }
}