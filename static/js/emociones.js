document.addEventListener("DOMContentLoaded", () => {

    const tarjetas = document.querySelectorAll(".bw-card");

    tarjetas.forEach(tarjeta => {

        tarjeta.addEventListener("click", () => {

            const estado = tarjeta.dataset.estado;

            console.log("Estado:", estado);
            
            const respuesta = document.getElementById("bwAiResponse");

            respuesta.value = "Pensando...";

            respuesta.style.height = "auto";

            const maxHeight = 180;

            if(respuesta.scrollHeight > maxHeight){

                respuesta.style.height = maxHeight + "px";
                respuesta.style.overflowY = "auto";

            }else{

                respuesta.style.height = respuesta.scrollHeight + "px";
                respuesta.style.overflowY = "hidden";

            }

            fetch("/api/estado_animo_actual", {

                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify({
                    estado: estado
                })

            })

            .then(async respuestaServidor => {

                const datos = await respuestaServidor.json();
            
                if (!respuestaServidor.ok) {
            
                    throw new Error(
                        datos.error ||
                        "No fue posible generar la respuesta."
                    );
            
                }
            
                return datos;
            
            })
            
            .then(async datos => {
            

                console.log(datos);
                console.log("Tipo:", typeof datos.recomendaciones);
                console.log("Valor:", datos.recomendaciones);
                console.log("Longitud:", datos.recomendaciones?.length);

                console.log(datos.respuesta_ia);

                const respuesta = document.getElementById("bwAiResponse");

                console.log("Textarea:", respuesta);

                if(respuesta && datos.respuesta_ia){

                    respuesta.value = datos.respuesta_ia;

                    respuesta.style.height = "auto";

                    const maxHeight = 180;

                    if(respuesta.scrollHeight > maxHeight){

                        respuesta.style.height = maxHeight + "px";
                        respuesta.style.overflowY = "auto";

                    }else{

                        respuesta.style.height = respuesta.scrollHeight + "px";
                        respuesta.style.overflowY = "hidden";

                    }

                }
                
                if (
                    (estado === "Reflexivo" || estado === "Sorprendido"|| estado === "Ansioso" ) &&
                    datos.recomendaciones &&
                    datos.recomendaciones.length > 0
                ) {
                
                
                    console.log(
                        "Recomendaciones nuevas recibidas:",
                        datos.recomendaciones
                    );
                
                    console.log(
                        "Actualizando recomendaciones..."
                    );
                
                    cargarRecomendaciones(
                        datos.recomendaciones
                    );
                
                }

                restaurarPanelIANormal();

                if (estado === "Triste") {

                    const panel = document.querySelector(".bw-ai-panel");
                
                    if (panel) {
                
                        panel.innerHTML = `
                            <button
                                id="cuentame-triste"
                                class="bw-ai-button bw-ai-button-triste"
                                type="button"
                            >
                                Cuéntamelo
                            </button>
                        `;

                
                        document
                            .getElementById("cuentame-triste")
                            .addEventListener(
                                "click",
                                mostrarCampoTriste
                            );
                    }
                
                    return;
                }
                
                
                
                
                
                
            })

            .catch(error => {
                console.error("========== ERROR COMPLETO ==========");
                console.error(error);
                console.error("Mensaje:", error.message);
                console.error("Stack:", error.stack);
                console.error("====================================");
            
            
                const respuesta =
                    document.getElementById("bwAiResponse");
            
                if (respuesta) {
            
                    respuesta.value =
                        "No pude generar una respuesta en este momento. " +
                        "Pero tu estado de ánimo sigue guardado. " +
                        "Puedes intentarlo nuevamente en unos segundos.";
            
                    respuesta.style.height = "auto";
            
                    const maxHeight = 180;
            
                    if (respuesta.scrollHeight > maxHeight) {
            
                        respuesta.style.height = maxHeight + "px";
                        respuesta.style.overflowY = "auto";
            
                    } else {
            
                        respuesta.style.height =
                            respuesta.scrollHeight + "px";
            
                        respuesta.style.overflowY = "hidden";
            
                    }
            
                }
            
            });
            

        });
        
    });

});

async function enviarRespuestaTriste() {

    const campo = document.getElementById(
        "respuesta-triste"
    );

    const boton = document.getElementById(
        "enviar-respuesta-triste"
    );

    if (!campo || !boton) {
        return;
    }

    const respuestaUsuario =
        campo.value.trim();

    if (!respuestaUsuario) {
        return;
    }

    boton.disabled = true;
    campo.disabled = true;

    boton.textContent = "…";

    const respuestaIA =
        document.getElementById(
            "bwAiResponse"
        );

    if (respuestaIA) {

        respuestaIA.value = "Pensando...";

        ajustarAltura(respuestaIA);
    }

    try {

        const response = await fetch(
            "/api/triste/analizar",
            {
                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify({
                    respuesta: respuestaUsuario
                })
            }
        );

        const datos = await response.json();

        if (!response.ok) {

            throw new Error(
                datos.error ||
                "No fue posible analizar la respuesta."
            );
        }

        console.log(
            "Estado triste:",
            datos.estado_triste
        );

        console.log(
            "Respuesta final:",
            datos.respuesta_ia
        );

        if (respuestaIA) {

            respuestaIA.value =
                datos.respuesta_ia;

            ajustarAltura(respuestaIA);
        }

        if (
            datos.recomendaciones &&
            datos.recomendaciones.length > 0
        ) {

            console.log(
                "Recomendaciones:",
                datos.recomendaciones
            );

            cargarRecomendaciones(
                datos.recomendaciones
            );
        }

    } catch (error) {

        console.error(
            "Error enviando respuesta triste:",
            error
        );

        if (respuestaIA) {

            respuestaIA.value =
                "No pude analizar tu respuesta en este momento.";

            ajustarAltura(respuestaIA);
        }

    } finally {

        boton.disabled = false;
        campo.disabled = false;
        boton.textContent = "➜";
    }
}


