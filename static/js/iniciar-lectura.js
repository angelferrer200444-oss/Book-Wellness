document.addEventListener('DOMContentLoaded', () => {

    const btnEmpezar = document.getElementById('btnEmpezar');

    btnEmpezar.addEventListener('click', async () => {

        const formato = document.getElementById('formatoLectura').value.trim();
        const paginasTotales = document.getElementById('total').value;
        const capTotal = document.getElementById('capTotal').value;

        // Validar solo los campos que aún no estaban guardados
        if (!window.datosLectura.paginasYaGuardadas && !paginasTotales) {
            alert('Por favor ingresa el número de páginas totales del libro.');
            return;
        }

        if (!window.datosLectura.capitulosYaGuardados && !capTotal) {
            alert('Por favor ingresa el número de capítulos totales del libro.');
            return;
        }

        if (!formato) {
            alert('Por favor selecciona o escribe el formato de lectura.');
            return;
        }

        // Si no estaba completo, guardamos los datos nuevos
        if (!window.datosLectura.datosCompletos) {

            try {

                await fetch('/api/iniciar_lectura', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        id_libro: window.datosLectura.id_libro,
                        paginas_totales: window.datosLectura.paginasYaGuardadas ? null : paginasTotales,
                        num_caps: window.datosLectura.capitulosYaGuardados ? null : capTotal,
                        formato: formato
                    })
                });

            } catch (error) {
                alert('No se pudieron guardar los datos del libro.');
                return;
            }
        }

        // Avanzar al cronómetro
        window.location.href = `/seccion2-lectura?id_libro=${window.datosLectura.id_libro}`;
    });

});
