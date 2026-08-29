document.addEventListener("DOMContentLoaded", cargarLogros);

async function cargarLogros() {
    try {
        const respuesta = await fetch("/api/logros");

        if (!respuesta.ok) {
            throw new Error("No fue posible obtener los logros.");
        }

        const datos = await respuesta.json();

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
                    campo.textContent.trim().toLowerCase() === "progreso"
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

            if (progreso) {
                progreso.textContent =
                    `${logro.progreso} / ${logro.objetivo}`;
            }

            if (barra) {
                barra.style.width =
                    `${logro.porcentaje}%`;
            }

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

    } catch (error) {
        console.error(
            "Error al cargar los logros:",
            error
        );
    }
}