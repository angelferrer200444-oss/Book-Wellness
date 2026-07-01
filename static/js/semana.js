document.addEventListener("DOMContentLoaded", () => {

    const weekItems = document.querySelectorAll(".week-item");

    const today = new Date();

    // Día del mes de hoy (ej: 1, 2, 30)
    const todayNumber = today.getDate();

    // Obtener días de esta "semana visual"
    // (3 días antes + hoy + 3 días después)
    const days = [];

    for (let i = -3; i <= 3; i++) {
        const d = new Date(today);
        d.setDate(today.getDate() + i);
        days.push(d);
    }

    weekItems.forEach((item, index) => {

        const date = days[index];

        if (!date) return;

        const dayNumber = date.getDate();

        // Poner número en el cuadro
        const numberEl = item.querySelector(".day-number");
        if (numberEl) {
            numberEl.textContent = dayNumber;
        }

        // Marcar hoy
        if (dayNumber === todayNumber) {
            item.classList.add("today");
        }

    });

});
