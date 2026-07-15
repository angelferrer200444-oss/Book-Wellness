const monthYear = document.getElementById("monthYear");
const calendarDates = document.getElementById("calendarDates");
const prevBtn = document.getElementById("prevMonth");
const nextBtn = document.getElementById("nextMonth");

const months = [
    "Enero", "Febrero", "Marzo", "Abril",
    "Mayo", "Junio", "Julio", "Agosto",
    "Septiembre", "Octubre", "Noviembre", "Diciembre"
];

let currentDate = new Date();
let fechasMarcadas = {};

async function cargarFechas() {
    try {
        const res = await fetch('/api/fechas_calendario');
        fechasMarcadas = await res.json();
    } catch(e) {
        fechasMarcadas = {};
    }
    renderCalendar();
}

function renderCalendar() {
    const year = currentDate.getFullYear();
    const month = currentDate.getMonth();

    monthYear.textContent = `${months[month]} ${year}`;
    calendarDates.innerHTML = "";

    const firstDay = new Date(year, month, 1).getDay();
    const lastDate = new Date(year, month + 1, 0).getDate();
    const today = new Date();

    for(let i = 0; i < firstDay; i++) {
        calendarDates.appendChild(document.createElement("span"));
    }

    for(let day = 1; day <= lastDate; day++) {
        const dateElement = document.createElement("span");
        dateElement.textContent = day;

        const fechaStr = `${year}-${String(month + 1).padStart(2,'0')}-${String(day).padStart(2,'0')}`;

        if(day === today.getDate() && month === today.getMonth() && year === today.getFullYear()) {
            dateElement.classList.add("active-day");
        }

        if(fechasMarcadas[fechaStr] === 'fin_libro') {
            dateElement.classList.add("fin-libro-day");
            dateElement.style.cursor = "pointer";
            dateElement.addEventListener('click', () => abrirModal(fechaStr));
        } else if(fechasMarcadas[fechaStr] === 'sesion') {
            dateElement.classList.add("sesion-day");
            dateElement.style.cursor = "pointer";
            dateElement.addEventListener('click', () => abrirModal(fechaStr));
        }

        calendarDates.appendChild(dateElement);
    }
}

async function abrirModal(fecha) {
    const modal = document.getElementById('modal-fecha');
    if(!modal) return;

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
            <div style="display:flex; gap:10px; align-items:center; margin-bottom:15px;
                        background:#efe1cc; border-radius:10px; padding:10px;">
                <img src="${libro.portada || ''}" style="width:50px; height:70px; object-fit:cover;
                     border-radius:5px; background:#ccc;">
                <div>
                    <p style="margin:0; font-weight:bold; color:#5b120d;">${libro.titulo}</p>
                    <p style="margin:0; font-size:13px; color:#7c4f3a;">${libro.autor}</p>
                    <p style="margin:0; font-size:12px; color:#999;">
                        ${libro.tipo === 'sesion' ? '📖 Sesión iniciada' : '⏰ Fecha límite'}
                    </p>
                </div>
            </div>
        `).join('');

    } catch(e) {
        document.getElementById('modal-libros').innerHTML = '<p>Error al cargar.</p>';
    }
}

function cerrarModal() {
    const modal = document.getElementById('modal-fecha');
    if(modal) modal.style.display = 'none';
}

prevBtn.addEventListener("click", () => {
    currentDate.setMonth(currentDate.getMonth() - 1);
    renderCalendar();
});

nextBtn.addEventListener("click", () => {
    currentDate.setMonth(currentDate.getMonth() + 1);
    renderCalendar();
});

cargarFechas();