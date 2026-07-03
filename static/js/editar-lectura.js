const datosEl = document.getElementById('datos-lectura');

window.datosLectura = {
    id_libro: datosEl.dataset.idLibro || null,
    datosCompletos: datosEl.dataset.completos === 'true',
    paginasYaGuardadas: datosEl.dataset.paginasGuardadas === 'true',
    capitulosYaGuardados: datosEl.dataset.capitulosGuardados === 'true'
};

function activarEdicion() {
    // Datos del libro
    document.getElementById('total').disabled = false;
    document.getElementById('total').style.opacity = '1';
    document.getElementById('capTotal').disabled = false;
    document.getElementById('capTotal').style.opacity = '1';
    document.getElementById('formatoLectura').disabled = false;
    document.getElementById('formatoLectura').style.opacity = '1';
    document.getElementById('fechaInicio').disabled = false;
    document.getElementById('fechaInicio').style.opacity = '1';
    document.getElementById('fechaLimite').disabled = false;


    // Progreso de lectura
    document.getElementById('leido').disabled = false;
    document.getElementById('leido').style.opacity = '1';
    document.getElementById('capLeidos').disabled = false;
    document.getElementById('capLeidos').style.opacity = '1';

    document.getElementById('btnEditar').style.display = 'none';
    document.getElementById('btnGuardar').style.display = 'block';
}

async function guardarEdicion() {

    
    const paginas = document.getElementById('total').value;
    const caps = document.getElementById('capTotal').value;
    const formato = document.getElementById('formatoLectura').value;
    const paginasLeidas = document.getElementById('leido').value;
    const capLeidos = document.getElementById('capLeidos').value;
    const fechaInicio = document.getElementById('fechaInicio') ? document.getElementById('fechaInicio').value : null;

    try {
        // Guardar datos del libro
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

        // Guardar progreso de lectura
        await fetch('/api/actualizar_progreso', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                id_libro: window.datosLectura.id_libro,
                pagina_actual: paginasLeidas,
                capitulos_leidos: capLeidos,
                fecha_inicio: fechaInicio
            })
        });

        // Volver a bloquear todos los campos
        document.getElementById('total').disabled = true;
        document.getElementById('total').style.opacity = '0.6';
        document.getElementById('capTotal').disabled = true;
        document.getElementById('capTotal').style.opacity = '0.6';
        document.getElementById('formatoLectura').disabled = true;
        document.getElementById('formatoLectura').style.opacity = '0.6';
        document.getElementById('leido').disabled = true;
        document.getElementById('leido').style.opacity = '0.6';
        document.getElementById('capLeidos').disabled = true;
        document.getElementById('capLeidos').style.opacity = '0.6';
        document.getElementById('fechaInicio').disabled = true;
        document.getElementById('fechaInicio').style.opacity = '0.6';

        document.getElementById('btnGuardar').style.display = 'none';
        document.getElementById('btnEditar').style.display = 'block';

        alert('Datos actualizados correctamente.');
        actualizarProgreso();

    } catch (error) {
        alert('Error al guardar los cambios.');
    }
}