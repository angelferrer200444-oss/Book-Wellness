const datosEl = document.getElementById('datos-lectura');

window.datosLectura = {
    id_libro: datosEl.dataset.idLibro || null,
    datosCompletos: datosEl.dataset.completos === 'true',
    paginasYaGuardadas: datosEl.dataset.paginasGuardadas === 'true',
    capitulosYaGuardados: datosEl.dataset.capitulosGuardados === 'true'
};

   function activarEdicion() {
    document.getElementById('total').disabled = false;
    document.getElementById('total').style.opacity = '1';
    document.getElementById('capTotal').disabled = false;
    document.getElementById('capTotal').style.opacity = '1';
    document.getElementById('formatoLectura').disabled = false;
    document.getElementById('btnEditar').style.display = 'none';
    document.getElementById('btnGuardar').style.display = 'block';
}

async function guardarEdicion() {
    const paginas = document.getElementById('total').value;
    const caps = document.getElementById('capTotal').value;
    const formato = document.getElementById('formatoLectura').value;

    try {
        await fetch('/api/iniciar_lectura', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                id_libro: window.datosLectura.id_libro,
                paginas_totales: paginas,
                num_caps: caps,
                formato: formato
            })
        });

        // Volver a bloquear
        document.getElementById('total').disabled = true;
        document.getElementById('total').style.opacity = '0.6';
        document.getElementById('capTotal').disabled = true;
        document.getElementById('capTotal').style.opacity = '0.6';
        document.getElementById('formatoLectura').disabled = true;
        document.getElementById('btnGuardar').style.display = 'none';
        document.getElementById('btnEditar').style.display = 'block';

        alert('Datos actualizados correctamente.');
        actualizarProgreso();

    } catch (error) {
        alert('Error al guardar los cambios.');
    }
}