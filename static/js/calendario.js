const months = [
    "Enero", "Febrero", "Marzo", "Abril",
    "Mayo", "Junio", "Julio", "Agosto",
    "Septiembre", "Octubre", "Noviembre", "Diciembre"
];

const iconosAnimo = {
    'Feliz': '😊',
    'Tranquilo': '😌',
    'Reflexivo': '🤔',
    'Sorprendido': '😮',
    'Triste': '😢',
    'Ansioso': '😰'
};

let currentDate = new Date();
let fechasMarcadas = {};

let monthYear, calendarDates, prevBtn, nextBtn;

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

    if(monthYear) monthYear.textContent = `${months[month]} ${year}`;
    if(!calendarDates) return;
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

        if(fechasMarcadas[fechaStr] === 'concluido') {
            dateElement.classList.add("concluido-day");
            dateElement.style.cursor = "pointer";
            dateElement.addEventListener('click', () => abrirModal(fechaStr));
        } else if(fechasMarcadas[fechaStr] === 'fecha_limite') {
            dateElement.classList.add("fecha-limite-day");
            dateElement.style.cursor = "pointer";
            dateElement.addEventListener('click', () => abrirModal(fechaStr));
        } else if(fechasMarcadas[fechaStr] === 'sesion') {
            dateElement.classList.add("sesion-day");
            dateElement.style.cursor = "pointer";
            dateElement.addEventListener('click', () => abrirModal(fechaStr));
        }

        if(fechasMarcadas[fechaStr] === 'primera_sesion') {
            dateElement.classList.add("primera-sesion-day");
            dateElement.style.cursor = "pointer";
            dateElement.addEventListener('click', () => abrirModal(fechaStr));
        }
        if(fechasMarcadas[fechaStr] === 'expirada') {
            dateElement.classList.add("expirada-day");
            dateElement.style.cursor = "pointer";
            dateElement.addEventListener('click', () => abrirModal(fechaStr));
        }


        calendarDates.appendChild(dateElement);
    }
}

