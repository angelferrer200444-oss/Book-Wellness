function actualizarProgreso(){

    let total = parseFloat(document.getElementById("total").value) || 0;
    let leido = parseFloat(document.getElementById("leido").value) || 0;

    let capTotal = parseFloat(document.getElementById("capTotal").value) || 0;
    let capLeidos = parseFloat(document.getElementById("capLeidos").value) || 0;

    const barra = document.getElementById("barraProgreso");

    let porcentajePaginas = null;
    let porcentajeCapitulos = null;

    // Calcular páginas
    if(total > 0 && leido >= 0){
        porcentajePaginas = (leido / total) * 100;
    }

    // Calcular capítulos
    if(capTotal > 0 && capLeidos >= 0){
        porcentajeCapitulos = (capLeidos / capTotal) * 100;
    }

    let porcentaje;

    // Ambos sistemas disponibles
    if(porcentajePaginas !== null && porcentajeCapitulos !== null){

        porcentaje =
            (porcentajePaginas + porcentajeCapitulos) / 2;

    }

    // Solo páginas
    else if(porcentajePaginas !== null){

        porcentaje = porcentajePaginas;

    }

    // Solo capítulos
    else if(porcentajeCapitulos !== null){

        porcentaje = porcentajeCapitulos;

    }

    // Nada disponible
    else{

        barra.style.opacity = "0";
        return;

    }

    porcentaje = Math.min(porcentaje, 100);

    barra.style.opacity = "1";
    barra.style.width = porcentaje + "%";
    barra.textContent = porcentaje.toFixed(0) + "%";
}

document.addEventListener('DOMContentLoaded', () => {
    actualizarProgreso();
});

