document.getElementById('formulario-registro').addEventListener('submit', async (e) => {
    e.preventDefault(); 

    
    const nombre = document.getElementById('nombre').value;
    const correo = document.getElementById('correo').value;
    const password = document.getElementById('password').value;
    const nivelLectura = document.getElementById('nivel').value;
    const alerta = document.getElementById('mensaje-alerta');
    
    const emailValido = /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(correo);
if (!emailValido) {
    alerta.style.color = "red";
    alerta.innerText = "Por favor ingresa un correo electrónico válido.";
    return;
}

    
    const datosUsuario = {
        nombre: nombre,
        correo: correo,
        password: password,
        nivel: nivelLectura
    };

    try {
        
        const respuesta = await fetch('http://127.0.0.1:5000/api/registrar_usuario', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(datosUsuario)
        });

        const resultado = await respuesta.json();

        if (respuesta.status === 201) {
    alerta.style.color = "green";
    alerta.innerText = resultado.mensaje;
    document.getElementById('formulario-registro').reset();
    
    setTimeout(() => {
        window.location.href = "/sesion";
    }, 1500);  
        } else {
            alerta.style.color = "red";
            alerta.innerText = resultado.error || "Error al registrar.";
        }

    } catch (error) {
        console.error("Error:", error);
        alerta.style.color = "red";
        alerta.innerText = "No hay conexión con el servidor de Python.";
    }
});