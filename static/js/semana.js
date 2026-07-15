document.addEventListener("DOMContentLoaded", () => {

    const weekItems = document.querySelectorAll(".week-item");

    const today = new Date();
    const todayNumber = today.getDate();

    const dayNames = [
        "Dom",
        "Lun",
        "Mar",
        "Mié",
        "Jue",
        "Vie",
        "Sáb"
    ];

    // Generar los 7 días (3 antes + hoy + 3 después)
    const days = [];

    for (let i = -3; i <= 3; i++) {
        const d = new Date(today);
        d.setDate(today.getDate() + i);
        days.push(d);
    }

    weekItems.forEach((item, index) => {

        const date = days[index];

        if (!date) return;

        // Número del día
        const numberEl = item.querySelector(".day-number");
        if (numberEl) {
            numberEl.textContent = date.getDate();
        }

        // Nombre del día
        const nameEl = item.querySelector(".day-name");
        if (nameEl) {
            nameEl.textContent = dayNames[date.getDay()];
        }

        // Resaltar el día de hoy
        if (
            date.getDate() === today.getDate() &&
            date.getMonth() === today.getMonth() &&
            date.getFullYear() === today.getFullYear()
        ) {
            item.classList.add("today");
        }

    });

});

// Cargar fechas marcadas y agregar clicks
async function iniciarMarcasSemana() {
    let fechasMarcadas = {};
    try {
        const res = await fetch('/api/fechas_calendario');
        fechasMarcadas = await res.json();
    } catch(e) {}

    const weekItems = document.querySelectorAll(".week-item");
    const today = new Date();

    const days = [];
    for (let i = -3; i <= 3; i++) {
        const d = new Date(today);
        d.setDate(today.getDate() + i);
        days.push(d);
    }

    weekItems.forEach((item, index) => {
        const date = days[index];
        if (!date) return;

        const fechaStr = `${date.getFullYear()}-${String(date.getMonth()+1).padStart(2,'0')}-${String(date.getDate()).padStart(2,'0')}`;

        if(fechasMarcadas[fechaStr] === 'fin_libro') {
            item.classList.add("fin-libro-day");
            item.style.cursor = "pointer";
            item.addEventListener('click', () => abrirModalSemana(fechaStr));
        } else if(fechasMarcadas[fechaStr] === 'sesion') {
            item.classList.add("sesion-day");
            item.style.cursor = "pointer";
            item.addEventListener('click', () => abrirModalSemana(fechaStr));
        }
    });
}

async function abrirModalSemana(fecha) {
    let modal = document.getElementById('modal-fecha');
    
    if(!modal) {
        modal = document.createElement('div');
        modal.id = 'modal-fecha';
        modal.style.cssText = 'display:none; position:fixed; top:0; left:0; width:100%; height:100%; background:rgba(0,0,0,0.5); z-index:1000; justify-content:center; align-items:center;';
        modal.innerHTML = `
            <div style="background:#f3e7d3; border:3px solid #5b120d; border-radius:20px; padding:30px; max-width:400px; width:90%; position:relative;">
                <button onclick="document.getElementById('modal-fecha').style.display='none'" style="position:absolute; top:10px; right:15px; background:none; border:none; font-size:20px; cursor:pointer; color:#5b120d;">✕</button>
                <h3 id="modal-fecha-titulo" style="color:#5b120d; margin-bottom:15px;"></h3>
                <div id="modal-libros"></div>
            </div>
        `;
        document.body.appendChild(modal);
    }

    document.getElementById('modal-fecha-titulo').textContent = `📅 ${fecha}`;
    document.getElementById('modal-libros').innerHTML = '<p>Cargando...</p>';
    modal.style.display = 'flex';

    try {
        const res = await fetch(`/api/libros_por_fecha?fecha=${fecha}`);
        const libros = await res.json();

        if(libros.length === 0) {
            document.getElementById('modal-libros').innerHTML = '<p>Sin libros registrados.</p>';
            return;
        }

        document.getElementById('modal-libros').innerHTML = libros.map(libro => `
            <div style="display:flex; gap:10px; align-items:center; margin-bottom:15px; background:#efe1cc; border-radius:10px; padding:10px;">
                <img src="${libro.portada || ''}" style="width:50px; height:70px; object-fit:cover; border-radius:5px; background:#ccc;">
                <div>
                    <p style="margin:0; font-weight:bold; color:#5b120d;">${libro.titulo}</p>
                    <p style="margin:0; font-size:13px; color:#7c4f3a;">${libro.autor}</p>
                    <p style="margin:0; font-size:12px; color:#999;">${libro.tipo === 'sesion' ? '📖 Sesión iniciada' : '⏰ Fecha límite'}</p>
                </div>
            </div>
        `).join('');

    } catch(e) {
        document.getElementById('modal-libros').innerHTML = '<p>Error al cargar.</p>';
    }
}

iniciarMarcasSemana();
