/* ==========================================================
   SELECCIONAR PREGUNTA ALEATORIA
========================================================== */

const preguntasAleatorias = document.querySelectorAll(".aleatoria");

// Ocultamos todas
preguntasAleatorias.forEach(pregunta => {
    pregunta.style.display = "none";
});

// Elegimos una al azar
const indiceAleatorio = Math.floor(
    Math.random() * preguntasAleatorias.length
);

const preguntaAleatoria = preguntasAleatorias[indiceAleatorio];

// La mostramos
preguntaAleatoria.style.display = "";

/* ==========================================================
   OBTENER SOLO LAS PREGUNTAS VISIBLES
========================================================== */

const preguntas = Array.from(
    document.querySelectorAll(".pregunta")
).filter(pregunta => {

    return pregunta.style.display !== "none";

});

const puntos = document.querySelectorAll(".punto");

const btnContinuar =
    document.getElementById("btnContinuar");

const btnAtras =
    document.getElementById("btnAtras");

const btnMenu =
    document.getElementById("btnMenu");

let actual = 0;

/* ==========================================================
   ACTUALIZAR INTERFAZ
========================================================== */

function actualizarInterfaz() {

    preguntas.forEach(pregunta => {

        pregunta.classList.remove("activa");

    });

    puntos.forEach(punto => {

        punto.classList.remove("activo");

    });

    preguntas[actual].classList.add("activa");

    puntos[actual].classList.add("activo");

    btnAtras.style.visibility =
        actual === 0
            ? "hidden"
            : "visible";

    btnContinuar.textContent =
        actual === preguntas.length - 1
            ? "Finalizar"
            : "Continuar";

}

/* ==========================================================
   FINALIZAR REFLEXIÓN
========================================================== */

async function finalizarReflexion() {

    const params =
        new URLSearchParams(window.location.search);

    const id_libro =
        params.get("id_libro");

    const segundosTotal =
        parseInt(
            localStorage.getItem("tiempo_lectura") || 0
        );

    const tiempo_minutos =
        Math.floor(segundosTotal / 60);

    const paginaActual =
        parseInt(
            document.getElementById("paginaActual").value
        ) || window.paginaAnterior;

    const paginasLeidasSesion =
        Math.max(
            0,
            paginaActual - window.paginaAnterior
        );

    const capitulosLeidosHoy =
        parseInt(
            document.getElementById("capitulosHoy").value
        ) || 0;

    const continuar =
        document.getElementById(
            "continuarLectura"
        ).value;

    const estadoAnimo =
        document.getElementById(
            "estadoAnimo"
        ).value;

    const notas =
        document.getElementById(
            "notas"
        ).value;

    const respuestaAleatoria =
        preguntaAleatoria.querySelector(
            ".respuestaAleatoria"
        ).value;

    const idPreguntaAleatoria =
        preguntaAleatoria.dataset.id;
        try {

            const resp = await fetch("/api/guardar_lectura", {
    
                method: "POST",
    
                headers: {
    
                    "Content-Type": "application/json"
    
                },
    
                body: JSON.stringify({
    
                    id_libro: id_libro,
    
                    tiempo_minutos: tiempo_minutos,
    
                    estado: continuar,
    
                    fecha_fin: new Date()
                        .toISOString()
                        .split("T")[0],
    
                    paginas_leidas: paginasLeidasSesion,
    
                    pagina_actual: paginaActual,
    
                    capitulos_leidos: capitulosLeidosHoy,
    
                    estado_animo: estadoAnimo,
    
                    notas: notas,
    
                    tipo_reflexion: idPreguntaAleatoria,

                    respuesta_reflexion: respuestaAleatoria

    
                })
    
            });
    
            const data = await resp.json();
    
            console.log(
                "RESPUESTA SERVIDOR:",
                resp.status,
                data
            );
    
            localStorage.removeItem(
                "tiempo_lectura"
            );
    
            window.location.href = "/";
    
        }
    
        catch (error) {
    
            console.error(error);
    
            alert(
                "Error al guardar la lectura."
            );
    
        }
    
    }
    
    /* ==========================================================
       CONTINUAR
    ========================================================== */
    
    btnContinuar.addEventListener("click", () => {
    
        if (actual === preguntas.length - 1) {
    
            finalizarReflexion();
    
            return;
    
        }
    
        actual++;
    
        actualizarInterfaz();
    
    });
    
    /* ==========================================================
       ATRÁS
    ========================================================== */
    
    btnAtras.addEventListener("click", () => {
    
        if (actual === 0) {
    
            return;
    
        }
    
        actual--;
    
        actualizarInterfaz();
    
    });
    
    /* ==========================================================
       MENÚ
    ========================================================== */
    
    btnMenu.addEventListener("click", () => {
    
        const salir = confirm(
    
            "¿Deseas volver al menú principal? Se perderán los cambios no guardados."
    
        );
    
        if (salir) {
    
            window.location.href = "/";
    
        }
    
    });
    
    /* ==========================================================
       INICIO
    ========================================================== */
    
    actualizarInterfaz();
    
