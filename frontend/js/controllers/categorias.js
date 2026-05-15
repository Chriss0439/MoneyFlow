/**
 * Controlador de Categorías
 * Maneja la visualización de la lista de categorías y el formulario para añadir nuevas.
 */

window.categoriasController = {
    loadData: async function() {
        try {
            const categorias = await api.getCategorias();
            document.getElementById('input-search-categorias').value = '';
            filtrarCategorias('');
            
            const listIngresos = document.getElementById('categorias-ingreso-list');
            const listGastos = document.getElementById('categorias-gasto-list');
            
            listIngresos.innerHTML = '';
            listGastos.innerHTML = '';
            
            // Paleta de colores pastel para los iconos (igual que el mockup)
            const pastelColors = ['#D1B3FF', '#FFB3B3', '#B3FFD1', '#B3D1FF', '#FFE1B3'];

            categorias.forEach((cat, index) => {
                const color = pastelColors[index % pastelColors.length];
                const bg = `${color}33`; // con opacidad
                const textCol = color.replace('FF', '99'); // más oscuro para el ícono

                const cardHTML = `
                    <div class="glass-card" onclick="window.categoriasController.showHistory(${cat.id}, '${cat.nombre}')" style="margin-bottom: 12px; padding: 16px; display: flex; justify-content: space-between; align-items: center; cursor: pointer;">
                        <div style="display: flex; align-items: center; gap: 16px;">
                            <div style="width: 48px; height: 48px; background: ${bg}; color: ${textCol}; border-radius: 12px; display: flex; align-items: center; justify-content: center; font-weight: bold; font-size: 1.2rem;">
                                ${cat.nombre.charAt(0).toUpperCase()}
                            </div>
                            <div>
                                <h4 style="margin: 0; font-size: 1.05rem; color: var(--text-main); font-weight: 600;">${cat.nombre}</h4>
                                <small style="color: var(--text-muted);">${cat.tipo === 'ingreso' ? 'Entrada' : 'Salida'} de dinero</small>
                            </div>
                        </div>
                        <div style="color: var(--text-muted);">
                            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M9 18l6-6-6-6"/></svg>
                        </div>
                    </div>
                `;

                if (cat.tipo === 'ingreso') {
                    listIngresos.innerHTML += cardHTML;
                } else {
                    listGastos.innerHTML += cardHTML;
                }
            });

        } catch (error) {
            console.error("Error al cargar categorías:", error);
            showToast("Error al cargar las categorías.", 'error');
        }
    },

    showHistory: async function(categoria_id, nombre) {
        showView('view-category-history');
        document.getElementById('cat-history-title').textContent = nombre;
        
        const historyList = document.getElementById('cat-history-list');
        historyList.innerHTML = '<div class="empty-state">Cargando...</div>';

        try {
            // El API ahora recibe: mes, anio, categoria_id
            const historial = await api.getHistorial(null, null, categoria_id);
            historyList.innerHTML = ''; 

            if (historial.length === 0) {
                historyList.innerHTML = '<div class="empty-state">No hay movimientos para esta categoría.</div>';
                return;
            }

            historial.forEach(mov => {
                const isIngreso = mov.tipo_categoria === 'ingreso';
                const colorClass = isIngreso ? 'text-green' : 'text-red';
                const sign = isIngreso ? '+' : '-';
                
                historyList.innerHTML += `
                    <div class="history-item">
                        <div class="history-item-left">
                            <h4>${mov.descripcion || 'Sin descripción'}</h4>
                            <small>${mov.fecha}</small>
                        </div>
                        <div class="history-item-right ${colorClass}" style="font-weight: 700;">
                            ${sign}Q ${parseFloat(mov.monto).toFixed(2)}
                        </div>
                    </div>
                `;
            });
        } catch (error) {
            console.error("Error al cargar historial de categoría:", error);
            historyList.innerHTML = '<div class="empty-state">Error al cargar datos.</div>';
        }
    }
};

// ================= BÚSQUEDA =================

function filtrarCategorias(query) {
    const q = query.toLowerCase().trim();

    const ingresoCards = document.querySelectorAll('#categorias-ingreso-list .glass-card');
    const gastoCards   = document.querySelectorAll('#categorias-gasto-list .glass-card');

    let visiblesIngreso = 0;
    let visiblesGasto   = 0;

    ingresoCards.forEach(card => {
        const nombre = card.querySelector('h4').textContent.toLowerCase();
        const visible = nombre.includes(q);
        card.style.display = visible ? '' : 'none';
        if (visible) visiblesIngreso++;
    });

    gastoCards.forEach(card => {
        const nombre = card.querySelector('h4').textContent.toLowerCase();
        const visible = nombre.includes(q);
        card.style.display = visible ? '' : 'none';
        if (visible) visiblesGasto++;
    });

    document.getElementById('section-header-ingresos').style.display = visiblesIngreso > 0 ? '' : 'none';
    document.getElementById('section-header-gastos').style.display   = visiblesGasto   > 0 ? '' : 'none';
}

document.getElementById('input-search-categorias').addEventListener('input', (e) => {
    filtrarCategorias(e.target.value);
});

// ================= NAVEGACIÓN =================

// Abrir formulario para añadir nueva
document.getElementById('btn-show-add-category').addEventListener('click', () => {
    showView('view-add-category');
});

// Cancelar formulario
document.getElementById('btn-cancel-category').addEventListener('click', () => {
    document.getElementById('form-category').reset();
    showView('view-categories');
});

// ================= FORMULARIO =================
// Enviar nueva categoría al Backend
document.getElementById('form-category').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const data = {
        nombre: document.getElementById('cat-nombre').value,
        tipo: document.getElementById('cat-tipo').value
    };

    try {
        const btn = document.getElementById('btn-submit-cat');
        btn.disabled = true;
        btn.textContent = 'Guardando...';

        await api.createCategoria(data);

        // Limpiar, volver y recargar
        document.getElementById('form-category').reset();
        showView('view-categories');
        window.categoriasController.loadData();
        
        // También recargar el formulario de "Añadir Movimiento" del Dashboard 
        // para que la nueva categoría aparezca en el select
        if (window.movimientosController) {
            window.movimientosController.cargarCategorias();
        }

    } catch (error) {
        showToast("Error al crear categoría: " + error.message, 'error');
    } finally {
        const btn = document.getElementById('btn-submit-cat');
        btn.disabled = false;
        btn.textContent = 'Guardar Categoría';
    }
});
