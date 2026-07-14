document.addEventListener("DOMContentLoaded", cargarRecomendaciones);

async function cargarRecomendaciones() {

    const contenedor = document.getElementById("recomendaciones");

    contenedor.innerHTML = `
        <div class="loader-container">

            <div class="loader"></div>

            <span id="texto-carga">
                Generando recomendaciones...
            </span>

        </div>
    `;

    try {

        const respuesta = await fetch("/api/recomendaciones");

        if (!respuesta.ok) {
            throw new Error("No se pudieron obtener las recomendaciones.");
        }

        const libros = await respuesta.json();

        console.log(libros);

        contenedor.innerHTML = "";

        libros.forEach(libro => {

            const card = document.createElement("div");
            card.className = "book-card";
            card.style.cursor = "pointer";

            card.addEventListener("click", () => {

                if (libro.id_google) {
            
                    window.location.href =
                        `/libro?id_google=${encodeURIComponent(libro.id_google)}&portada=${encodeURIComponent(libro.portada)}`;
            
                } else {
            
                    window.location.href =
                        `/libro?clave=${encodeURIComponent(libro.key)}&portada=${encodeURIComponent(libro.portada)}`;
            
                }
            
            });
            

            const imagen = document.createElement("img");

            imagen.src = libro.portada;
            imagen.alt = libro.titulo;
            imagen.title = libro.titulo;
            imagen.loading = "lazy";

            card.appendChild(imagen);

            contenedor.appendChild(card);

        });

    }

    catch (error) {

        console.error(error);

        contenedor.innerHTML = `
            <div class="loader-container">

                <span id="texto-carga">
                    No fue posible cargar las recomendaciones.
                </span>

            </div>
        `;

    }

}
