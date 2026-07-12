document.addEventListener('DOMContentLoaded', () => {
    const toggleFormBtn = document.getElementById('toggle-form-btn');
    const cancelNoteBtn = document.getElementById('cancel-note-btn');
    const formContainer = document.getElementById('note-form-container');
    const newNoteForm = document.getElementById('new-note-form');
    const notesListLayout = document.getElementById('notes-list-layout');
    const noteCategorySelect = document.getElementById('note-category-select');

    const dropdownFilterBtn = document.getElementById('dropdown-filter-btn');
    const dropdownMenuOptions = document.getElementById('dropdown-menu-options');

    let currentSelectedCategory = "Todos";

    // Función de filtrado de notas
    function filterNotes(category) {
        const notes = notesListLayout.querySelectorAll('.note-card');
        notes.forEach(note => {
            const noteCategory = note.getAttribute('data-category');
            if (category === "Todos" || noteCategory === category) {
                note.style.setProperty('display', 'flex', 'important');
                note.style.opacity = '1';
            } else {
                note.style.setProperty('display', 'none', 'important');
            }
        });
    }

    // Desplegar menú de filtros
    dropdownFilterBtn.addEventListener('click', (e) => {
        e.stopPropagation();
        dropdownMenuOptions.classList.toggle('show-menu');
        dropdownFilterBtn.classList.toggle('active-filter');
    });

    // Cambiar filtro al hacer clic en una opción
    document.querySelectorAll('.dropdown-item').forEach(item => {
        item.addEventListener('click', (e) => {
            currentSelectedCategory = e.target.getAttribute('data-value');
            const buttonText = e.target.textContent;
            dropdownFilterBtn.innerHTML = `${buttonText} <span class="arrow-down"></span>`;
            dropdownMenuOptions.classList.remove('show-menu');
            dropdownFilterBtn.classList.remove('active-filter');
            filterNotes(currentSelectedCategory);
        });
    });

    // Cerrar el filtro si se hace clic fuera de él
    document.addEventListener('click', () => {
        dropdownMenuOptions.classList.remove('show-menu');
        dropdownFilterBtn.classList.remove('active-filter');
    });

    // Mostrar u ocultar el formulario de nueva nota
    function toggleForm() {
        formContainer.classList.toggle('show');
        if (formContainer.classList.contains('show')) {
            document.getElementById('note-title-input').focus();
        }
    }

    toggleFormBtn.addEventListener('click', toggleForm);
    
    cancelNoteBtn.addEventListener('click', () => {
        newNoteForm.reset();
        formContainer.classList.remove('show');
    });

    // Guardar una nueva nota
    newNoteForm.addEventListener('submit', (e) => {
        e.preventDefault();

        const title = document.getElementById('note-title-input').value;
        const content = document.getElementById('note-content-input').value;
        const noteAssignedCategory = noteCategorySelect.value;

        const dateOptions = { day: 'numeric', month: 'short', year: 'numeric' };
        const formattedDate = new Date().toLocaleDateString('es-ES', dateOptions)
            .replace('.', '')
            .replace(/^(\d+)\s([a-z])/, (m, p1, p2) => p1 + ' ' + p2.toUpperCase());

        const noteCard = document.createElement('div');
        noteCard.className = 'note-card new-note-animation';
        noteCard.setAttribute('data-category', noteAssignedCategory);
        
        noteCard.innerHTML = `
            <div class="note-header">
                <div class="note-title-wrapper">
                    <h3 class="note-title">${title}</h3>
                    <span class="note-category-badge">${noteAssignedCategory}</span>
                </div>
                <span class="note-date">${formattedDate}</span>
            </div>
            <div class="note-body">
                <p>${content}</p>
            </div>
            <div class="note-footer">
                <button class="note-action-btn edit-btn">Editar</button>
                <button class="note-action-btn delete-btn">Borrar</button>
            </div>
        `;

        // Insertar la nota al principio de la lista
        notesListLayout.insertBefore(noteCard, notesListLayout.firstChild);

        // Limpiar y cerrar formulario
        newNoteForm.reset();
        formContainer.classList.remove('show');
        
        // Aplicar filtro actual
        filterNotes(currentSelectedCategory);
        
        if (noteCard.style.display !== 'none') {
            noteCard.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
        }

        // Asignar evento de borrar a la nueva nota
        noteCard.querySelector('.delete-btn').addEventListener('click', () => {
            noteCard.remove();
        });
    });

    // Asignar evento de borrar a las notas predeterminadas del HTML
    document.querySelectorAll('.note-card .delete-btn').forEach(btn => {
        btn.addEventListener('click', (e) => {
            e.target.closest('.note-card').remove();
        });
    });
});