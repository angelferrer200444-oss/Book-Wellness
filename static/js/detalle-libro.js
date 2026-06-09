document.addEventListener('DOMContentLoaded', function() {

    let yaAgregado = false;

    async function agregarLibro(categoria) {

        if (yaAgregado) return;
        yaAgregado = true;

        const id_usuario = localStorage.getItem('usuario_id');

        if (!id_usuario) {
            alert("Debes iniciar sesión para agregar libros.");
            window.location.href = "/sesion";
            return;
        }

        try {
            const respuesta = await fetch('/api/agregar_libro', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    id_usuario: id_usuario,
                    titulo: datoLibro.titulo,
                    autor: datoLibro.autor,
                    descripcion: datoLibro.descripcion,
                    portada: datoLibro.portada,
                    categoria: categoria,
                     key_libro: datoLibro.key 
                })
            });

            const resultado = await respuesta.json();

            if (respuesta.status === 201) {
                document.getElementById('btn-leyendo').disabled = true;
                document.getElementById('btn-pendiente').disabled = true;
                document.getElementById('btn-leyendo').style.opacity = "0.6";
                document.getElementById('btn-pendiente').style.opacity = "0.6";
                document.getElementById('btn-leyendo').style.cursor = "not-allowed";
                document.getElementById('btn-pendiente').style.cursor = "not-allowed";
                document.getElementById('btn-leyendo').innerText = "✓ Agregado";
                document.getElementById('btn-pendiente').innerText = "✓ Agregado";

            } else if (respuesta.status === 409) {
                yaAgregado = false;
                alert("Este libro ya está en tu lista.");

            } else {
                yaAgregado = false;
                alert(resultado.error || "Error al agregar el libro.");
            }

        } catch (error) {
            yaAgregado = false;
            alert("No hay conexión con el servidor.");
        }
    }

    document.getElementById('btn-leyendo').addEventListener('click', function() {
    agregarLibro('leyendo');
    });

    document.getElementById('btn-pendiente').addEventListener('click', function() {
    agregarLibro('pendiente');
    });

});