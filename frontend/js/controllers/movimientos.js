/**
 * controllers/movimientos.js
 * Controlador para la creación de nuevos ingresos o gastos.
 */

window.movimientosController = {
    categoriasDisponibles: [],

    cargarCategorias: async function() {
        try {
            this.categoriasDisponibles = await api.getCategorias();
        } catch (error) {
            console.error("Error recargando categorías", error);
        }
    },

    openForm: async function(tipo) {
        document.getElementById('mov-tipo').value = tipo;
        document.getElementById('add-mov-title').textContent = tipo === 'ingreso' ? 'Nuevo Ingreso' : 'Nuevo Gasto';
        document.getElementById('form-movement').reset();
        showView('view-add-movement');

        if (this.categoriasDisponibles.length === 0) {
            try {
                this.categoriasDisponibles = await api.getCategorias();
            } catch (error) {
                console.error("Error cargando categorías", error);
                return;
            }
        }

        const select = document.getElementById('mov-categoria');
        select.innerHTML = '<option value="">Selecciona una categoría</option>';
        
        this.categoriasDisponibles
            .filter(c => c.tipo === tipo)
            .forEach(c => {
                select.innerHTML += `<option value="${c.id}">${c.nombre}</option>`;
            });
    }
};

// Listeners
document.getElementById('btn-add-income').addEventListener('click', () => {
    window.movimientosController.openForm('ingreso');
});

document.getElementById('btn-add-expense').addEventListener('click', () => {
    window.movimientosController.openForm('gasto');
});

document.getElementById('btn-back-dashboard').addEventListener('click', () => {
    showView('view-dashboard');
});

document.getElementById('form-movement').addEventListener('submit', async (e) => {
    e.preventDefault();
    const btn = document.getElementById('btn-submit-mov');
    btn.textContent = 'Guardando...';
    btn.disabled = true;

    try {
        const payload = {
            categoria_id: parseInt(document.getElementById('mov-categoria').value),
            monto: parseFloat(document.getElementById('mov-monto').value),
            descripcion: document.getElementById('mov-desc').value || "",
            es_apoyo_familiar: false
        };

        await api.createMovimiento(payload);
        
        showView('view-dashboard');
        if (window.dashboardController) {
            await window.dashboardController.loadData();
        }
    } catch (error) {
        showToast("Error al guardar: " + error.message, 'error');
    } finally {
        btn.textContent = 'Guardar';
        btn.disabled = false;
    }
});
