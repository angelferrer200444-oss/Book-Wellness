btnEmpezar.addEventListener('click', async () => {

    const formato = document.getElementById('formatoLectura').value.trim();
    const paginasTotales = document.getElementById('total').value;
    const capTotal = document.getElementById('capTotal').value;

    if (!formato) {
        alert('Por favor selecciona o escribe el formato de lectura.');
        return;
    }

    try {
        await fetch('/api/iniciar_lectura', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                id_libro: window.datosLectura.id_libro,
                paginas_totales: window.datosLectura.paginasYaGuardadas ? null : paginasTotales || null,
                num_caps: window.datosLectura.capitulosYaGuardados ? null : capTotal || null,
                formato: formato
            })
        });
    } catch (error) {
        alert('No se pudieron guardar los datos del libro.');
        return;
    }

    window.location.href = `/seccion2-lectura?id_libro=${window.datosLectura.id_libro}`;
});