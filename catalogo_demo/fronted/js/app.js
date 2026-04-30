// URL de la API
const API_URL = "http://localhost:8000/api/productos";
const ADMIN_URL = "http://localhost:8000/admin/productos";

let todosLosProductos = [];
let categoriasUnicas = [];
let modoAdmin = false;
let filtroActivo = "todas";   // para recordar el filtro actual

document.addEventListener("DOMContentLoaded", () => {
    obtenerProductos();
    configurarToggleAdmin();
    configurarFormularioCrear();
});

// ------------------- TOGGLE ADMIN -------------------
function configurarToggleAdmin() {
    const btn = document.getElementById("btn-admin");  // Coincide con el HTML
    btn.addEventListener("click", () => {
        modoAdmin = !modoAdmin;
        if (modoAdmin) {
            btn.textContent = "🔧 Desactivar Admin";
            btn.classList.add("activo");
            document.getElementById("admin-panel").style.display = "block";
        } else {
            btn.textContent = "🔧 Activar Admin";
            btn.classList.remove("activo");
            document.getElementById("admin-panel").style.display = "none";
        }
        // Repintar con el filtro activo
        aplicarFiltro();
    });
}

// ------------------- OBTENER PRODUCTOS -------------------
async function obtenerProductos() {
    try {
        const respuesta = await fetch(API_URL);
        if (!respuesta.ok) throw new Error("Error al obtener productos");
        todosLosProductos = await respuesta.json();
        extraerCategorias();
        aplicarFiltro();  // Mostrar productos según el filtro activo
        configurarBotonesFiltro();
    } catch (error) {
        console.error("Error:", error);
        document.getElementById("contenedor-productos").innerHTML =
            "<p style='text-align:center;padding:2rem;color:red'>Error al cargar el catálogo. ¿Está corriendo el backend?</p>";
    }
}

// ------------------- CATEGORÍAS -------------------
function extraerCategorias() {
    const categorias = todosLosProductos.map(p => p.categoria).filter(Boolean);
    categoriasUnicas = [...new Set(categorias)];
    generarBotonesFiltro();
}

function generarBotonesFiltro() {
    const nav = document.getElementById("filtros-nav");
    nav.innerHTML = '<button class="filtro-btn activo" data-categoria="todas">Todas</button>';
    categoriasUnicas.forEach(cat => {
        const btn = document.createElement("button");
        btn.className = "filtro-btn";
        btn.dataset.categoria = cat;
        btn.textContent = cat;
        if (cat === filtroActivo) btn.classList.add("activo"); 
        nav.appendChild(btn);
    });
}

function configurarBotonesFiltro() {
    document.getElementById("filtros-nav").addEventListener("click", (e) => {
        if (e.target.classList.contains("filtro-btn")) {
            document.querySelectorAll(".filtro-btn").forEach(btn => btn.classList.remove("activo"));
            e.target.classList.add("activo");
            filtroActivo = e.target.dataset.categoria;  // Guardar filtro activo
            aplicarFiltro();
        }
    });
}

function aplicarFiltro() {
    let productosAMostrar;
    if (filtroActivo === "todas") {
        productosAMostrar = todosLosProductos;
    } else {
        productosAMostrar = todosLosProductos.filter(p => p.categoria === filtroActivo);
    }
    mostrarProductos(productosAMostrar);
}

// ------------------- MOSTRAR PRODUCTOS -------------------
function mostrarProductos(lista) {
    const contenedor = document.getElementById("contenedor-productos");
    const sinResultados = document.getElementById("sin-resultados");
    contenedor.innerHTML = "";

    if (lista.length === 0) {
        sinResultados.style.display = "block";
        return;
    } else {
        sinResultados.style.display = "none";
    }

    lista.forEach(producto => {
        const card = document.createElement("article");
        card.className = "producto-card";

        const imgSrc = producto.imagen || "img/placeholder.jpg";
        card.innerHTML = `
            <img src="${imgSrc}" alt="${producto.nombre}" onerror="this.onerror=null;this.src='https://via.placeholder.com/300x200?text=Sin+Imagen';">
            <div class="producto-info">
                <span class="categoria-badge">${producto.categoria || 'Sin categoría'}</span>
                <h3>${producto.nombre}</h3>
                <p class="descripcion">${producto.descripcion || ''}</p>
                <p class="precio">$${producto.precio.toFixed(2)}</p>
                ${modoAdmin ? `<button class="btn-eliminar" data-id="${producto.id}">🗑 Eliminar</button>` : ''}
            </div>
        `;

        if (modoAdmin) {
            const btnEliminar = card.querySelector(".btn-eliminar");
            btnEliminar.addEventListener("click", () => eliminarProducto(producto.id));
        }

        contenedor.appendChild(card);
    });
}

// ------------------- ADMIN: CREAR PRODUCTO -------------------
function configurarFormularioCrear() {
    const form = document.getElementById("form-producto");  // Coincide con el HTML
    form.addEventListener("submit", async (e) => {
        e.preventDefault();
        const producto = {
            nombre: document.getElementById("nombre").value,
            descripcion: document.getElementById("descripcion").value || null,
            precio: parseFloat(document.getElementById("precio").value),
            categoria: document.getElementById("categoria").value || null,
            imagen: document.getElementById("imagen").value || null,
        };

        try {
            const respuesta = await fetch(ADMIN_URL, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(producto)
            });
            if (!respuesta.ok) throw new Error("Error al crear producto");
            const nuevoProducto = await respuesta.json();
            document.getElementById("mensaje-admin").innerHTML =
                `<span style="color:green;">✅ Producto "${nuevoProducto.nombre}" creado correctamente.</span>`;
            form.reset();
            obtenerProductos();  // Recargar y mantener filtro
        } catch (error) {
            console.error(error);
            document.getElementById("mensaje-admin").innerHTML =
                `<span style="color:red;">❌ Error al crear producto.</span>`;
        }
    });
}

// ------------------- ADMIN: ELIMINAR PRODUCTO -------------------
async function eliminarProducto(id) {
    if (!confirm("¿Seguro que quieres eliminar este producto?")) return;

    try {
        const respuesta = await fetch(`${ADMIN_URL}/${id}`, { method: "DELETE" });
        if (!respuesta.ok) throw new Error("Error al eliminar");
        obtenerProductos();  // Recargar lista
    } catch (error) {
        console.error(error);
        alert("Error al eliminar el producto.");
    }
}