document.addEventListener("DOMContentLoaded", () => {

    console.log("OBJETIVO-INDEX.JS CARGADO");
    console.log("DOM CARGADO - OBJETIVO INDEX");

    // =====================================================
    // ELEMENTOS DEL INDEX
    // =====================================================

    const noGoal = document.getElementById("index-no-goal");

    const goalTitleRow =
        document.getElementById("index-goal-title-row");

    const goalProgressRow =
        document.getElementById("index-goal-progress-row");

    const goalBarRow =
        document.getElementById("index-goal-bar-row");

    const goalStatusRow =
        document.getElementById("index-goal-status-row");

    const goalTitle =
        document.getElementById("index-goal-title");

    const goalProgress =
        document.getElementById("index-goal-progress");

    const goalProgressBar =
        document.getElementById("index-goal-progress-bar");

    const goalStatus =
        document.getElementById("index-goal-status");


    // =====================================================
    // CARGAR OBJETIVO MÁS RECIENTE
    // =====================================================

    async function cargarObjetivoIndex() {

        console.log("EJECUTANDO cargarObjetivoIndex");

        if (!noGoal) {
            console.error(
                "No se encontró #index-no-goal"
            );
            return;
        }

        try {

            const respuesta =
                await fetch("/api/objetivos");

            console.log(
                "RESPUESTA API:",
                respuesta.status
            );

            if (!respuesta.ok) {

                console.error(
                    "La API de objetivos respondió con error."
                );

                mostrarSinObjetivo();

                return;
            }

            const objetivos =
                await respuesta.json();

            console.log(
                "OBJETIVOS RECIBIDOS:",
                objetivos
            );


            // =================================================
            // NO HAY OBJETIVOS
            // =================================================

            if (
                !Array.isArray(objetivos) ||
                objetivos.length === 0
            ) {

                mostrarSinObjetivo();

                return;
            }


            // =================================================
            // OBTENER EL OBJETIVO MÁS RECIENTE
            // =================================================

            const objetivosActivos =
                objetivos.filter(
                    objetivo => objetivo.estado !== "completado"
                );

            const objetivo =
                obtenerObjetivoMasReciente(objetivosActivos);


            console.log(
                "OBJETIVO MÁS RECIENTE:",
                objetivo
            );


            if (!objetivo) {

                mostrarSinObjetivo();

                return;
            }


            // =================================================
            // MOSTRAR OBJETIVO
            // =================================================

            mostrarObjetivo(objetivo);

        }

        catch (error) {

            console.error(
                "ERROR CARGANDO OBJETIVO DEL INDEX:",
                error
            );

            mostrarSinObjetivo();
        }
    }


    // =====================================================
    // OBTENER OBJETIVO MÁS RECIENTE
    // =====================================================

    function obtenerObjetivoMasReciente(objetivos) {

        if (!objetivos.length) {
            return null;
        }

        /*
         * Intentamos ordenar por fecha de inicio.
         * El último objetivo creado normalmente tendrá
         * la fecha más reciente.
         */

        const objetivosOrdenados =
            [...objetivos].sort((a, b) => {

                const fechaA =
                    new Date(
                        a.fecha_inicio || 0
                    );

                const fechaB =
                    new Date(
                        b.fecha_inicio || 0
                    );
                return fechaB - fechaA;
            });


        return objetivosOrdenados[0];
    }


    // =====================================================
    // MOSTRAR "NO HAY OBJETIVOS"
    // =====================================================

    function mostrarSinObjetivo() {

        console.log(
            "MOSTRANDO: NO HAY OBJETIVOS"
        );

        noGoal.style.display = "";


        if (goalTitleRow) {
            goalTitleRow.classList.add("hidden");
        }

        if (goalProgressRow) {
            goalProgressRow.classList.add("hidden");
        }

        if (goalBarRow) {
            goalBarRow.classList.add("hidden");
        }

        if (goalStatusRow) {
            goalStatusRow.classList.add("hidden");
        }
    }


    // =====================================================
    // MOSTRAR OBJETIVO
    // =====================================================

    function mostrarObjetivo(objetivo) {

        console.log(
            "MOSTRANDO OBJETIVO EN INDEX:",
            objetivo
        );


        // Ocultar mensaje de "no hay objetivos"

        noGoal.style.display = "none";


        // Mostrar filas

        if (goalTitleRow) {
            goalTitleRow.classList.remove("hidden");
        }

        if (goalProgressRow) {
            goalProgressRow.classList.remove("hidden");
        }

        if (goalBarRow) {
            goalBarRow.classList.remove("hidden");
        }

        if (goalStatusRow) {
            goalStatusRow.classList.remove("hidden");
        }


        // =================================================
        // TÍTULO / META
        // =================================================

        if (goalTitle) {

            goalTitle.textContent =
                `${objetivo.titulo || "Objetivo"} · ${objetivo.meta || 0} ${objetivo.unidad || ""}`;
        }


        // =================================================
        // PROGRESO
        // =================================================

        const progreso =
            Number(objetivo.progreso_actual) || 0;

        const meta =
            Number(objetivo.meta) || 0;


        let porcentaje = 0;

        if (meta > 0) {

            porcentaje =
                Math.round(
                    (progreso / meta) * 100
                );
        }


        porcentaje =
            Math.max(
                0,
                Math.min(
                    100,
                    porcentaje
                )
            );


        if (goalProgress) {

            goalProgress.textContent =
                `${progreso} / ${meta} ${objetivo.unidad || ""}`;
        }


        // =================================================
        // BARRA
        // =================================================

        if (goalProgressBar) {

            goalProgressBar.style.width =
                `${porcentaje}%`;
        }


        // =================================================
        // ESTADO
        // =================================================

        if (goalStatus) {

            if (
                objetivo.estado === "completado" ||
                porcentaje >= 100
            ) {

                goalStatus.textContent =
                    `Completado (${porcentaje}%)`;

                goalStatus.classList.remove(
                    "status-pending"
                );

                goalStatus.classList.add(
                    "status-success"
                );

            }

            else {

                goalStatus.textContent =
                    `En progreso (${porcentaje}%)`;

                goalStatus.classList.remove(
                    "status-success"
                );

                goalStatus.classList.add(
                    "status-pending"
                );
            }
        }
    }



    // =====================================================
    // INICIO
    // =====================================================

    cargarObjetivoIndex();

});
