document.addEventListener("DOMContentLoaded", () => {

    const tarjetas = document.querySelectorAll(".bw-card");

    tarjetas.forEach(tarjeta => {

        tarjeta.addEventListener("click", () => {

            const estado = tarjeta.dataset.estado;

            console.log("Estado:", estado);

            fetch("/api/estado_animo_actual", {

                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify({
                    estado: estado
                })

            })

            .then(respuesta => respuesta.json())

            .then(datos => {

                console.log(datos.mensaje);

            })

            .catch(error => {

                console.error("Error:", error);

            });

        });

    });

});
