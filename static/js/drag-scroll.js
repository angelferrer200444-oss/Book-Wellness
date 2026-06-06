document.addEventListener("DOMContentLoaded", () => {

    document.querySelectorAll(".books-row").forEach(row => {

        let isDown = false;
        let startX;
        let scrollLeft;

        // CLICK Y DRAG (PC)
        row.addEventListener("mousedown", (e) => {
            isDown = true;
            startX = e.pageX - row.offsetLeft;
            scrollLeft = row.scrollLeft;
        });

        row.addEventListener("mouseleave", () => {
            isDown = false;
        });

        row.addEventListener("mouseup", () => {
            isDown = false;
        });

        row.addEventListener("mousemove", (e) => {
            if (!isDown) return;
            e.preventDefault();

            const x = e.pageX - row.offsetLeft;
            const walk = (x - startX) * 2; // velocidad
            row.scrollLeft = scrollLeft - walk;
        });

    });

});
