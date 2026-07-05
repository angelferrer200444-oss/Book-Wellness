const input = document.getElementById("bwAiInput");
const boton = document.getElementById("bwAiSend");
const respuesta = document.getElementById("bwAiResponse");

function ajustarAltura(textarea){

    textarea.style.height = "auto";

    const maxHeight = 180;

    if(textarea.scrollHeight > maxHeight){

        textarea.style.height = maxHeight + "px";
        textarea.style.overflowY = "auto";

    }else{

        textarea.style.height = textarea.scrollHeight + "px";
        textarea.style.overflowY = "hidden";

    }

}

async function enviarPregunta(){

    const mensaje = input.value.trim();

    if(mensaje === ""){
        return;
    }

    respuesta.value = "Pensando...";
    ajustarAltura(respuesta);

    input.value = "";

    try{

        const peticion = await fetch("/api/ia",{

            method:"POST",

            headers:{
                "Content-Type":"application/json"
            },

            body:JSON.stringify({
                mensaje:mensaje
            })

        });

        const datos = await peticion.json();

        respuesta.value = datos.respuesta;

        ajustarAltura(respuesta);

    }catch(error){

        console.error(error);

        respuesta.value = "No pude comunicarme con el asistente.";

        ajustarAltura(respuesta);

    }

}

boton.addEventListener("click", enviarPregunta);

input.addEventListener("keydown", function(e){

    if(e.key === "Enter"){

        e.preventDefault();

        enviarPregunta();

    }

});


