document.getElementById('formulario-login').addEventListener('submit', async (e) => {
    e.preventDefault(); 

    const correo = document.getElementById('correo-login').value;
    const password = document.getElementById('password-login').value;
    const alerta = document.getElementById('mensaje-alerta');

    
    const datosLogin = {
        correo: correo,
        password: password
    };

    try {
        
        const respuesta = await fetch('http://127.0.0.1:5000/api/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(datosLogin)
        });

        const resultado = await respuesta.json();

        if (respuesta.status === 200) {
            alerta.style.color = "green";
            alerta.innerText = resultado.mensaje;
            
            
           localStorage.setItem('usuario_nombre', resultado.usuario.nombre);
            localStorage.setItem('usuario_id', resultado.usuario.id_usuario); 

            
            setTimeout(() => {
                window.location.href = "/"; 
            }, 1500);
        } else {
            alerta.style.color = "red";
            alerta.innerText = resultado.error || "Credenciales incorrectas.";
        }

    } catch (error) {
        console.error("Error detectado:", error);
        alerta.style.color = "red";
        alerta.innerText = "No hay conexión con el servidor.";
    }
});