document.getElementById("formulario-registro").addEventListener("submit", async (e) => {

    e.preventDefault();

    const nombre = document.getElementById("nombre").value;
    const correo = document.getElementById("correo").value;
    const password = document.getElementById("password").value;
    const nivelLectura = document.getElementById("nivel").value;
    const alerta = document.getElementById("mensaje-alerta");

    const emailValido = /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(correo);

    if (!emailValido) {

        alerta.style.color = "red";
        alerta.innerText = "Por favor ingresa un correo electrónico válido.";
        return;

    }

    const datosUsuario = {
        nombre,
        correo,
        password,
        nivel: nivelLectura
    };

    try {

        const respuesta = await fetch("/api/registrar_usuario", {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify(datosUsuario)

        });

        const resultado = await respuesta.json();

        console.log("Respuesta del servidor:");
        console.log(resultado);

        if (!respuesta.ok) {

            alerta.style.color = "red";
            alerta.innerText = resultado.error || "Error al registrar.";
            return;

        }

        sessionStorage.setItem(
            "id_usuario_temporal",
            resultado.id_asignado
        );

        alert("ID guardado: " + sessionStorage.getItem("id_usuario_temporal"));

        document.addEventListener("DOMContentLoaded", () => {

    const formulario = document.querySelector("form");

    if (!formulario) return;

    formulario.addEventListener("submit", async (e) => {

        e.preventDefault();

        const idUsuario = sessionStorage.getItem("id_usuario_temporal");

        if (!idUsuario) {

            alert("No se encontró el usuario registrado.");
            return;

        }

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

            }
            else {

                respuestas[clave] = valor;

            }

        });

        try {

            const respuesta = await fetch("/api/guardar_encuesta", {

                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify({

                    id_usuario: idUsuario,
                    nivel: formData.get("nivel"),
                    respuestas: respuestas

                })

            });

            const resultado = await respuesta.json();

            if (!respuesta.ok) {

                alert(resultado.error || "Error al guardar la encuesta.");
                return;

            }

            sessionStorage.removeItem("id_usuario_temporal");

            alert("¡Registro completado correctamente!");

            window.location.href = "/sesion";

        }

        catch (error) {

            console.error(error);

            alert("Ocurrió un error inesperado.");

        }

    });

});


        console.log("ID guardado:", resultado.id_asignado);
        console.log(
            "ID en sessionStorage:",
            sessionStorage.getItem("id_usuario_temporal")
        );

        alerta.style.color = "green";
        alerta.innerText = resultado.mensaje;

        setTimeout(() => {

            if (nivelLectura === "principiante") {

                window.location.href = "/formulario-principiante";

            }
            else if (nivelLectura === "intermedio") {

                window.location.href = "/formulario-intermedio";

            }
            else {

                window.location.href = "/formulario-experto";

            }

        }, 1200);

    }

    catch (error) {

        console.error(error);

        alerta.style.color = "red";
        alerta.innerText = "No hay conexión con el servidor.";

    }

});
