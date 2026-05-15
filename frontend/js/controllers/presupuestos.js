/**
 * controllers/presupuestos.js
 * Controlador para el módulo de Presupuestos con Alertas.
 */

window.presupuestosController = {

    formatMoney: (n) => `Q ${parseFloat(n).toFixed(2)}`,

    // ── Cargar lista de presupuestos ──────────────────────────────────
    loadData: async function () {
        try {
            const [presupuestos, categorias] = await Promise.all([
                api.getPresupuestos(),
                api.getCategorias(),
            ]);

            // Poblar select de categorías de gasto
            const select = document.getElementById('presup-categoria');
            const gastoCats = categorias.filter(c => c.tipo === 'gasto');
            select.innerHTML = '<option value="">Selecciona una categoría...</option>';
            gastoCats.forEach(c => {
                select.innerHTML += `<option value="${c.id}">${c.nombre}</option>`;
            });

            // Pintar la lista
            const lista = document.getElementById('presup-list');
            lista.innerHTML = '';

            if (presupuestos.length === 0) {
                lista.innerHTML = '<div class="empty-state">Aún no tienes presupuestos definidos.</div>';
                return;
            }

            presupuestos.forEach(p => {
                const colorBarra = p.estado === 'excedido' ? '#FFB3B3'
                    : p.estado === 'advertencia' ? '#FFE1B3'
                    : '#B3FFD1';

                const iconEstado = p.estado === 'excedido' ? '🔴'
                    : p.estado === 'advertencia' ? '🟡'
                    : '🟢';

                const periodo = p.mes && p.anio
                    ? `${p.mes}/${p.anio}`
                    : p.mes ? `Mes ${p.mes}` : 'Todos los meses';

                lista.innerHTML += `
                    <div class="glass-card" style="margin-bottom: 12px; padding: 16px;">
                        <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 10px;">
                            <div>
                                <h4 style="margin: 0; font-size: 1rem; color: var(--text-main);">
                                    ${iconEstado} ${p.categoria_nombre}
                                </h4>
                                <small style="color: var(--text-muted);">${periodo}</small>
                            </div>
                            <div style="text-align: right;">
                                <strong style="color: var(--text-main);">${this.formatMoney(p.gastado)}</strong>
                                <small style="display: block; color: var(--text-muted);">de ${this.formatMoney(p.limite)}</small>
                            </div>
                        </div>
                        <!-- Barra de progreso -->
                        <div style="width: 100%; height: 8px; background: #F4F4F5; border-radius: 4px; overflow: hidden; margin-bottom: 8px;">
                            <div style="width: ${Math.min(p.pct_usado, 100)}%; height: 100%; background: ${colorBarra}; border-radius: 4px; transition: width 0.5s ease;"></div>
                        </div>
                        <div style="display: flex; justify-content: space-between; align-items: center;">
                            <small style="color: var(--text-muted);">${p.pct_usado}% utilizado</small>
                            <button class="btn-delete-presup" data-id="${p.id}"
                                style="background: none; border: none; color: var(--text-muted); cursor: pointer; font-size: 0.8rem; padding: 2px 6px;">
                                🗑 Eliminar
                            </button>
                        </div>
                    </div>
                `;
            });

            // Eventos de eliminar
            document.querySelectorAll('.btn-delete-presup').forEach(btn => {
                btn.addEventListener('click', async (e) => {
                    if (confirm('¿Eliminar este presupuesto?')) {
                        const id = e.currentTarget.getAttribute('data-id');
                        try {
                            await api.eliminarPresupuesto(id);
                            showToast('Presupuesto eliminado.', 'success');
                            this.loadData();
                            // Refrescar alertas en dashboard
                            window.presupuestosController.cargarAlertas();
                        } catch (err) {
                            showToast('Error: ' + err.message, 'error');
                        }
                    }
                });
            });

        } catch (err) {
            console.error('Error al cargar presupuestos:', err);
        }
    },

    // ── Guardar nuevo presupuesto ─────────────────────────────────────
    guardar: async function () {
        const categoriaId = parseInt(document.getElementById('presup-categoria').value);
        const limite = parseFloat(document.getElementById('presup-limite').value);
        const mes = parseInt(document.getElementById('presup-mes').value) || null;
        const anio = parseInt(document.getElementById('presup-anio').value) || null;

        if (!categoriaId || !limite || limite <= 0) {
            showToast('Selecciona una categoría y un límite válido.', 'error');
            return;
        }

        try {
            await api.crearPresupuesto({ categoria_id: categoriaId, limite, mes, anio });
            showToast('Presupuesto guardado ✓', 'success');
            document.getElementById('form-presupuesto').reset();
            this.loadData();
            window.presupuestosController.cargarAlertas();
        } catch (err) {
            showToast('Error: ' + err.message, 'error');
        }
    },

    // ── Cargar alertas en el banner del Dashboard ─────────────────────
    cargarAlertas: async function () {
        const banner = document.getElementById('banner-alertas');
        if (!banner) return;

        try {
            const alertas = await api.getAlertasPresupuesto();
            banner.innerHTML = '';

            if (alertas.length === 0) {
                banner.style.display = 'none';
                return;
            }

            banner.style.display = 'block';
            alertas.forEach(a => {
                const isExcedido = a.estado === 'excedido';
                const color = isExcedido ? '#FFB3B3' : '#FFE1B3';
                const colorTexto = isExcedido ? '#991b1b' : '#92400e';
                const icono = isExcedido ? '🔴' : '🟡';
                const msg = isExcedido
                    ? `Límite excedido en <strong>${a.categoria_nombre}</strong>: gastaste ${this.formatMoney(a.gastado)} de ${this.formatMoney(a.limite)}`
                    : `Cerca del límite en <strong>${a.categoria_nombre}</strong>: ${a.pct_usado}% utilizado`;

                banner.innerHTML += `
                    <div style="background: ${color}; color: ${colorTexto}; border-radius: 10px;
                                padding: 10px 14px; margin-bottom: 8px; font-size: 0.82rem; line-height: 1.5;">
                        ${icono} ${msg}
                    </div>
                `;
            });
        } catch (err) {
            console.error('Error al cargar alertas:', err);
        }
    },
};

// ── Formulario de nuevo presupuesto ───────────────────────────────────
document.getElementById('form-presupuesto').addEventListener('submit', (e) => {
    e.preventDefault();
    window.presupuestosController.guardar();
});

// ── Botón volver desde presupuestos ──────────────────────────────────
document.getElementById('btn-back-from-presupuestos').addEventListener('click', () => {
    showView('view-dashboard');
});
