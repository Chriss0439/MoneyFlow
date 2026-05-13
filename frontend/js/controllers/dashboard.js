/**
 * controllers/dashboard.js
 * Controlador para la pantalla principal y las gráficas.
 */

window.dashboardController = {
    chartInstance: null,

    formatMoney: (amount) => `Q ${parseFloat(amount).toFixed(2)}`,

    loadData: async function() {
        try {
            // Cargar datos del usuario
            const user = await api.getMe();
            // Tomar el primer nombre para que no sea muy largo
            const firstName = user.nombre.split(' ')[0];
            document.getElementById('user-name-display').textContent = firstName;

            // Leer valores de los filtros
            const mesVal = document.getElementById('filter-mes').value;
            const anioVal = document.getElementById('filter-anio').value;

            // Totales (Aún no filtramos el dashboard completo, solo el historial visual)
            const dashboard = await api.getDashboard();
            document.getElementById('balance-total').textContent = this.formatMoney(dashboard.saldo_actual);
            document.getElementById('balance-ingresos').textContent = this.formatMoney(dashboard.total_ingresos);
            document.getElementById('balance-gastos').textContent = this.formatMoney(dashboard.total_gastos);

            // Historial (Pasando filtros)
            const historial = await api.getHistorial(mesVal || null, anioVal || null);
            const historyList = document.getElementById('history-list');
            historyList.innerHTML = ''; 
            
            if (historial.length === 0) {
                historyList.innerHTML = '<div class="empty-state">No hay movimientos recientes</div>';
                return;
            }

            historial.slice(0, 5).forEach(mov => {
                const isIngreso = mov.tipo_categoria === 'ingreso';
                const colorClass = isIngreso ? 'text-green' : 'text-red';
                const sign = isIngreso ? '+' : '-';
                
                historyList.innerHTML += `
                    <div class="history-item">
                        <div class="history-item-left">
                            <h4>${mov.descripcion || 'Sin descripción'}</h4>
                            <small>${mov.fecha}</small>
                        </div>
                        <div class="history-item-right ${colorClass}" style="display: flex; align-items: center; gap: 12px;">
                            ${sign}${this.formatMoney(mov.monto)}
                            <button class="btn-delete-mov" data-id="${mov.id}" title="Eliminar" style="background:none; border:none; color:var(--text-muted); cursor:pointer; padding:4px; display:flex; align-items:center;">
                                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="transition: stroke 0.2s;" onmouseover="this.style.stroke='var(--danger)'" onmouseout="this.style.stroke='currentColor'">
                                  <path d="M3 6h18"></path>
                                  <path d="M19 6v14c0 1-1 2-2 2H7c-1 0-2-1-2-2V6"></path>
                                  <path d="M8 6V4c0-1 1-2 2-2h4c1 0 2 1 2 2v2"></path>
                                </svg>
                            </button>
                        </div>
                    </div>
                `;
            });
            
            // Adjuntar eventos a los basureros recién creados
            document.querySelectorAll('.btn-delete-mov').forEach(btn => {
                btn.addEventListener('click', async (e) => {
                    if(confirm("¿Estás seguro de eliminar este registro?")) {
                        const id = e.currentTarget.getAttribute('data-id');
                        try {
                            await api.deleteMovimiento(id);
                            window.dashboardController.loadData(); // Recargar todo
                        } catch (err) {
                            showToast("Error al borrar: " + err.message, 'error');
                        }
                    }
                });
            });

        } catch (error) {
            console.error("Error al cargar dashboard:", error);
        }
    },

    loadReport: async function() {
        try {
            const datos = await api.getReporteGastos();
            if (datos.length === 0) {
                showToast("Aún no tienes gastos para graficar.", 'info');
                showView('view-dashboard');
                return;
            }

            const labels = datos.map(d => d.categoria);
            const totales = datos.map(d => d.total);
            
            // Sumar el gran total para el centro
            const granTotal = totales.reduce((a, b) => a + b, 0);
            document.getElementById('chart-total-text').textContent = this.formatMoney(granTotal);
            
            // Paleta de colores pastel del Mockup
            const pastelColors = ['#D1B3FF', '#FFB3B3', '#B3FFD1', '#B3D1FF', '#FFE1B3'];
            
            if (this.chartInstance) {
                this.chartInstance.destroy();
            }

            const ctx = document.getElementById('gastosChart').getContext('2d');
            this.chartInstance = new Chart(ctx, {
                type: 'doughnut',
                data: {
                    labels: labels,
                    datasets: [{
                        data: totales,
                        backgroundColor: pastelColors,
                        borderWidth: 0,
                        hoverOffset: 4,
                        borderRadius: 15, // Puntas redondeadas
                        cutout: '80%' // Dona muy delgada
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: { display: false } // Ocultar leyenda nativa
                    }
                }
            });

            // Pintar la lista de Mayores Gastos con barras de progreso
            const mayoresList = document.getElementById('mayores-gastos-list');
            mayoresList.innerHTML = '';
            
            datos.sort((a,b) => b.total - a.total).forEach((d, index) => {
                const color = pastelColors[index % pastelColors.length];
                const porcentaje = Math.round((d.total / granTotal) * 100);
                
                mayoresList.innerHTML += `
                    <div class="glass-card" style="margin-bottom: 12px; padding: 16px;">
                        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;">
                            <div style="display: flex; align-items: center; gap: 12px;">
                                <div style="width: 40px; height: 40px; background: ${color}33; color: ${color.replace('FF','99')}; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: bold;">
                                    ${d.categoria.charAt(0)}
                                </div>
                                <div>
                                    <h4 style="margin: 0; font-size: 1rem; color: var(--text-main);">${d.categoria}</h4>
                                    <small style="color: var(--text-muted);">${porcentaje}% del total</small>
                                </div>
                            </div>
                            <strong style="font-size: 1.1rem; color: var(--text-main);">${this.formatMoney(d.total)}</strong>
                        </div>
                        <!-- Barra de progreso -->
                        <div style="width: 100%; height: 6px; background: #F4F4F5; border-radius: 4px; overflow: hidden;">
                            <div style="width: ${porcentaje}%; height: 100%; background: ${color}; border-radius: 4px;"></div>
                        </div>
                    </div>
                `;
            });

        } catch (error) {
            console.error("Error al cargar reporte:", error);
        }
    }
};

// Event Listeners del Dashboard
document.getElementById('btn-back-from-reports').addEventListener('click', () => {
    showView('view-dashboard');
});

// Detectar cambios en los filtros para recargar historial
document.getElementById('filter-mes').addEventListener('change', () => {
    window.dashboardController.loadData();
});
document.getElementById('filter-anio').addEventListener('change', () => {
    window.dashboardController.loadData();
});
