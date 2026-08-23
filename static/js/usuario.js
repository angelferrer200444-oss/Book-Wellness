document.addEventListener('DOMContentLoaded', function() {
    const nombreUsuario = localStorage.getItem('usuario_nombre');
    const btnUsuario = document.getElementById('btn-usuario');
    const dropdown = document.getElementById('user-dropdown');
    const nombreDropdown = document.getElementById('nombre-usuario-dropdown');
    const btnNotificaciones = document.getElementById('btn-notificaciones');

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
    if (btnNotificaciones) {
        // Consultar el estado inicial al cargar
        fetch('/notificaciones/estado')
            .then(res => res.json())
            .then(data => {
                actualizarTextoNotificaciones(data.activadas);
            })
            .catch(() => {
                btnNotificaciones.innerText = "🔔 Notificaciones: Activadas";
            });

        // Alternar al hacer clic
        btnNotificaciones.addEventListener('click', function(e) {
            e.stopPropagation(); // Evita que se cierre el dropdown
            fetch('/notificaciones/toggle', { method: 'POST' })
                .then(res => res.json())
                .then(data => {
                    actualizarTextoNotificaciones(data.activadas);
                });
        });
    }

    function actualizarTextoNotificaciones(activadas) {
        if (activadas) {
            btnNotificaciones.innerText = "🔔 Notificaciones: Activadas";
        } else {
            btnNotificaciones.innerText = "🔕 Notificaciones: Desactivadas";
        }
    }

});