const btn =
document.getElementById("filterBtn");

const menu =
document.getElementById("filterMenu");

btn.addEventListener("click", ()=>{

    menu.classList.toggle("show");

});

// BUSCADOR
const buscador =
document.createElement("input");

buscador.type = "text";
buscador.placeholder = "Buscar género...";
buscador.className = "genre-search";

menu.appendChild(buscador);

// CONTENEDOR DE GÉNEROS
const lista =
document.createElement("div");

lista.id = "genreList";

menu.appendChild(lista);

// CREAR GÉNEROS
GENEROS.forEach(genero=>{

    const enlace =
    document.createElement("a");

    enlace.className =
    "genre-item";

    enlace.href =
    `/filtrar?genero=${encodeURIComponent(genero)}`;

    enlace.textContent =
    genero;

    lista.appendChild(enlace);

});

// FILTRO
buscador.addEventListener("input", ()=>{

    const texto =
    buscador.value.toLowerCase();

    const items =
    lista.querySelectorAll(".genre-item");

    items.forEach(item=>{

        const visible =
        item.textContent
        .toLowerCase()
        .includes(texto);

        item.style.display =
        visible ? "block" : "none";

    });

});


// =====================================================
// ORDENAR
// =====================================================

const sortBtn =
document.getElementById("sortBtn");

const sortMenu =
document.getElementById("sortMenu");

sortBtn.addEventListener("click", () => {

    sortMenu.classList.toggle("show");

});


// OPCIONES DE ORDEN

const opcionesOrden = [
    {
        texto: "Más reciente",
        valor: "reciente"
    },
    {
        texto: "Más antiguo",
        valor: "antiguo"
    },
    {
        texto: "Título A-Z",
        valor: "az"
    },
    {
        texto: "Título Z-A",
        valor: "za"
    }
];


// CREAR OPCIONES

opcionesOrden.forEach(opcion => {

    const enlace =
    document.createElement("a");

    enlace.className =
    "genre-item";

    enlace.href =
    `/?orden=${opcion.valor}`;

    enlace.textContent =
    opcion.texto;

    sortMenu.appendChild(enlace);

});
