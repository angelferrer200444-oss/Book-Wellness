document.addEventListener("DOMContentLoaded", () => {

    const formulario = document.querySelector("form");

    if (!formulario) return;

    formulario.addEventListener("submit", async (e) => {

        e.preventDefault();

        const formData = new FormData(formulario);

        const respuestas = {};

        formData.forEach((valor, clave) => {

            if (clave === "nivel") return;
        
            if (clave.endsWith("[]")) {
        
                const nombreCampo = clave.replace("[]", "");
        
                if (!respuestas[nombreCampo]) {
                    respuestas[nombreCampo] = [];
                }
        
                respuestas[nombreCampo].push(valor);
        
            } else {
        
                respuestas[clave] = valor;
        
            }
        
        });
        
        console.log("Nivel:", formData.get("nivel"));
        console.log("Respuestas:", respuestas);
        
        try {
        
            const respuesta = await fetch("/api/guardar_encuesta", {
        

                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify({

                    nivel: formData.get("nivel"),
                    respuestas: respuestas

                })

            });

            const resultado = await respuesta.json();

            if (!respuesta.ok) {

                alert(resultado.error || "Error al guardar la encuesta.");
                return;

            }

            alert("¡Registro completado correctamente!");

            window.location.href = "/sesion";

        }

        catch (error) {

            console.error(error);

            alert("Ocurrió un error inesperado.");

        }

    });

});



