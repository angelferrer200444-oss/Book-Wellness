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



    emociones.forEach(emocion=>{


        emocion.addEventListener("click",(e)=>{


            e.stopPropagation();



            emociones.forEach(e=>{


                e.classList.remove("active");


            });




            emocion.classList.add("active");



            // pausa mientras una emoción está seleccionada

            const carousel = document.querySelector(".sidebar-carousel");


            if(carousel){

                pausaEmocion = true;

            }



        });



    });



});



