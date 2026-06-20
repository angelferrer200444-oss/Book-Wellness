let segundos = 0;

let pausado = false;

const timer =
document.getElementById("timer");

const btnPausa =
document.getElementById("btnPausa");

function actualizarCronometro(){

    const horas =
    Math.floor(segundos / 3600);

    const minutos =
    Math.floor((segundos % 3600) / 60);

    const segs =
    segundos % 60;

    timer.textContent =
        String(horas).padStart(2,"0")
        + ":"
        + String(minutos).padStart(2,"0")
        + ":"
        + String(segs).padStart(2,"0");
}

setInterval(()=>{

    if(!pausado){

        segundos++;

        actualizarCronometro();
    }

},1000);

btnPausa.addEventListener("click",()=>{

    pausado = !pausado;

    btnPausa.textContent = pausado

        ? "▶️ Continuar lectura"

        : "⏸️ Pausar lectura";

});

document.getElementById('btnFinalizar').addEventListener('click', () => {
    localStorage.setItem('tiempo_lectura', segundos);
    const params = new URLSearchParams(window.location.search);
    const id_libro = params.get('id_libro');
    window.location.href = `/seccion3-lectura?id_libro=${id_libro}`;
});