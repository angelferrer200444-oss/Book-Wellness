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
                
                
                
            })

            .catch(error => {

                console.error("Error:", error);
            
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
