function actualizarFormato() {

    const formato = document
        .getElementById("formatoLectura")
        .value
        .toLowerCase();

    const labelTotal = document.getElementById("labelTotal");
    const labelLeido = document.getElementById("labelLeido");
    const labelCapLeidos = document.getElementById("labelCapLeidos");
    const labelTiempo = document.getElementById("labelTiempo");

    const total = document.getElementById("total");
    const leido = document.getElementById("leido");

    if (formato.includes("audio")) {

        labelTotal.textContent = "Duración Total (min):";
        labelLeido.textContent = "Minutos Escuchados:";
        labelCapLeidos.textContent = "Capítulos Escuchados:";
        labelTiempo.textContent = "Tiempo de Escucha:";

        total.placeholder = "720";
        leido.placeholder = "350";

    } else {

        labelTotal.textContent = "Páginas Totales:";
        labelLeido.textContent = "Páginas Leídas:";
        labelCapLeidos.textContent = "Capítulos Leídos:";
        labelTiempo.textContent = "Tiempo Leído:";

        total.placeholder = "500";
        leido.placeholder = "250";
    }
}