async function abrirModal(fecha) {
    // Seguimiento: actualizar timeline
    const timeline = document.getElementById('timeline-contenido');
    if(timeline) {
        const [anio, mes, dia] = fecha.split('-');
        const tituloEl = document.getElementById('timeline-titulo');
        if(tituloEl) tituloEl.textContent = `${parseInt(dia)} DE ${months[parseInt(mes)-1].toUpperCase()} ${anio}`;

        timeline.innerHTML = '<p style="color:#5a1c11; opacity:0.7;">Cargando...</p>';

        try {
            const res = await fetch(`/api/eventos_seguimiento?fecha=${fecha}`);
            const eventos = await res.json();

            if(eventos.length === 0) {
                timeline.innerHTML = '<p style="color:#5a1c11; opacity:0.7; text-align:center;">Sin eventos en esta fecha.</p>';
                return;
            }

                                timeline.innerHTML = eventos.map(ev => {
        const esSesion = ev.tipo === 'sesion' || ev.tipo === 'primera_sesion';
        const esConcluido = ev.tipo === 'concluido';
        const esLimite = ev.tipo === 'fecha_limite';
        const esExpirada = ev.tipo === 'expirada';

        let descLimite = '';
        if(esLimite || esExpirada) {
            if(ev.estado === 'He terminado el libro' && ev.fecha_fin && ev.fecha_limite) {
                const fin = new Date(ev.fecha_fin);
                const limite = new Date(ev.fecha_limite);
                const diasSobraron = Math.round((limite - fin) / (1000 * 60 * 60 * 24));
                descLimite = diasSobraron >= 0
                    ? `✅ Completada antes · ${diasSobraron} días de sobra`
                    : `⏰ Terminado ${Math.abs(diasSobraron)} días tarde`;
            } else if(esExpirada) {
                descLimite = `❌ Venció sin terminar el libro`;
            } else {
                descLimite = `⏳ Aún en plazo`;
            }
        }
        

                    let terminadoTarde = false;
        if(ev.estado === 'He terminado el libro' && ev.fecha_fin && ev.fecha_limite) {
            const fin = new Date(ev.fecha_fin);
            const limite = new Date(ev.fecha_limite);
            terminadoTarde = fin > limite;
        }

        const badge = esSesion
            ? (ev.tipo === 'primera_sesion' ? '🌟 Primera Sesión' : 'Sesión')
            : esConcluido ? '✅ Concluido'
            : (ev.estado === 'He terminado el libro'
                ? (terminadoTarde ? '⏰ Completada tarde' : '✅ Completada')
                : esExpirada ? '❌ Vencida'
                : '⏳ En curso');

                const badgeClass = (esSesion || esConcluido)
            ? 'status-completed'
            : esExpirada ? 'status-expired'
            : 'status-pending';
            
                const fechaStr = ev.fecha_inicio || ev.fecha || ev.fecha_limite || ev.fecha_fin || '';
        const [anioEv, mesEv, diaEv] = fechaStr.split(' ')[0].split('-');
        const diaNum = parseInt(diaEv);
        const mesNom = months[parseInt(mesEv)-1].substring(0,3).toUpperCase();

        let horaEv = '';
        if(fechaStr.includes(' ')) {
            horaEv = fechaStr.split(' ')[1].substring(0, 5);
        }

        const desc = esSesion
            ? `${ev.tipo === 'primera_sesion' ? '🌟 Primera sesión · ' : ''}${horaEv ? '🕐 ' + horaEv + ' · ' : ''}📖 ${ev.paginas_leidas || 0} páginas · ⏱️ ${Math.floor((ev.tiempo_minutos || 0) / 60)}h ${(ev.tiempo_minutos || 0) % 60}m${ev.como_te_sientes ? ' · ' + (iconosAnimo[ev.como_te_sientes] || '') + ' ' + ev.como_te_sientes : ''}`
            : esConcluido
            ? `🎉 Libro terminado · 📖 ${ev.paginas_leidas || 0} páginas totales`
            : descLimite;
            
        if(fechaStr.includes(' ')) {
            horaEv = fechaStr.split(' ')[1].substring(0, 5);
        }

                return `
                    <div class="timeline-item ${badgeClass}">
                        <div class="date-box">
                            <div class="date-info">
                                <span class="day">${diaNum}</span>
                                <span class="month">${mesNom}</span>
                            </div>
                            <div class="time-bar">${esSesion ? '📖 Sesión' : esConcluido ? '✅ Concluido' : esExpirada ? '⚠️ Expirada' : '⏰ Límite'}</div>
                        </div>
                        <div class="event-card">
                            <div class="badge">${badge}</div>
                            <h3 class="event-title">${ev.titulo}</h3>
                            <p class="event-desc">${desc}</p>
                            
                        </div>
                    </div>
                `;
            }).join('');

        } catch(e) {
            timeline.innerHTML = '<p style="color:#5a1c11; opacity:0.7;">Error al cargar eventos.</p>';
        }
        return;
    }

    // Index: modal
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

function cerrarModal() {
    const modal = document.getElementById('modal-fecha');
    if(modal) modal.style.display = 'none';
}

document.addEventListener('DOMContentLoaded', async () => {
    monthYear = document.getElementById("monthYear");
    calendarDates = document.getElementById("calendarDates");
    prevBtn = document.getElementById("prevMonth");
    nextBtn = document.getElementById("nextMonth");

    if(prevBtn) prevBtn.addEventListener("click", () => {
        currentDate.setMonth(currentDate.getMonth() - 1);
        renderCalendar();
    });

    if(nextBtn) nextBtn.addEventListener("click", () => {
        currentDate.setMonth(currentDate.getMonth() + 1);
        renderCalendar();
    });

    const params = new URLSearchParams(window.location.search);
    const fechaParam = params.get('fecha');

    if(fechaParam) {
        const [anio, mes, dia] = fechaParam.split('-').map(Number);
        currentDate = new Date(anio, mes - 1, dia);
    }

    await cargarFechas();

    if(fechaParam) {
        abrirModal(fechaParam);
    }
});