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
