document.addEventListener("DOMContentLoaded", () => {

    const weekItems = document.querySelectorAll(".week-item");

    const today = new Date();

    const dayNames = [
        "Dom",
        "Lun",
        "Mar",
        "Mié",
        "Jue",
        "Vie",
        "Sáb"
    ];

    const days = [];

    for (let i = -3; i <= 3; i++) {
        const d = new Date(today);
        d.setDate(today.getDate() + i);
        days.push(d);
    }

    weekItems.forEach((item, index) => {

        const date = days[index];

        if (!date) return;

        const numberEl = item.querySelector(".day-number");
        if (numberEl) {
            numberEl.textContent = date.getDate();
        }

        const nameEl = item.querySelector(".day-name");
        if (nameEl) {
            nameEl.textContent = dayNames[date.getDay()];
        }

        if (
            date.getDate() === today.getDate() &&
            date.getMonth() === today.getMonth() &&
            date.getFullYear() === today.getFullYear()
        ) {
            item.classList.add("today");
        }

    });

});

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

    const claseTipo = {
        'fecha_limite': 'fecha-limite-day',
        'expirada': 'expirada-day',
        'concluido': 'concluido-day',
        'primera_sesion': 'primera-sesion-day',
        'sesion': 'sesion-day'
    };

    weekItems.forEach((item, index) => {
        const date = days[index];
        if (!date) return;

        const fechaStr = `${date.getFullYear()}-${String(date.getMonth()+1).padStart(2,'0')}-${String(date.getDate()).padStart(2,'0')}`;
        const tipo = fechasMarcadas[fechaStr];
        const clase = claseTipo[tipo];

        if(clase) {
            item.classList.add(clase);
            item.style.cursor = "pointer";
            item.addEventListener('click', () => {
                window.location.href = `/seguimiento?fecha=${fechaStr}`;
            });
        }
    });
}

document.addEventListener("DOMContentLoaded", iniciarMarcasSemana);