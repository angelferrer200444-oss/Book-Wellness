document.addEventListener('DOMContentLoaded', () => {
    const modal = document.getElementById('goal-modal');
    const openModalBtn = document.getElementById('open-modal-btn');
    const closeModalBtn = document.getElementById('close-modal-btn');
    const goalForm = document.getElementById('goal-form');
    
    // Cambiado al contenedor superior (Metas Activas)
    const mainGoalsContainer = document.getElementById('main-goals-container');
    const addButtonCard = document.getElementById('add-button-card');

    // Desplegar Menú Modal al presionar el botón "Insertar Objetivo"
    if (openModalBtn) {
        openModalBtn.addEventListener('click', (e) => {
            e.preventDefault();
            if (modal) {
                modal.classList.add('active');
                const dateInput = document.getElementById('goal-date');
                if (dateInput) dateInput.valueAsDate = new Date();
            }
        });
    }

    // Ocultar Menú Modal al cancelar
    if (closeModalBtn) {
        closeModalBtn.addEventListener('click', () => {
            modal.classList.remove('active');
            goalForm.reset();
        });
    }

    // Cerrar si el usuario hace clic fuera de la tarjeta blanca (en el fondo borroso)
    if (modal) {
        modal.addEventListener('click', (e) => {
            if (e.target === modal) {
                modal.classList.remove('active');
                goalForm.reset();
            }
        });
    }

    // Recibir datos, procesar barra de progreso y pintar tarjeta dinámicamente
    if (goalForm) {
        goalForm.addEventListener('submit', (e) => {
            e.preventDefault();

            const title = document.getElementById('goal-title').value;
            const desc = document.getElementById('goal-desc').value;
            
            // AUTOMATIZACIÓN: El progreso inicial empieza en 0 de forma automática
            const current = 0;
            const total = parseInt(document.getElementById('goal-total').value);
            const unit = document.getElementById('goal-unit').value;
            const rawDate = document.getElementById('goal-date').value;

            // Formatear la fecha ingresada para que se vea elegante (Ej: 15 jun 2026)
            const dateObj = new Date(rawDate + 'T00:00:00'); 
            const formattedDate = dateObj.toLocaleDateString('es-ES', { day: 'numeric', month: 'short', year: 'numeric' });

            // Lógica interactiva de las barras de progreso
            let percentage = Math.round((current / total) * 100);
            if (percentage > 100) percentage = 100;
            if (percentage < 0) percentage = 0;
            
            const isCompleted = percentage === 100;
            const statusClass = isCompleted ? 'status-success' : 'status-pending';
            const statusText = isCompleted ? 'Logrado' : 'En Progreso';
            const barClass = isCompleted ? 'progress-bar bar-success' : 'progress-bar';

            // Crear el bloque HTML correspondiente a la nueva tarjeta
            const newCard = document.createElement('div');
            newCard.className = 'card card-container-design';
            newCard.innerHTML = `
                <div class="card-header-brown">Meta Activa</div>
                <div class="db-diagram-box">
                    <div class="diagram-header">
                        <span class="db-icon">📌</span> ${title}
                    </div>
                    <div class="diagram-body">
                        <div class="diagram-row item-highlight">
                            <span class="diag-field">Meta</span>
                            <span class="diag-value">${total} ${unit}</span>
                        </div>
                        <div class="diagram-row">
                            <span class="diag-field">Progreso</span>
                            <span class="diag-value">${current} / ${total} ${unit}</span>
                        </div>
                        <div class="progress-container">
                            <div class="progress-bar ${barClass}" style="width: ${percentage}%;"></div>
                        </div>
                        <div class="diagram-row">
                            <span class="diag-field">Vence el</span>
                            <span class="diag-value description-text" style="font-weight: 600; color: #4a1f14;">${formattedDate}</span>
                        </div>
                        <div class="diagram-row border-top-dash">
                            <span class="diag-field">Porcentaje</span>
                            <span class="diag-status ${statusClass}">${percentage}% - ${statusText}</span>
                        </div>
                    </div>
                </div>
            `;

            // DESPLAZAMIENTO EFECTIVO: Inserta la nueva tarjeta justo antes del botón "Insertar Objetivo"
            if (mainGoalsContainer && addButtonCard) {
                mainGoalsContainer.insertBefore(newCard, addButtonCard);
                
                // Hace un pequeño scroll automático hacia el nuevo objetivo añadido
                mainGoalsContainer.scrollTo({
                    left: mainGoalsContainer.scrollWidth,
                    behavior: 'smooth'
                });
            }

            // Ocultar modal y limpiar campos
            modal.classList.remove('active');
            goalForm.reset();
        });
    }
});