function mostrarCampoTriste() {

    const panel = document.querySelector(".bw-ai-panel");

    if (!panel) {
        return;
    }

    panel.innerHTML = `
        <input
            type="text"
            id="respuesta-triste"
            class="bw-ai-input"
            placeholder="Cuéntame qué ocurre..."
        >

        <button
            id="enviar-respuesta-triste"
            class="bw-ai-button"
            type="button"
        >
            ➜
        </button>
    `;

    const campo = document.getElementById(
        "respuesta-triste"
    );

    const boton = document.getElementById(
        "enviar-respuesta-triste"
    );

    if (campo) {
        campo.focus();

        campo.addEventListener("keydown", function(e) {

            if (e.key === "Enter") {

                e.preventDefault();

                enviarRespuestaTriste();
            }

        });
    }

    if (boton) {

        boton.addEventListener(
            "click",
            enviarRespuestaTriste
        );
    }
}



function mostrarResultadoTriste(datos) {

    const panelIA = document.getElementById("respuesta-ia");

    panelIA.innerHTML = `
        <div class="bw-ai-card">

            <div class="bw-ai-header">
                📚 Bibliotecario AM
            </div>

            <textarea
                id="bwAiResponse"
                class="bw-ai-response"
                readonly
                placeholder="Pregúntame algo..."
            >${datos.respuesta_ia || ""}</textarea>

            <div class="bw-ai-panel">

                <input
                    type="text"
                    id="bwAiInput"
                    class="bw-ai-input"
                    placeholder="Escribe aquí..."
                >

                <button
                    id="bwAiSend"
                    class="bw-ai-button">
                    ➜
                </button>

            </div>

        </div>
    `;

    // Reutilizamos exactamente el comportamiento
    // del panel IA normal.

    const input = document.getElementById("bwAiInput");
    const boton = document.getElementById("bwAiSend");
    const respuesta = document.getElementById("bwAiResponse");

    function ajustarAltura(textarea) {

        textarea.style.height = "auto";

        const maxHeight = 180;

        if (textarea.scrollHeight > maxHeight) {

            textarea.style.height = maxHeight + "px";
            textarea.style.overflowY = "auto";

        } else {

            textarea.style.height =
                textarea.scrollHeight + "px";

            textarea.style.overflowY = "hidden";
        }
    }

    // Ajustar el tamaño del mensaje recibido
    ajustarAltura(respuesta);

    async function enviarPregunta() {

        const mensaje = input.value.trim();

        if (mensaje === "") {
            return;
        }

        respuesta.value = "Pensando...";
        ajustarAltura(respuesta);

        input.value = "";

        try {

            const peticion = await fetch("/api/ia", {

                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify({
                    mensaje: mensaje
                })

            });

            const datosIA = await peticion.json();

            respuesta.value =
                datosIA.respuesta ||
                "No pude generar una respuesta.";

            ajustarAltura(respuesta);

        } catch (error) {

            console.error(error);

            respuesta.value =
                "No pude comunicarme con el asistente.";

            ajustarAltura(respuesta);
        }
    }

    boton.addEventListener(
        "click",
        enviarPregunta
    );

    input.addEventListener(
        "keydown",
        function(e) {

            if (e.key === "Enter") {

                e.preventDefault();

                enviarPregunta();
            }
        }
    );
}

function restaurarPanelIANormal() {

    const panel = document.querySelector(".bw-ai-panel");

    if (!panel) {
        return;
    }

    panel.innerHTML = `
        <input
            type="text"
            id="bwAiInput"
            class="bw-ai-input"
            placeholder="Escribe aquí..."
        >

        <button
            id="bwAiSend"
            class="bw-ai-button"
            type="button"
        >
            ➜
        </button>
    `;

    const input = document.getElementById("bwAiInput");
    const boton = document.getElementById("bwAiSend");
    const respuesta = document.getElementById("bwAiResponse");

    if (!input || !boton || !respuesta) {
        return;
    }

    async function enviarPregunta() {

        const mensaje = input.value.trim();

        if (mensaje === "") {
            return;
        }

        respuesta.value = "Pensando...";
        ajustarAltura(respuesta);

        input.value = "";

        try {

            const peticion = await fetch("/api/ia", {
                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify({
                    mensaje: mensaje
                })
            });

            const datos = await peticion.json();

            respuesta.value =
                datos.respuesta ||
                "No pude generar una respuesta.";

            ajustarAltura(respuesta);

        } catch (error) {

            console.error(error);

            respuesta.value =
                "No pude comunicarme con el asistente.";

            ajustarAltura(respuesta);
        }
    }

    boton.addEventListener(
        "click",
        enviarPregunta
    );

    input.addEventListener(
        "keydown",
        function(e) {

            if (e.key === "Enter") {

                e.preventDefault();

                enviarPregunta();
            }
        }
    );
}
