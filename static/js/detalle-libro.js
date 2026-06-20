document.addEventListener('DOMContentLoaded', () => {
document.getElementById('btn-leyendo').disabled = true;
document.getElementById('btn-pendiente').disabled = true;
    cargarLibro();

    const frases = [

        "Buscando ejemplar...",
        "Consultando biblioteca...",
        "Leyendo prólogo...",
        "Abriendo páginas...",
        "Recuperando información...",
        "Explorando catálogo...",
        "Buscando edición más completa...",
        "Organizando estantería..."

    ];

    const textoCarga = document.getElementById("texto-carga-cabecera");

    if(textoCarga){

        textoCarga.textContent =
            frases[Math.floor(Math.random() * frases.length)];

    }

    let yaAgregado = false;

    async function agregarLibro(categoria) {

        if(yaAgregado) return;

        yaAgregado = true;

        const id_usuario = localStorage.getItem('usuario_id');

        if(!id_usuario){

            alert("Debes iniciar sesión para agregar libros.");
            window.location.href = "/sesion";

            return;

        }

        try{

            const respuesta = await fetch('/api/agregar_libro', {

                method:'POST',

                headers:{
                    'Content-Type':'application/json'
                },

                body:JSON.stringify({

                    id_usuario:id_usuario,
                    titulo:datoLibro.titulo,
                    autor:datoLibro.autor,
                    descripcion:datoLibro.descripcion,
                    portada:datoLibro.portada,
                    categoria:categoria,
                    key_libro:datoLibro.key,
                    paginas:datoLibro.paginas

                })

            });

            const resultado = await respuesta.json();

            if(respuesta.status === 201){

                document.getElementById('btn-leyendo').disabled = true;
                document.getElementById('btn-pendiente').disabled = true;

                document.getElementById('btn-leyendo').style.opacity = "0.6";
                document.getElementById('btn-pendiente').style.opacity = "0.6";

                document.getElementById('btn-leyendo').style.cursor = "not-allowed";
                document.getElementById('btn-pendiente').style.cursor = "not-allowed";

                document.getElementById('btn-leyendo').innerText = "✓ Agregado";
                document.getElementById('btn-pendiente').innerText = "✓ Agregado";

            }

            else if(respuesta.status === 409){

                yaAgregado = false;
                alert("Este libro ya está en tu lista.");

            }

            else{

                yaAgregado = false;
                alert(resultado.error || "Error al agregar el libro.");

            }

        }

        catch(error){

            yaAgregado = false;
            alert("No hay conexión con el servidor.");

        }

    }

    document.getElementById('btn-leyendo')
        .addEventListener('click', () => agregarLibro('leyendo'));

    document.getElementById('btn-pendiente')
        .addEventListener('click', () => agregarLibro('pendiente'));

});

async function cargarLibro(){

    try{

        const respuesta = await fetch(
            `/api/libro?clave=${encodeURIComponent(datoLibro.key)}`
        );

        const data = await respuesta.json();

        console.log(data);

        datoLibro.titulo = data.titulo;
        datoLibro.autor = data.autor;
        datoLibro.descripcion = data.descripcion;
        datoLibro.paginas = (data.paginas !== "Desconocido") ? data.paginas : null;

        const cabecera = document.getElementById("cabecera-libro");

        if(cabecera){

            cabecera.innerHTML = `
                <h1>${data.titulo || "Sin título"}</h1>
                <h2 class="book-subtitle">${data.subtitulo || ""}</h2>
                <h3 class="book-author">${data.autor || "Autor desconocido"}</h3>
            `;

        }

        document.getElementById("descripcion").innerHTML =
            data.descripcion || "Descripción no disponible";

        document.getElementById("anio").innerHTML =
            data.anio || "Desconocido";
        
            document.getElementById("paginas").innerHTML =
            data.paginas || "Desconocido";
        
        document.getElementById("generos").innerHTML =
            data.generos || "No disponible";
        
        document.getElementById("pais").innerHTML =
            data.pais || "Desconocido";
        
        document.getElementById("formato").innerHTML =
            data.formato || "Desconocido";   
            
        document.getElementById('btn-leyendo').disabled = false;
        document.getElementById('btn-pendiente').disabled = false;

    }

    catch(error){

        console.error(error);

        const cabecera = document.getElementById("cabecera-libro");

        if(cabecera){

            cabecera.innerHTML = `
                <h1>Error al cargar</h1>
            `;

        }

        document.getElementById("descripcion").innerHTML =
            "No fue posible obtener la información.";

    }

}
