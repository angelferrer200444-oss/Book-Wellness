document.addEventListener("DOMContentLoaded",()=>{


    // =========================
    // CARRUSEL SIDEBAR
    // =========================

    const carousel = document.querySelector(".sidebar-carousel");


    if(carousel){


        let posicion = 0;

        let pausado = false;

        let pausaEmocion = false;

        let isDown = false;

        let startX = 0;

        let movimiento = 0;



        const panels = document.querySelectorAll(".sidebar-column");

        // =========================
        // MENSAJE DE DESLIZAR
        // =========================

        const hint = document.createElement("div");

        hint.textContent = "Deslizar con el mouse 🖱️";

        hint.className = "carousel-hint";

        carousel.parentElement.appendChild(hint);


        carousel.addEventListener("mouseenter",()=>{

            hint.classList.add("show");

        });


        carousel.addEventListener("mouseleave",()=>{

            hint.classList.remove("show");

        });




        // =========================
        // PAUSA AL ESTAR ENCIMA
        // =========================


        panels.forEach(panel=>{


            panel.addEventListener("mouseenter",()=>{

                pausado = true;

            });



            panel.addEventListener("mouseleave",()=>{

                pausado = false;

                pausaEmocion = false;

            });



        });




        // =========================
        // CAMBIAR PANEL
        // =========================


        function moverPanel(){


            carousel.style.transform =
            `translateX(-${posicion * 33.333}%)`;


        }




        // =========================
        // CARRUSEL AUTOMÁTICO
        // =========================


        setInterval(()=>{


            if(pausado || pausaEmocion || isDown) return;



            posicion++;



            if(posicion > 2){

                posicion = 0;

            }



            moverPanel();



        },5000);







        // =========================
        // DRAG MANUAL
        // =========================


        carousel.addEventListener("mousedown",(e)=>{


            isDown = true;

            pausado = true;


            startX = e.pageX;



        });





        document.addEventListener("mouseup",()=>{


            if(!isDown) return;



            isDown = false;

            pausado = false;



            if(movimiento > 80){

                posicion--;

            }



            if(movimiento < -80){

                posicion++;

            }



            if(posicion < 0){

                posicion = 2;

            }



            if(posicion > 2){

                posicion = 0;

            }



            moverPanel();



            movimiento = 0;



        });







        document.addEventListener("mousemove",(e)=>{


            if(!isDown) return;



            movimiento = e.pageX - startX;



        });



    }







    // =========================
    // EMOCIONES
    // =========================

    const emociones = document.querySelectorAll(".bw-card");


    // =========================
    // RESTAURAR EMOCIÓN ACTIVA
    // =========================

    fetch("/api/estado_animo_actual", {
        method: "GET"
    })
    .then(async respuesta => {

        if (!respuesta.ok) {
            return null;
        }

        return await respuesta.json();

    })
    .then(datos => {

        if (!datos || !datos.estado) {
            return;
        }

        const emocionActual = Array.from(emociones).find(
            emocion =>
                emocion.dataset.estado.toLowerCase() ===
                datos.estado.toLowerCase()
        );

        if (!emocionActual) {
            return;
        }

        emociones.forEach(emocion => {
            emocion.classList.remove("active");
        });

        emocionActual.classList.add("active");

        // Mantener pausado el carrusel
        const carousel =
            document.querySelector(".sidebar-carousel");

        if (carousel) {
            pausaEmocion = true;
        }

    })
    .catch(error => {

        console.error(
            "No se pudo restaurar el estado de ánimo:",
            error
        );

    });


    // =========================
    // CLIC EN EMOCIÓN
    // =========================

    emociones.forEach(emocion => {

        emocion.addEventListener("click", (e) => {

            e.stopPropagation();

            emociones.forEach(e => {
                e.classList.remove("active");
            });

            emocion.classList.add("active");

            // pausa mientras una emoción está seleccionada
            const carousel =
                document.querySelector(".sidebar-carousel");

            if (carousel) {
                pausaEmocion = true;
            }

        });

    });




});


