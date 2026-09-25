document.addEventListener("DOMContentLoaded", cargarLogros);


async function cargarLogros() {

    // Elementos de carga y contenedor de logros
    const loader = document.getElementById("logros-loader");
    const contenedor = document.getElementById(
        "simulation-goals-container"
    );

    try {

        // Mientras se calculan los logros:
        // loader visible y logros ocultos.
        if (loader) {
            loader.style.display = "flex";
        }

        if (contenedor) {
            contenedor.style.display = "none";
        }


        // Obtener los logros calculados por el servidor
        const respuesta = await fetch("/api/logros");

        if (!respuesta.ok) {
            throw new Error(
                "No fue posible obtener los logros."
            );
        }


        const datos = await respuesta.json();


        // Actualizar cada logro con los datos calculados
        datos.forEach(logro => {

            const tarjeta = document.querySelector(
                `[data-logro="${logro.id}"]`
            );

            if (!tarjeta) {
                return;
            }


            const filas = tarjeta.querySelectorAll(
                ".diagram-row"
            );

            let progreso = null;


            filas.forEach(fila => {

                const campo = fila.querySelector(
                    ".diag-field"
                );

                if (
                    campo &&
                    campo.textContent.trim().toLowerCase() ===
                    "progreso"
                ) {

                    progreso = fila.querySelector(
                        ".diag-value"
                    );

                }

            });


            const barra = tarjeta.querySelector(
                ".progress-bar"
            );

            const porcentaje = tarjeta.querySelector(
                ".diag-status"
            );


            // Actualizar progreso
            if (progreso) {

                progreso.textContent =
                    `${logro.progreso} / ${logro.objetivo}`;

            }


            // Actualizar barra
            if (barra) {

                barra.style.width =
                    `${logro.porcentaje}%`;

            }


            // Actualizar porcentaje y estado
            if (porcentaje) {

                porcentaje.textContent =
                    `${logro.porcentaje}%`;


                if (logro.completado) {

                    porcentaje.classList.remove(
                        "status-pending"
                    );

                    porcentaje.classList.add(
                        "status-success"
                    );


                    if (barra) {

                        barra.classList.add(
                            "bar-success"
                        );

                    }

                } else {

                    porcentaje.classList.remove(
                        "status-success"
                    );

                    porcentaje.classList.add(
                        "status-pending"
                    );


                    if (barra) {

                        barra.classList.remove(
                            "bar-success"
                        );

                    }

                }

            }

        });


        // Los logros solamente se muestran
        // después de terminar todos los cálculos.
        if (loader) {
            loader.style.display = "none";
        }

        if (contenedor) {
            contenedor.style.display = "";
        }


    } catch (error) {

        console.error(
            "Error al cargar los logros:",
            error
        );


        // Si ocurre un error, los logros permanecen ocultos.
        if (contenedor) {
            contenedor.style.display = "none";
        }

        if (loader) {
            loader.style.display = "flex";
        }

    }

}






