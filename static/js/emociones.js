document.addEventListener("DOMContentLoaded", () => {

    const tarjetas = document.querySelectorAll(".bw-card");

    tarjetas.forEach(tarjeta => {

        tarjeta.addEventListener("click", () => {

            const estado = tarjeta.dataset.estado;

            console.log("Estado:", estado);

            const respuesta = document.getElementById("bwAiResponse");

            if (respuesta) {

                respuesta.value = "Pensando...";

                ajustarAltura(respuesta);

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

                console.log("Respuesta del servidor:", datos);

                if (!respuestaServidor.ok) {

                    const error = new Error(
                        datos.error ||
                        "No fue posible generar la respuesta."
                    );

                    error.bloqueado = datos.bloqueado;
                    error.horas_restantes = datos.horas_restantes;

                    throw error;
                }

                return datos;

            })

            .then(async datos => {

                console.log("Datos recibidos:", datos);

                console.log(
                    "Tipo recomendaciones:",
                    typeof datos.recomendaciones
                );

                console.log(
                    "Recomendaciones:",
                    datos.recomendaciones
                );

                console.log(
                    "Cantidad:",
                    datos.recomendaciones?.length
                );

                console.log(
                    "Respuesta IA:",
                    datos.respuesta_ia
                );


                // ==========================================
                // MOSTRAR RESPUESTA DE LA IA
                // ==========================================

                const respuesta =
                    document.getElementById("bwAiResponse");

                if (respuesta && datos.respuesta_ia) {

                    respuesta.value = datos.respuesta_ia;

                    ajustarAltura(respuesta);

                }


                // ==========================================
                // ACTUALIZAR RECOMENDACIONES
                // ==========================================

                if (
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


                // ==========================================
                // TRISTE
                // ==========================================

                if (estado === "Triste") {

                    const panel =
                        document.querySelector(".bw-ai-panel");

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

                        const botonTriste =
                            document.getElementById(
                                "cuentame-triste"
                            );

                        if (botonTriste) {

                            botonTriste.addEventListener(
                                "click",
                                mostrarCampoTriste
                            );

                        }

                    }

                    return;
                }


                // ==========================================
                // RESTAURAR PANEL NORMAL
                // ==========================================

                restaurarPanelIANormal();

            })

            .catch(error => {

                console.error(
                    "========== ERROR COMPLETO =========="
                );

                console.error(error);

                console.error(
                    "Mensaje:",
                    error.message
                );

                console.error(
                    "Bloqueado:",
                    error.bloqueado
                );

                console.error(
                    "Horas restantes:",
                    error.horas_restantes
                );

                console.error(
                    "===================================="
                );


                const respuesta =
                    document.getElementById("bwAiResponse");

                if (!respuesta) {
                    return;
                }


                // ==========================================
                // ERROR POR BLOQUEO DE 24 HORAS
                // ==========================================

                if (error.bloqueado) {

                    respuesta.value =
                        "Ya registraste un estado de ánimo recientemente. " +
                        "Podrás registrar uno nuevo cuando hayan pasado las 24 horas.";

                    if (
                        error.horas_restantes !== undefined
                    ) {

                        respuesta.value +=
                            " Te quedan aproximadamente " +
                            error.horas_restantes +
                            " horas.";

                    }

                }

                // ==========================================
                // OTRO ERROR
                // ==========================================

                else {

                    respuesta.value =
                        "No pude generar una respuesta en este momento. " +
                        "Pero tu estado de ánimo sigue guardado. " +
                        "Puedes intentarlo nuevamente en unos segundos.";

                }


                ajustarAltura(respuesta);

            });

        });

    });

});


// ==========================================================
// AJUSTAR ALTURA DEL TEXTAREA
// ==========================================================

function ajustarAltura(textarea) {

    if (!textarea) {
        return;
    }

    textarea.style.height = "auto";

    const maxHeight = 180;

    if (textarea.scrollHeight > maxHeight) {

        textarea.style.height =
            maxHeight + "px";

        textarea.style.overflowY = "auto";

    } else {

        textarea.style.height =
            textarea.scrollHeight + "px";

        textarea.style.overflowY = "hidden";

    }

}


// ==========================================================
// ENVIAR RESPUESTA DE TRISTE
// ==========================================================

