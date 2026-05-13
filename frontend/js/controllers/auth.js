/**
 * controllers/auth.js
 * Controlador para la pantalla de Login y Sesiones.
 */

document.getElementById('go-to-register').addEventListener('click', (e) => {
    e.preventDefault(); 
    showView('view-register');
});

document.getElementById('go-to-login').addEventListener('click', (e) => {
    e.preventDefault(); 
    showView('view-login');
});

document.getElementById('btn-logout').addEventListener('click', () => {
    api.logout();
    showView('view-login');
});

document.getElementById('login-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const btn = e.target.querySelector('button');
    btn.textContent = 'Cargando...';
    btn.disabled = true;

    try {
        const correo = document.getElementById('login-email').value;
        const pass = document.getElementById('login-password').value;
        
        const response = await api.login(correo, pass);
        api.setToken(response.access_token);
        
        e.target.reset();
        showView('view-dashboard');
        
        if (window.dashboardController) {
            await window.dashboardController.loadData();
        }
    } catch (error) {
        showToast(error.message, 'error');
    } finally {
        btn.textContent = 'Entrar a mi cuenta';
        btn.disabled = false;
    }
});

// ─── FORMULARIO DE REGISTRO ────────────────────────────────────────────────
document.getElementById('register-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const btn = e.target.querySelector('button');
    btn.textContent = 'Creando cuenta...';
    btn.disabled = true;

    try {
        const nombre  = document.getElementById('reg-name').value;
        const correo  = document.getElementById('reg-email').value;
        const pass    = document.getElementById('reg-password').value;

        const response = await api.register(nombre, correo, pass);
        api.setToken(response.access_token);

        e.target.reset();
        showView('view-dashboard');

        if (window.dashboardController) {
            await window.dashboardController.loadData();
        }
    } catch (error) {
        showToast(error.message, 'error');
    } finally {
        btn.textContent = 'Comenzar';
        btn.disabled = false;
    }
});
