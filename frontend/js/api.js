/**
 * api.js
 * Capa de conexión entre el Frontend y el Backend FastAPI
 */

const API_URL = "http://localhost:8000";

const api = {
    // ─── MANEJO DEL TOKEN JWT ──────────────────────────────────────
    setToken: (token) => localStorage.setItem("moneyflow_token", token),
    getToken: () => localStorage.getItem("moneyflow_token"),
    logout: () => localStorage.removeItem("moneyflow_token"),
    isLoggedIn: () => !!localStorage.getItem("moneyflow_token"),

    // ─── HELPER PARA HACER PETICIONES ──────────────────────────────
    request: async (endpoint, options = {}) => {
        const headers = {
            "Content-Type": "application/json",
            ...options.headers
        };

        // Si hay token, inyectarlo
        const token = api.getToken();
        if (token) {
            headers["Authorization"] = `Bearer ${token}`;
        }

        const response = await fetch(`${API_URL}${endpoint}`, {
            ...options,
            headers
        });

        // Si el backend dice "Token expirado o inválido", borramos sesión
        if (response.status === 401 && endpoint !== "/auth/login") {
            api.logout();
            window.location.reload(); 
        }

        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.detail || "Error en el servidor");
        }
        
        return data;
    },

    // ─── ENDPOINTS (LOS MÓDULOS DEL BACKEND) ───────────────────────
    
    // Auth
    login: (correo, password) => 
        api.request("/auth/login", {
            method: "POST",
            body: JSON.stringify({ correo, password })
        }),
        
    register: (nombre, correo, password) => 
        api.request("/auth/register", {
            method: "POST",
            body: JSON.stringify({ nombre, correo, password })
        }),

    getMe: () =>
        api.request("/auth/me", { method: "GET" }),

    // Dashboard
    getDashboard: () => 
        api.request("/dashboard/resumen", { method: "GET" }),

    // Movimientos
    getHistorial: (mes = null, anio = null, categoria_id = null) => {
        let url = "/movimientos/";
        const params = new URLSearchParams();
        if (mes) params.append("mes", mes);
        if (anio) params.append("anio", anio);
        if (categoria_id) params.append("categoria_id", categoria_id);
        if (params.toString()) url += "?" + params.toString();
        
        return api.request(url, { method: "GET" });
    },
        
    createMovimiento: (data) =>
        api.request("/movimientos/", {
            method: "POST",
            body: JSON.stringify(data)
        }),

    deleteMovimiento: (id) =>
        api.request(`/movimientos/${id}`, { method: "DELETE" }),

    // Categorías
    getCategorias: () =>
        api.request("/categorias/", { method: "GET" }),
        
    createCategoria: (data) =>
        api.request("/categorias/", {
            method: "POST",
            body: JSON.stringify(data)
        }),
        
    // Reportes (CU-05)
    getReporteGastos: () =>
        api.request("/reportes/gastos-por-categoria", { method: "GET" }),

    // Presupuestos
    getPresupuestos: () =>
        api.request("/presupuestos/", { method: "GET" }),

    crearPresupuesto: (data) =>
        api.request("/presupuestos/", {
            method: "POST",
            body: JSON.stringify(data),
        }),

    eliminarPresupuesto: (id) =>
        api.request(`/presupuestos/${id}`, { method: "DELETE" }),

    getAlertasPresupuesto: () =>
        api.request("/presupuestos/alertas", { method: "GET" }),
};
