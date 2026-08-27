document.addEventListener('DOMContentLoaded', function() {
    const nombreUsuario = localStorage.getItem('usuario_nombre');
    const btnUsuario = document.getElementById('btn-usuario');
    const dropdown = document.getElementById('user-dropdown');
    const nombreDropdown = document.getElementById('nombre-usuario-dropdown');

    // Elementos del botón de notificaciones
    const btnNotif = document.getElementById('btn-toggle-notif');
    const labelNotif = document.getElementById('notif-btn-label');

    if (!btnUsuario) return;

    if (nombreUsuario) {
        nombreDropdown.innerText = nombreUsuario;
    } else {
        btnUsuario.addEventListener('click', function() {
            window.location.href = "/sesion";
        });
    }

    btnUsuario.addEventListener('click', function(e) {
        if (!nombreUsuario) return;
        dropdown.style.display = dropdown.style.display === 'none' ? 'block' : 'none';
    });

    document.addEventListener('click', function(e) {
        if (!e.target.closest('.user-menu-container')) {
            dropdown.style.display = 'none';
        }
    });

    const btnLogout = document.getElementById('btn-logout');
    if (btnLogout) {
        btnLogout.addEventListener('click', function() {
            localStorage.removeItem('usuario_nombre');
            localStorage.removeItem('usuario_id');
            window.location.href = "/sesion";
        });
    }

    // ==========================================
    // LÓGICA DEL BOTÓN DE NOTIFICACIONES
    // ==========================================
    if (btnNotif) {
        // Consultar el estado inicial al cargar la página
        fetch('/notificaciones/estado')
            .then(res => res.json())
            .then(data => {
                actualizarBotonNotificaciones(data.activadas);
            })
            .catch(() => {
                actualizarBotonNotificaciones(true);
            });

        // Alternar el estado al hacer clic
        btnNotif.addEventListener('click', function(e) {
            e.stopPropagation(); // Evita que se cierre el menú desplegable
            fetch('/notificaciones/toggle', { method: 'POST' })
                .then(res => res.json())
                .then(data => {
                    actualizarBotonNotificaciones(data.activadas);
                });
        });
    }

    function actualizarBotonNotificaciones(activadas) {
        if (activadas) {
            btnNotif.classList.remove('inactive');
            btnNotif.classList.add('active');
            if (labelNotif) labelNotif.innerText = "🔔 Activadas";
        } else {
            btnNotif.classList.remove('active');
            btnNotif.classList.add('inactive');
            if (labelNotif) labelNotif.innerText = "🔕 Desactivadas";
        }
    }

});