document.addEventListener('DOMContentLoaded', () => {

    const toggleFormBtn = document.getElementById('toggle-form-btn');
    const cancelNoteBtn = document.getElementById('cancel-note-btn');
    const formContainer = document.getElementById('note-form-container');
    const newNoteForm = document.getElementById('new-note-form');
    const notesListLayout = document.getElementById('notes-list-layout');
    const dropdownFilterBtn = document.getElementById('dropdown-filter-btn');
    const dropdownMenuOptions = document.getElementById('dropdown-menu-options');
    const bookCoverDisplay = document.getElementById('book-cover-display');
    const currentBookTitle = document.getElementById('current-book-title');
    const currentBookAuthor = document.getElementById('current-book-author');
    const prevBookBtn = document.getElementById('prev-book-btn');
    const nextBookBtn = document.getElementById('next-book-btn');

    let currentSelectedCategory = "Todos";
    let currentLibroId = null;
    let carruselIndex = 0;

    const libros = window.librosCarrusel || [];

    // ========================
    // CARRUSEL
    // ========================
    function actualizarCarrusel() {
        if(libros.length === 0) {
            currentBookTitle.textContent = 'Sin libros';
            currentBookAuthor.textContent = '';
            return;
        }

        const libro = libros[carruselIndex];
        currentLibroId = libro.id;
        currentBookTitle.textContent = libro.titulo;
        currentBookAuthor.textContent = libro.autor;

        if(libro.portada) {
            bookCoverDisplay.innerHTML = `<img src="${libro.portada}" style="width:100%;height:100%;object-fit:cover;border-radius:8px;">`;
        } else {
            bookCoverDisplay.innerHTML = '<span>Portada<br>Libro</span>';
        }

        filterNotes(currentSelectedCategory);
    }

    prevBookBtn.addEventListener('click', () => {
        if(libros.length === 0) return;
        carruselIndex = (carruselIndex - 1 + libros.length) % libros.length;
        actualizarCarrusel();
    });

    nextBookBtn.addEventListener('click', () => {
        if(libros.length === 0) return;
        carruselIndex = (carruselIndex + 1) % libros.length;
        actualizarCarrusel();
    });

    // ========================
    // FILTRADO
    // ========================
function filterNotes(category) {
    document.querySelectorAll('.note-card').forEach(note => {
        const cat = note.getAttribute('data-category');
        const libroId = note.getAttribute('data-libro');
        const libroMatch = currentLibroId === null || String(libroId) === String(currentLibroId);
        const catMatch = category === "Todos" || cat === category;
        if(libroMatch && catMatch) {
            note.style.setProperty('display', 'flex', 'important');
        } else {
            note.style.setProperty('display', 'none', 'important');
        }
    });
}
    dropdownFilterBtn.addEventListener('click', (e) => {
        e.stopPropagation();
        dropdownMenuOptions.classList.toggle('show-menu');
        dropdownFilterBtn.classList.toggle('active-filter');
    });

    document.querySelectorAll('.dropdown-item').forEach(item => {
        item.addEventListener('click', (e) => {
            currentSelectedCategory = e.target.getAttribute('data-value');
            dropdownFilterBtn.innerHTML = `${e.target.textContent} <span class="arrow-down"></span>`;
            dropdownMenuOptions.classList.remove('show-menu');
            dropdownFilterBtn.classList.remove('active-filter');
            filterNotes(currentSelectedCategory);
        });
    });

    document.addEventListener('click', () => {
        dropdownMenuOptions.classList.remove('show-menu');
        dropdownFilterBtn.classList.remove('active-filter');
    });

    // ========================
    // FORMULARIO
    // ========================
    toggleFormBtn.addEventListener('click', () => {
        formContainer.classList.toggle('show');
        if (formContainer.classList.contains('show')) {
            document.getElementById('note-title-input').focus();
        }
    });

    cancelNoteBtn.addEventListener('click', () => {
        newNoteForm.reset();
        formContainer.classList.remove('show');
    });

    newNoteForm.addEventListener('submit', async (e) => {
        e.preventDefault();

        const titulo = document.getElementById('note-title-input').value.trim();
        const contenido = document.getElementById('note-content-input').value.trim();
        const categoria = document.getElementById('note-category-select').value;

        try {
            const res = await fetch('/api/agregar_nota', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ titulo, contenido, categoria, id_libro: currentLibroId })
            });
            const data = await res.json();

            if(res.status === 201) {
                const fecha = new Date().toLocaleDateString('es-ES', { day: 'numeric', month: 'short', year: 'numeric' });
                const card = crearCardNota(data.id_nota, titulo, contenido, categoria, fecha, 'manual', null, currentLibroId);
                notesListLayout.insertBefore(card, notesListLayout.firstChild);
                newNoteForm.reset();
                formContainer.classList.remove('show');
                filterNotes(currentSelectedCategory);
            }
        } catch(err) {
            alert('Error al guardar la nota.');
        }
    });

    // ========================
    // CREAR CARD
    // ========================
    function crearCardNota(id, titulo, contenido, categoria, fecha, tipo, campo = null, libroId = null) {
        const card = document.createElement('div');
        card.className = 'note-card';
        card.setAttribute('data-category', categoria);
        card.setAttribute('data-id', id);
        card.setAttribute('data-tipo', tipo);
        card.setAttribute('data-libro', libroId || '');
        if(campo) card.setAttribute('data-campo', campo);

        card.innerHTML = `
            <div class="note-header">
                <div class="note-title-wrapper">
                    <h3 class="note-title">${titulo}</h3>
                    <span class="note-category-badge">${categoria}</span>
                </div>
                <span class="note-date">${fecha}</span>
            </div>
            <div class="note-body"><p>${contenido}</p></div>
            <div class="note-footer">
                <button class="note-action-btn edit-btn">Editar</button>
                <button class="note-action-btn delete-btn" ${tipo === 'sesion' ? 'disabled style="opacity:0.4;"' : ''}>Borrar</button>
            </div>
        `;

        asignarEventos(card);
        return card;
    }

    // ========================
    // EDITAR
    // ========================
    function asignarEventos(card) {
        card.querySelector('.edit-btn').addEventListener('click', () => editarNota(card));
        const deleteBtn = card.querySelector('.delete-btn');
        if(!deleteBtn.disabled) {
            deleteBtn.addEventListener('click', () => borrarNota(card));
        }
    }

    function editarNota(card) {
        const tipo = card.getAttribute('data-tipo');
        const id = card.getAttribute('data-id');
        const campo = card.getAttribute('data-campo');
        const body = card.querySelector('.note-body p');
        const titulo = card.querySelector('.note-title');
        const contenidoActual = body.textContent;
        const tituloActual = titulo.textContent;

        if(tipo === 'sesion') {
            const textarea = document.createElement('textarea');
            textarea.value = contenidoActual;
            textarea.className = 'form-textarea';
            textarea.rows = 3;
            body.replaceWith(textarea);

            const btnGuardar = document.createElement('button');
            btnGuardar.textContent = 'Guardar';
            btnGuardar.className = 'note-action-btn submit-note-btn';
            card.querySelector('.note-footer').prepend(btnGuardar);
            card.querySelector('.edit-btn').style.display = 'none';

            btnGuardar.addEventListener('click', async () => {
                const nuevoValor = textarea.value.trim();
                await fetch('/api/editar_nota', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ tipo: 'sesion', id_nota: id, campo, valor: nuevoValor })
                });
                const p = document.createElement('p');
                p.textContent = nuevoValor;
                textarea.replaceWith(p);
                btnGuardar.remove();
                card.querySelector('.edit-btn').style.display = '';
            });

        } else {
            const inputTitulo = document.createElement('input');
            inputTitulo.value = tituloActual;
            inputTitulo.className = 'form-input';
            titulo.replaceWith(inputTitulo);

            const textarea = document.createElement('textarea');
            textarea.value = contenidoActual;
            textarea.className = 'form-textarea';
            textarea.rows = 3;
            body.replaceWith(textarea);

            const btnGuardar = document.createElement('button');
            btnGuardar.textContent = 'Guardar';
            btnGuardar.className = 'note-action-btn submit-note-btn';
            card.querySelector('.note-footer').prepend(btnGuardar);
            card.querySelector('.edit-btn').style.display = 'none';

            btnGuardar.addEventListener('click', async () => {
                const nuevoTitulo = inputTitulo.value.trim();
                const nuevoContenido = textarea.value.trim();
                const categoria = card.getAttribute('data-category');

                await fetch('/api/editar_nota', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ tipo: 'manual', id_nota: id, titulo: nuevoTitulo, contenido: nuevoContenido, categoria })
                });

                const h3 = document.createElement('h3');
                h3.className = 'note-title';
                h3.textContent = nuevoTitulo;
                inputTitulo.replaceWith(h3);

                const p = document.createElement('p');
                p.textContent = nuevoContenido;
                textarea.replaceWith(p);
                btnGuardar.remove();
                card.querySelector('.edit-btn').style.display = '';
            });
        }
    }

    // ========================
    // BORRAR
    // ========================
    async function borrarNota(card) {
        if(!confirm('¿Borrar esta nota?')) return;
        const id = card.getAttribute('data-id');
        await fetch('/api/eliminar_nota', {
            method: 'DELETE',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ tipo: 'manual', id_nota: id })
        });
        card.remove();
    }

    // ========================
    // ASIGNAR EVENTOS A CARDS EXISTENTES
    // ========================
    document.querySelectorAll('.note-card').forEach(card => asignarEventos(card));

    // ========================
    // INICIAR CARRUSEL
    // ========================
    actualizarCarrusel();

});