async function enviarRespuestaTriste() {

    const campo =
        document.getElementById(
            "respuesta-triste"
        );

    const boton =
        document.getElementById(
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

        respuestaIA.value =
            "Pensando...";

        ajustarAltura(respuestaIA);

    }


    try {

        const response =
            await fetch(
                "/api/triste/analizar",
                {
                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body: JSON.stringify({
                        respuesta:
                            respuestaUsuario
                    })
                }
            );


        const datos =
            await response.json();


        console.log(
            "Respuesta servidor Triste:",
            datos
        );


        // ==================================================
        // AQUÍ ESTABA EL ERROR
        // ==================================================

        if (!response.ok) {

            const error =
                new Error(
                    datos.error ||
                    "No fue posible generar la respuesta."
                );

            error.bloqueado =
                datos.bloqueado;

            error.horas_restantes =
                datos.horas_restantes;

            throw error;
        }


        console.log(
            "Estado triste:",
            datos.estado_triste
        );

        console.log(
            "Respuesta final:",
            datos.respuesta_ia
        );


        // ==================================================
        // MOSTRAR RESPUESTA IA
        // ==================================================

        if (
            respuestaIA &&
            datos.respuesta_ia
        ) {

            respuestaIA.value =
                datos.respuesta_ia;

            ajustarAltura(
                respuestaIA
            );

        }


        // ==================================================
        // ACTUALIZAR RECOMENDACIONES
        // ==================================================

        if (
            datos.recomendaciones &&
            datos.recomendaciones.length > 0
        ) {

            console.log(
                "Recomendaciones Triste:",
                datos.recomendaciones
            );

            console.log(
                "Actualizando recomendaciones..."
            );

            cargarRecomendaciones(
                datos.recomendaciones
            );

        }

    }

    catch (error) {

        console.error(
            "Error enviando respuesta triste:",
            error
        );


        if (!respuestaIA) {
            return;
        }


        // ==================================================
        // ERROR POR 24 HORAS
        // ==================================================

        if (error.bloqueado) {

            respuestaIA.value =
                "Ya registraste un estado de ánimo recientemente. " +
                "Podrás registrar uno nuevo cuando hayan pasado las 24 horas.";

            if (
                error.horas_restantes !== undefined
            ) {

                respuestaIA.value +=
                    " Te quedan aproximadamente " +
                    error.horas_restantes +
                    " horas.";

            }

        }

        // ==================================================
        // OTRO ERROR
        // ==================================================

        else {

            respuestaIA.value =
                "No pude analizar tu respuesta en este momento.";

        }


        ajustarAltura(
            respuestaIA
        );

    }

    finally {

        boton.disabled = false;

        campo.disabled = false;

        boton.textContent = "➜";

        /*
         * IMPORTANTE:
         * No restauramos aquí el panel.
         *
         * Si lo hacemos, podemos borrar inmediatamente
         * el estado visual de Triste después de recibir
         * correctamente la respuesta.
         */

    }

}


// ==========================================================
// MOSTRAR CAMPO PARA TRISTE
// ==========================================================

function mostrarCampoTriste() {

    const panel =
        document.querySelector(
            ".bw-ai-panel"
        );


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


    const campo =
        document.getElementById(
            "respuesta-triste"
        );

    const boton =
        document.getElementById(
            "enviar-respuesta-triste"
        );


    if (campo) {

        campo.focus();

        campo.addEventListener(
            "keydown",
            function(e) {

                if (e.key === "Enter") {

                    e.preventDefault();

                    enviarRespuestaTriste();

                }

            }
        );

    }


    if (boton) {

        boton.addEventListener(
            "click",
            enviarRespuestaTriste
        );

    }

}


// ==========================================================
// MOSTRAR RESULTADO TRISTE
// ==========================================================

function mostrarResultadoTriste(datos) {

    const panelIA =
        document.getElementById(
            "respuesta-ia"
        );


    if (!panelIA) {
        return;
    }


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
                    class="bw-ai-button"
                >
                    ➜
                </button>

            </div>

        </div>

    `;


    const input =
        document.getElementById(
            "bwAiInput"
        );

    const boton =
        document.getElementById(
            "bwAiSend"
        );

    const respuesta =
        document.getElementById(
            "bwAiResponse"
        );


    ajustarAltura(
        respuesta
    );


    async function enviarPregunta() {

        const mensaje =
            input.value.trim();


        if (mensaje === "") {
            return;
        }


        respuesta.value =
            "Pensando...";

        ajustarAltura(
            respuesta
        );

        input.value = "";


        try {

            const peticion =
                await fetch(
                    "/api/ia",
                    {
                        method: "POST",

                        headers: {
                            "Content-Type":
                                "application/json"
                        },

                        body: JSON.stringify({
                            mensaje:
                                mensaje
                        })
                    }
                );


            const datosIA =
                await peticion.json();


            respuesta.value =
                datosIA.respuesta ||
                "No pude generar una respuesta.";


            ajustarAltura(
                respuesta
            );

        }

        catch (error) {

            console.error(error);

            respuesta.value =
                "No pude comunicarme con el asistente.";

            ajustarAltura(
                respuesta
            );

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


// ==========================================================
// RESTAURAR PANEL IA NORMAL
// ==========================================================

function restaurarPanelIANormal() {

    const panel =
        document.querySelector(
            ".bw-ai-panel"
        );


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


    const input =
        document.getElementById(
            "bwAiInput"
        );

    const boton =
        document.getElementById(
            "bwAiSend"
        );

    const respuesta =
        document.getElementById(
            "bwAiResponse"
        );


    if (
        !input ||
        !boton ||
        !respuesta
    ) {
        return;
    }


    async function enviarPregunta() {

        const mensaje =
            input.value.trim();


        if (mensaje === "") {
            return;
        }


        respuesta.value =
            "Pensando...";

        ajustarAltura(
            respuesta
        );

        input.value = "";


        try {

            const peticion =
                await fetch(
                    "/api/ia",
                    {
                        method: "POST",

                        headers: {
                            "Content-Type":
                                "application/json"
                        },

                        body: JSON.stringify({
                            mensaje:
                                mensaje
                        })
                    }
                );


            const datosIA =
                await peticion.json();


            respuesta.value =
                datosIA.respuesta ||
                "No pude generar una respuesta.";


            ajustarAltura(
                respuesta
            );

        }

        catch (error) {

            console.error(error);

            respuesta.value =
                "No pude comunicarme con el asistente.";

            ajustarAltura(
                respuesta
            );

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
