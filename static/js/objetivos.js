document.addEventListener("DOMContentLoaded", () => {

    

    // =====================================================
    // ELEMENTOS
    // =====================================================

    const modal =
        document.getElementById("goal-modal");

    document.body.appendChild(modal);

    const openModalBtn =
        document.getElementById("open-modal-btn");

    const emptyCreateBtn =
        document.getElementById("empty-create-btn");

    const closeModalBtn =
        document.getElementById("close-modal-btn");

    const cancelBtn =
        document.getElementById("cancel-goal-btn");

    const form =
        document.getElementById("goal-form");

    const configuration =
        document.getElementById("goal-configuration");

    const saveBtn =
        document.getElementById("save-goal-btn");

    const emptyMessage =
        document.getElementById("empty-goals-message");

    const surveyEmpty =
        document.getElementById("goal-survey-empty");

    const aiChat =
        document.getElementById("goal-ai-chat");

    const aiMessages =
        document.getElementById("ai-chat-messages");
    
    const aiInput =
        document.getElementById("ai-chat-input");
    
    const aiSend =
        document.getElementById("ai-chat-send");
    
    


    // =====================================================
    // CAMPOS
    // =====================================================

    const titleInput =
        document.getElementById("goal-title");

    const descInput =
        document.getElementById("goal-desc");

    const totalInput =
        document.getElementById("goal-total");

    const unitDisplay =
        document.getElementById("goal-unit");

    const conditionSelect =
        document.getElementById("goal-condition");

    const conditionGroup =
        document.getElementById("condition-value-group");

    const conditionValue =
        document.getElementById("goal-condition-value");

    const frequencyGroup =
        document.getElementById("frequency-group");

    const frequencySelect =
        document.getElementById("goal-frequency");

    const startDate =
        document.getElementById("goal-start-date");

    const endDate =
        document.getElementById("goal-end-date");

    const preview =
        document.getElementById("goal-preview");


    // =====================================================
    // ESTADO
    // =====================================================

    let tipoSeleccionado = null;

    let objetivoEditandoId = null;


    // =====================================================
    // ABRIR MODAL
    // =====================================================

    function abrirModal() {

        modal.classList.add("active");
    }


    // =====================================================
    // CERRAR MODAL
    // =====================================================

    function cerrarModal() {

        modal.classList.remove("active");
    }


    // =====================================================
    // PREPARAR MODAL PARA CREAR
    // =====================================================

    function prepararNuevoObjetivo() {

        objetivoEditandoId = null;

        form.reset();

        tipoSeleccionado = null;

        tipos.forEach((item) => {
            item.classList.remove("selected");
        });

        configuration.classList.add("hidden");

        conditionGroup.classList.add("hidden");

        frequencyGroup.classList.add("hidden");

        unitDisplay.textContent =
            "Selecciona un tipo";

        preview.textContent =
            "Selecciona un tipo de objetivo para comenzar.";

        saveBtn.textContent =
            "Guardar Objetivo";

        validarFormulario();
    }


    // =====================================================
    // BOTÓN NUEVO
    // =====================================================

    if (openModalBtn) {

        openModalBtn.addEventListener(
            "click",
            () => {

                prepararNuevoObjetivo();

                abrirModal();
            }
        );
    }


    if (emptyCreateBtn) {

        emptyCreateBtn.addEventListener(
            "click",
            () => {

                prepararNuevoObjetivo();
                abrirModal();
            }
        );
    }


    // =====================================================
    // CERRAR
    // =====================================================

    if (closeModalBtn) {

        closeModalBtn.addEventListener(
            "click",
            cerrarModal
        );
    }


    if (cancelBtn) {

        cancelBtn.addEventListener(
            "click",
            cerrarModal
        );
    }


    modal.addEventListener("click", (evento) => {

        if (evento.target === modal) {

            cerrarModal();
        }

    });


    // =====================================================
    // TIPOS DE OBJETIVO
    // =====================================================

    const tipos =
        document.querySelectorAll(".goal-type-card");


    tipos.forEach((boton) => {

        boton.addEventListener("click", () => {

            console.log("TIPO SELECCIONADO:", boton.dataset.goalType);

            tipos.forEach((item) => {
                item.classList.remove("selected");
            });

            boton.classList.add("selected");

            tipoSeleccionado =
                boton.dataset.goalType;

                // SI ES EL BOTÓN DE IA
                if(tipoSeleccionado === "ia"){

                    configuration.classList.add("hidden");

                    if(surveyEmpty){
                        surveyEmpty.classList.add("hidden");
                    }

                    aiMessages.innerHTML = "";

                    agregarMensajeIA(

                    `Hola, soy Am, tu Bibliotecario de Book Wellness.
                    
                    Cuéntame qué quieres conseguir con tu lectura y te ayudaré a elegir el objetivo adecuado.`,
                    
                    "ia"
                    
                    );
                        

                    aiChat.classList.remove("hidden");

                    return;
                }


                // SI ES UN OBJETIVO NORMAL
                else{

                    aiChat.classList.add("hidden");

                }


                configurarTipo(tipoSeleccionado);


                if(tipoSeleccionado !== "ia"){
                
                    configuration.classList.remove("hidden");
                
                }
                

            if (surveyEmpty) {
                surveyEmpty.classList.add("hidden");
            }

            actualizarPreview();
            validarFormulario();
        });

    });


    // =====================================================
    // CONFIGURAR TIPO
    // =====================================================

    function configurarTipo(tipo) {

        if (tipo === "libros") {

            unitDisplay.textContent = "libros";

            totalInput.placeholder = "Ej: 5";

            frequencyGroup.classList.add("hidden");
        }


        else if (tipo === "paginas") {

            unitDisplay.textContent = "páginas";

            totalInput.placeholder = "Ej: 500";

            frequencyGroup.classList.add("hidden");
        }


        else if (tipo === "tiempo") {

            unitDisplay.textContent = "minutos";

            totalInput.placeholder = "Ej: 300";

            frequencyGroup.classList.add("hidden");
        }


        else if (tipo === "rutina") {

            unitDisplay.textContent = "días";

            totalInput.placeholder = "Ej: 7";

            frequencyGroup.classList.remove("hidden");
        }

        else if (tipo === "ia") {

            abrirAsistenteObjetivos();
        
            return;
        }


        actualizarPreview();
    }


    // =====================================================
    // CONDICIONES
    // =====================================================

    conditionSelect.addEventListener(
        "change",
        () => {

            if (
                conditionSelect.value === "ninguna"
            ) {

                conditionGroup.classList.add("hidden");

                conditionValue.value = "";
            }

            else {

                conditionGroup.classList.remove("hidden");
            }

            actualizarPreview();
        }
    );


    // =====================================================
    // PREVISUALIZACIÓN
    // =====================================================

    function actualizarPreview() {

        if (!tipoSeleccionado) {

            preview.textContent =
                "Selecciona un tipo de objetivo para comenzar.";

            return;
        }


        const titulo =
            titleInput.value.trim();


        const meta =
            totalInput.value;


        const unidad =
            unitDisplay.textContent;


        if (!meta) {

            preview.textContent =
                "Define la cantidad que quieres alcanzar.";

            return;
        }


        let texto =
            titulo || "Tu nuevo objetivo";


        texto +=
            ` · ${meta} ${unidad}`;



        if (
            conditionSelect.value !== "ninguna" &&
            conditionValue.value.trim()
        ) {

            texto +=
                ` · ${conditionValue.value.trim()}`;
        }


        preview.textContent = texto;
    }
    // =====================================================
    // VALIDAR FORMULARIO
    // =====================================================

    function validarFormulario() {

        const tituloValido =
            titleInput.value.trim() !== "";
    
    
        const metaValida =
            totalInput.value !== "" &&
            Number(totalInput.value) > 0;
    
    
        const tipoValido =
            objetivoEditandoId
                ? true
                : tipoSeleccionado !== null &&
                  tipoSeleccionado !== "ia";
        
    
    
        saveBtn.disabled =
            !tituloValido ||
            !metaValida ||
            !tipoValido;
    }
    


    // =====================================================
    // EVENTOS DE CAMPOS
    // =====================================================

    titleInput.addEventListener(
        "input",
        () => {

            actualizarPreview();
            validarFormulario();
        }
    );


    descInput.addEventListener(
        "input",
        actualizarPreview
    );


    totalInput.addEventListener(
        "input",
        () => {

            actualizarPreview();
            validarFormulario();
        }
    );


    conditionValue.addEventListener(
        "input",
        actualizarPreview
    );


    // =====================================================
    // CREAR DATOS DEL FORMULARIO
    // =====================================================

    function obtenerDatosFormulario() {

        return {

            titulo:
                titleInput.value.trim(),

            descripcion:
                descInput.value.trim(),

            tipo:
                tipoSeleccionado,

            meta:
                Number(totalInput.value),

            unidad:
                unitDisplay.textContent,

            fecha_inicio:
                startDate.value || null,

            fecha_fin:
                endDate.value || null,

            condicion_tipo:
                conditionSelect.value,

            condicion_valor:
                conditionValue.value.trim() || null,

            frecuencia:
                frequencyGroup.classList.contains("hidden")
                    ? null
                    : frequencySelect.value
        };
    }


    // =====================================================
    // GUARDAR OBJETIVO
    // =====================================================

    form.addEventListener(
        "submit",
        async (evento) => {

            evento.preventDefault();


            if (!tipoSeleccionado) {
                return;
            }

            if (!startDate.value) {

                alert("La fecha de inicio es obligatoria.");
            
                return;
            }


            const objetivo =
                obtenerDatosFormulario();


            try {

                let url =
                    "/api/objetivos";


                let metodo =
                    "POST";


                // Si estamos editando
                if (objetivoEditandoId) {

                    url =
                        `/api/objetivos/${objetivoEditandoId}`;

                    metodo =
                        "PUT";
                }

                console.log("DATOS QUE ENVÍO:", objetivo);

                const respuesta =
                    await fetch(
                        url,
                        {
                            method: metodo,

                            headers: {
                                "Content-Type":
                                    "application/json"
                            },

                            body:
                                JSON.stringify(objetivo)
                        }
                    );


                const datos =
                    await respuesta.json();


                if (!respuesta.ok) {

                    alert(
                        datos.error ||
                        "No se pudo guardar el objetivo."
                    );

                    return;
                }


                // =================================================
                // CREAR
                // =================================================

                if (!objetivoEditandoId) {

                    agregarObjetivo(
                        datos.objetivo
                    );
                }
                // =================================================
                // EDITAR
                // =================================================

                else {

                    actualizarTarjeta(
                        datos.objetivo
                    );
                }


                cerrarModal();


                prepararNuevoObjetivo();

            }


            catch (error) {

                console.error(
                    "Error guardando objetivo:",
                    error
                );

                alert(
                    "No se pudo conectar con el servidor."
                );
            }

        }
    );
    
    // =====================================================
    // RENDERIZAR TARJETA (UNIFICADO)
    // =====================================================

    function obtenerHTMLTarjeta(objetivo) {
        const condicionTexto =
            objetivo.condicion_tipo === "ninguna"
                ? "Cualquier lectura"
                : `${objetivo.condicion_tipo}: ${objetivo.condicion_valor || ""}`;

        const frecuenciaTexto =
            objetivo.frecuencia || "No aplica";

        const estadoTexto =
            objetivo.estado === "completado" ? "Completado" : "En progreso";

        const estadoClase =
            objetivo.estado === "completado" ? "status-success" : "status-pending";

        return `
            <div class="card card-container-design goals-main-card" data-goal-id="${objetivo.id_objetivo}">
                <div class="card-header-brown">
                    Metas Activas
                </div>
                <div class="db-diagram-box">
                    <div class="diagram-header">
                        <span class="db-icon">🎯</span>
                        Mis Objetivos
                        <button type="button" class="goal-edit-btn" title="Editar objetivo">✏️</button>

                        <button type="button" class="goal-delete-btn" title="Eliminar objetivo">🗑️</button>
                    </div>
                    <div class="diagram-body goals-list">
                        <div class="diagram-row item-highlight">
                            <span class="diag-field">Objetivo</span>
                            <span class="diag-value">${objetivo.titulo}</span>
                        </div>
                        <div class="diagram-row">
                            <span class="diag-field">Descripción</span>
                            <span class="diag-value description-text">${objetivo.descripcion || "Sin descripción"}</span>
                        </div>
                        <div class="diagram-row">
                            <span class="diag-field">Meta</span>
                            <span class="diag-value">${objetivo.meta} ${objetivo.unidad}</span>
                        </div>
                        <div class="diagram-row">
                            <span class="diag-field">Progreso</span>
                            <span class="diag-value">${objetivo.progreso_actual} / ${objetivo.meta} ${objetivo.unidad}</span>
                        </div>
                        <div class="progress-container">
                            <div class="progress-bar" style="width: ${objetivo.porcentaje}%;"></div>
                        </div>
                        <div class="diagram-row">
                            <span class="diag-field">Inicio</span>
                            <span class="diag-value">${objetivo.fecha_inicio || "Sin fecha"}</span>
                        </div>
                        <div class="diagram-row">
                            <span class="diag-field">Finalización</span>
                            <span class="diag-value">${objetivo.fecha_fin || "Sin fecha"}</span>
                        </div>
                        <div class="diagram-row">
                            <span class="diag-field">Condición</span>
                            <span class="diag-value">${condicionTexto}</span>
                        </div>
                        <div class="diagram-row">
                            <span class="diag-field">Frecuencia</span>
                            <span class="diag-value">${frecuenciaTexto}</span>
                        </div>
                        <div class="diagram-row border-top-dash">
                            <span class="diag-field">Progreso</span>

                            <div class="goal-progress-wrapper">

                                <div class="goal-progress-bar">
                                    <div class="goal-progress-fill"></div>
                                </div>

                                <span class="diag-status ${estadoClase}">
                                    ${estadoTexto} (0%)
                                </span>

                            </div>
                        </div>

                    </div>
                </div>
            </div>
        `;
    }

    // =====================================================
    // MOSTRAR OBJETIVO
    // =====================================================

    function agregarObjetivo(objetivo) {
        const mainContainer = document.getElementById("main-goals-container");
        const emptyCard = document.getElementById("empty-goals-card");
    
        if (emptyCard) {
            emptyCard.remove();
        }
    
        mainContainer.insertAdjacentHTML("beforeend", obtenerHTMLTarjeta(objetivo));
    }

    function convertirFechaInput(fecha) {

        if (!fecha) {
            return "";
        }
    
        const fechaObj = new Date(fecha);
    
        if (isNaN(fechaObj)) {
            return fecha;
        }
    
        const año = fechaObj.getFullYear();
        const mes = String(fechaObj.getMonth() + 1).padStart(2, "0");
        const dia = String(fechaObj.getDate()).padStart(2, "0");
    
        return `${año}-${mes}-${dia}`;
    }
    
    // =====================================================
    // EDITAR OBJETIVO
    // =====================================================

    const activeContainer =
        document.getElementById("main-goals-container");


    activeContainer.addEventListener(
        "click",
        (evento) => {

            const botonEliminar =
                evento.target.closest(".goal-delete-btn");


            if (botonEliminar) {

                const tarjeta =
                    botonEliminar.closest(".goals-main-card");


                const id =
                    tarjeta.dataset.goalId;


                eliminarObjetivo(id);
            }


            const boton =
                evento.target.closest(".goal-edit-btn");


            if (!boton) {
                return;
            }


            const tarjeta =
                boton.closest(".goals-main-card");


            if (!tarjeta) {
                return;
            }


            const id =
                tarjeta.dataset.goalId;


            if (!id) {
                return;
            }


            editarObjetivo(id);
        }
    );




    async function editarObjetivo(id) {

        console.log("TIPO AL EDITAR:", tipoSeleccionado);

        try {

            const respuesta =
                await fetch("/api/objetivos");


            const objetivos =
                await respuesta.json();


            const objetivo =
                objetivos.find(
                    (item) =>
                        String(item.id_objetivo) === String(id)
                );
            
            console.log("OBJETIVO RECIBIDO:", objetivo);


            if (!objetivo) {

                alert(
                    "No se encontró el objetivo."
                );

                return;
            }


            objetivoEditandoId =
                objetivo.id_objetivo;


            // =================================================
            // RELLENAR FORMULARIO
            // =================================================

            titleInput.value =
                objetivo.titulo || "";


            descInput.value =
                objetivo.descripcion || "";


            totalInput.value =
                objetivo.meta || "";


            startDate.value =
                convertirFechaInput(objetivo.fecha_inicio);
            
            
            endDate.value =
                convertirFechaInput(objetivo.fecha_fin);


            conditionSelect.value =
                objetivo.condicion_tipo || "ninguna";


            conditionValue.value =
                objetivo.condicion_valor || "";


            if (
                objetivo.condicion_tipo &&
                objetivo.condicion_tipo !== "ninguna"
            ) {

                conditionGroup.classList.remove(
                    "hidden"
                );
            }

            else {

                conditionGroup.classList.add(
                    "hidden"
                );
            }


            // =================================================
            // SELECCIONAR TIPO
            // =================================================

            tipos.forEach((item) => {

                item.classList.remove(
                    "selected"
                );


                if (
                    item.dataset.goalType ===
                    objetivo.tipo
                ) {

                    item.classList.add(
                        "selected"
                    );
                }

            });
            
            
            tipoSeleccionado = objetivo.tipo;

            configurarTipo(tipoSeleccionado);

            // Actualizar selección visual
            tipos.forEach((item) => {

                item.classList.remove("selected");

                if (item.dataset.goalType === tipoSeleccionado) {

                    item.classList.add("selected");

                }

            });

            validarFormulario();


            validarFormulario();


            if (objetivo.frecuencia) {

                frequencyGroup.classList.remove(
                    "hidden"
                );

                frequencySelect.value =
                    objetivo.frecuencia;
            }


            configuration.classList.remove(
                "hidden"
            );


            if (surveyEmpty) {

                surveyEmpty.classList.add(
                    "hidden"
                );
            }


            saveBtn.textContent =
                "Guardar Cambios";


            actualizarPreview();

            validarFormulario();

            abrirModal();

        }


        catch (error) {

            console.error(
                "Error obteniendo objetivo:",
                error
            );

            alert(
                "No se pudo cargar el objetivo."
            );
        }
    }

    async function eliminarObjetivo(id) {

        const confirmar =
            confirm("¿Seguro que quieres eliminar este objetivo?");
    
    
        if (!confirmar) {
            return;
        }
    
    
        try {
    
            const respuesta =
                await fetch(
                    `/api/objetivos/${id}`,
                    {
                        method: "DELETE"
                    }
                );
    
    
            const datos =
                await respuesta.json();
    
    
            if (!respuesta.ok) {
    
                alert(
                    datos.error ||
                    "No se pudo eliminar el objetivo."
                );
    
                return;
            }
    
    
            const tarjeta =
                document.querySelector(
                    `[data-goal-id="${id}"]`
                );
    
    
            if (tarjeta) {
    
                tarjeta.remove();
    
            }
    
    
        }
    
        catch(error) {
    
            console.error(
                "Error eliminando objetivo:",
                error
            );
    
            alert(
                "No se pudo conectar con el servidor."
            );
        }
    }
    


    // =====================================================
    // ACTUALIZAR TARJETA
    // =====================================================

    function actualizarTarjeta(objetivo) {
        const tarjeta = activeContainer.querySelector(`[data-goal-id="${objetivo.id_objetivo}"]`);
    
        if (tarjeta) {
            tarjeta.outerHTML = obtenerHTMLTarjeta(objetivo);
        }
    }


    // =====================================================
    // CARGAR OBJETIVOS EXISTENTES
    // =====================================================

    async function cargarObjetivos() {

        try {

            const respuesta =
                await fetch(
                    "/api/objetivos"
                );


            const objetivos =
                await respuesta.json();


            objetivos.forEach(
                (objetivo) => {

                    agregarObjetivo(
                        objetivo
                    );

                }
            );


        }

        catch (error) {

            console.error(
                "Error cargando objetivos:",
                error
            );
        }
    }

    // =====================================================
    // ASISTENTE IA OBJETIVOS
    // =====================================================

    function abrirAsistenteObjetivos(){

        console.log("Abriendo asistente IA de objetivos");

        configuration.classList.add("hidden");

        preview.textContent =
            "Am está preparando una guía para crear tu objetivo.";

    }

    // =====================================================
    // CHAT IA OBJETIVOS
    // =====================================================


    function agregarMensajeIA(texto, tipo){

        const mensaje =
            document.createElement("div");


        mensaje.classList.add(
            tipo === "usuario"
                ? "user-message"
                : "ai-message"
        );


        mensaje.innerHTML = formatearMensajeIA(texto);


        aiMessages.appendChild(mensaje);


        aiMessages.scrollTop =
            aiMessages.scrollHeight;
    }

    async function enviarMensajeIA(){

        const texto = aiInput.value.trim();
    
    
        if(!texto){
            return;
        }
    
    
        agregarMensajeIA(
            texto,
            "usuario"
        );
    
    
        aiInput.value = "";
    
    
        try{
    
    
            const respuesta = await fetch(
                "/api/ia",
                {
                    method:"POST",
    
                    headers:{
                        "Content-Type":"application/json"
                    },
    
                    body:JSON.stringify({
                        mensaje:texto,
                        seccion:"objetivos"
                    })
                }
            );
    
    
            const datos = await respuesta.json();
    
    
            agregarMensajeIA(
                datos.respuesta,
                "ia"
            );
    
    
        }
    
    
        catch(error){
    
            console.error(
                "Error IA objetivos:",
                error
            );
    
    
            agregarMensajeIA(
                "No pude conectarme con Am en este momento.",
                "ia"
            );
    
        }
    
    }

    function formatearMensajeIA(texto){

        return texto
            // Escapar HTML básico
            .replace(/</g, "&lt;")
            .replace(/>/g, "&gt;")
    
            // Títulos con negrita tipo **texto**
            .replace(/\*\*(.*?)\*\*/g, "<strong>$1</strong>")
    
            // Eliminar asteriscos sueltos usados como viñetas
            .replace(/^\s*\*\s+/gm, "• ")
    
            // Separadores
            .replace(/^---$/gm, "")
    
            // Saltos de línea
            .replace(/\n/g, "<br>");
    }
    
    
        
    
    if(aiSend){

        aiSend.addEventListener(
            "click",
            enviarMensajeIA
        );
    
    }

    if(aiInput){

        aiInput.addEventListener(
            "keypress",
            (e)=>{
    
                if(e.key === "Enter"){
    
                    enviarMensajeIA();
    
                }
    
            }
        );
    
    }
    
    

    // =====================================================
    // INICIO
    // =====================================================

    validarFormulario();

    cargarObjetivos();

});





