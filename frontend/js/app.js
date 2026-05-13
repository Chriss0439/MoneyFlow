/**
 * app.js
 * Enrutador principal de la aplicación.
 * Maneja qué pantalla (View) se está mostrando.
 */

// Función global para cambiar de pantalla
window.showView = function(viewId) {
    document.querySelectorAll('.view').forEach(el => el.classList.remove('active'));
    document.getElementById(viewId).classList.add('active');

    // Gestión de la Barra de Navegación Global (Componente)
    const navbar = document.getElementById('main-navbar');
    
    // Solo mostrar la barra en estas tres pantallas principales
    if (['view-dashboard', 'view-reports', 'view-categories'].includes(viewId)) {
        navbar.style.display = 'flex';
        
        // Quitar la clase active a todos los botones
        document.querySelectorAll('.nav-btn').forEach(btn => btn.classList.remove('active'));
        
        // Asignar active al botón correspondiente
        if (viewId === 'view-dashboard') document.getElementById('nav-btn-dashboard').classList.add('active');
        if (viewId === 'view-reports') document.getElementById('nav-btn-reports').classList.add('active');
        if (viewId === 'view-categories') document.getElementById('nav-btn-categories').classList.add('active');
        
    } else {
        // Ocultar la barra si estamos en Login, Historial de Categoría, o Agregar Movimiento
        navbar.style.display = 'none';
    }
};

// Función para mostrar notificaciones (Toasts) bonitas en lugar de alert()
window.showToast = function(message, type = 'error') {
    let container = document.getElementById('toast-container');
    if (!container) {
        container = document.createElement('div');
        container.id = 'toast-container';
        container.className = 'toast-container';
        document.body.appendChild(container);
    }

    const toast = document.createElement('div');
    toast.className = `toast ${type}`;
    toast.textContent = message;

    container.appendChild(toast);

    // Remover del DOM después de que termine la animación (3.8s total)
    setTimeout(() => {
        if (toast.parentNode) {
            toast.parentNode.removeChild(toast);
        }
    }, 3800);
};

// Inicializador principal
window.initApp = async function() {
    if (api.isLoggedIn()) {
        showView('view-dashboard');
        // Llamamos al controlador del dashboard
        if (window.dashboardController) {
            await window.dashboardController.loadData();
        }
    } else {
        showView('view-login');
    }
};

// Arrancar cuando el HTML cargue
document.addEventListener('DOMContentLoaded', () => {
    initApp();
});
