document.addEventListener(
    "DOMContentLoaded",
    () => cargarRecomendaciones()
);


async function cargarRecomendaciones(
    recomendacionesNuevas = null
) {

    const contenedor =
        document.getElementById("recomendaciones");


    /*
     * Mostrar cargando
     */
    contenedor.innerHTML = `
        <div class="loader-container">
            <div class="loader"></div>

            <span id="texto-carga">
                Generando recomendaciones...
            </span>
        </div>
    `;


    try {

        let libros;


        /*
         * Si Reflexivo ya nos entregó
         * las recomendaciones, usamos esas.
         *
         * NO hacemos otro fetch.
         *
         * Así evitamos llamar nuevamente
         * al recomendador.
         */
        if (
            recomendacionesNuevas &&
            recomendacionesNuevas.length > 0
        ) {

            libros = recomendacionesNuevas;

        } else {

            /*
             * Carga normal de la página.
             *
             * Aquí solamente obtenemos
             * las recomendaciones guardadas
             * en cache.
             */
            const respuesta = await fetch(
                "/api/recomendaciones"
            );

            if (!respuesta.ok) {

                throw new Error(
                    "No se pudieron obtener las recomendaciones."
                );

            }

            libros = await respuesta.json();

        }


        console.log(
            "Recomendaciones para mostrar:",
            libros
        );


        /*
         * Limpiar loader
         */
        contenedor.innerHTML = "";


        /*
         * Crear tarjetas
         */
        libros.forEach(libro => {

            const card =
                document.createElement("div");

            card.className = "book-card";

            card.style.cursor = "pointer";


            card.addEventListener(
                "click",
                () => {

                    if (libro.id_google) {

                        window.location.href =
                            `/libro?id_google=${encodeURIComponent(
                                libro.id_google
                            )}&portada=${encodeURIComponent(
                                libro.portada
                            )}`;

                    } else {

                        window.location.href =
                            `/libro?clave=${encodeURIComponent(
                                libro.key
                            )}&portada=${encodeURIComponent(
                                libro.portada
                            )}`;

                    }

                }
            );


            const imagen =
                document.createElement("img");


            imagen.src =
                libro.portada;

            imagen.alt =
                libro.titulo;

            imagen.title =
                libro.titulo;

            imagen.loading =
                "lazy";


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
