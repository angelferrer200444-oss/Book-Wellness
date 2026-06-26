document.addEventListener('DOMContentLoaded', () => {

    const frases = [

        "Buscando ejemplares...",
        "Consultando biblioteca...",
        "Explorando catálogo...",
        "Revisando estanterías...",
        "Buscando nuevas lecturas...",
        "Recuperando información...",
        "Organizando colección...",
        "Abriendo catálogo..."

    ];

    const texto = document.getElementById("texto-carga-cabecera");

    if(texto){

        texto.textContent =
            frases[Math.floor(Math.random() * frases.length)];

    }

    cargarResultados();

});

async function cargarResultados(){

    try{

        const params = new URLSearchParams(window.location.search);

        const consulta =
            params.get("q") ||
            params.get("genero") ||
            "";


        const respuesta = await fetch(
            `/api/buscar?q=${encodeURIComponent(consulta)}`
        );

        const libros = await respuesta.json();

        mostrarResultados(consulta, libros);

    }

    catch(error){

        console.error(error);

        document.getElementById("contenedor-resultados").innerHTML = `
            <h2>Error al cargar resultados</h2>
        `;

    }

}

function mostrarResultados(consulta, libros){

    let html = `

        <div class="results-container">

            <div class="results-header">

                <h2>
                    Resultados para "${consulta}"
                </h2>

                <span class="results-count">
                    ${libros.length} libros encontrados
                </span>

            </div>

            <div class="results-shelf">

                <div class="books-grid">
    `;

    libros.forEach(libro => {

        html += `

        <a href="/libro?id_google=${encodeURIComponent(libro.id_google || "")}&clave=${encodeURIComponent(libro.key || "")}&portada=${encodeURIComponent(libro.portada)}"
        class="book-link">
        

                <div class="book-card result-card">

                    <img
                        src="${libro.portada}"
                        alt="${libro.titulo}"
                    >

                    <div class="book-info">

                        <p class="book-title-card">
                            ${libro.titulo}
                        </p>

                    </div>

                </div>

            </a>

        `;

    });

    html += `

                </div>

                <div class="shelf"></div>

            </div>

        </div>

    `;

    document.getElementById("contenedor-resultados").innerHTML = html;

}
