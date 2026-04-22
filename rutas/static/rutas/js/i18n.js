/**
 * RutasEAFIT - Sistema de Internacionalización (i18n)
 * Soporta Español (es) e Inglés (en)
 * Idioma por defecto: Español
 */

const translations = {
    es: {
        // ============================
        // LOGIN PAGE
        // ============================
        "login.title": "RutaMedellín",
        "login.subtitle": "Tu guía de transporte universitario",
        "login.email_label": "Correo electrónico",
        "login.email_placeholder": "tucorreo@gmail.com",
        "login.password_label": "Contraseña",
        "login.password_placeholder": "••••••••",
        "login.submit": "Iniciar sesión",
        "login.no_account": "¿No tienes cuenta?",
        "login.register_link": "Regístrate aquí",
        "login.tagline": "Viaja sin complicaciones: Encuentra las rutas más fáciles desde EAFIT a Medellín y de vuelta en un solo clic.",

        // ============================
        // REGISTRO PAGE
        // ============================
        "register.title": "Crea tu cuenta",
        "register.subtitle": "Únete a la comunidad de RutaMedellín",
        "register.name_label": "Nombre completo",
        "register.name_placeholder": "Ej. Juan Pérez",
        "register.email_label": "Correo electrónico",
        "register.email_placeholder": "tucorreo@gmail.com",
        "register.password_label": "Contraseña",
        "register.password_placeholder": "Mínimo 8 caracteres",
        "register.confirm_label": "Confirmar contraseña",
        "register.confirm_placeholder": "Repite tu contraseña",
        "register.submit": "Comenzar a viajar",
        "register.has_account": "¿Ya tienes una cuenta?",
        "register.login_link": "Inicia sesión aquí",

        // ============================
        // INICIO / BUSCADOR PAGE
        // ============================
        "nav.route_finder": "Buscador de Rutas",
        "nav.subtitle": "Transporte Público de Medellín",
        "nav.logout": "Cerrar sesión",
        "search.where_from": "¿Desde dónde?",
        "search.where_to": "¿Hacia dónde?",
        "search.prefer_label": "Preferir rutas que sean:",
        "search.reset_filters": "Limpiar Filtros",
        "search.fastest": "⚡ Más rápida",
        "search.fastest_desc": "Menor tiempo",
        "search.direct": "🛤️ Directa",
        "search.direct_desc": "Sin transbordos",
        "search.cheapest": "💰 Más barata",
        "search.cheapest_desc": "Mejor precio",
        "search.find_routes": "🔍 Buscar Rutas",
        "search.invalid_title": "Búsqueda no válida",
        "search.routes_available": "Rutas Disponibles",
        "search.no_routes": "No se encontraron rutas que coincidan con tu búsqueda.",
        "search.clear_filters": "Limpiar Filtros",
        "search.select_route": "Seleccionar Ruta",
        "search.view_details": "Ver Detalles de Ruta",
        "search.mixed_route": "Ruta Mixta",
        "search.transfer_at": "Transbordo en",
        "search.best": "⭐ MEJOR",

        // ============================
        // DETALLES PAGE
        // ============================
        "detail.your_route": "Tu Ruta Seleccionada",
        "detail.transport_system": "Sistema de Transporte de Medellín",
        "detail.back_search": "Volver a búsqueda",
        "detail.from": "DESDE",
        "detail.to": "HASTA",
        "detail.route_details": "Detalles de Ruta",
        "detail.total_time": "Tiempo Total",
        "detail.total_fare": "Tarifa Total",
        "detail.departure": "SALIDA",
        "detail.arrival": "LLEGADA",
        "detail.ai_tip_title": "Tip de tu Asesor IA",
        "detail.open_map": "Abrir Mapa Interactivo",
        "detail.all_stops": "Todas las Paradas de la Ruta",
        "detail.time": "Hora",
        "detail.other_departures": "Otras Salidas Disponibles",
        "detail.other_departures_desc": "Elige un horario o tipo de bus diferente para el mismo destino",
        "detail.selected": "Seleccionada",
        "detail.current": "Actual",

        // ============================
        // MAPA PAGE
        // ============================
        "map.route_to": "Ruta hacia",
        "map.from": "Desde",
        "map.route_info": "Información de Ruta",
        "map.route_from_to": "Ruta desde",
        "map.to": "hasta",
        "map.buses_title": "Buses a Tomar",
        "map.buses_desc": "Estos buses te llevarán desde",
        "map.trip_costs": "Costos del Viaje",
        "map.total_fare": "Tarifa Total:",
        "map.route_details": "Detalles de Ruta",
        "map.estimated_duration": "Duración estimada",
        "map.total_stops": "Total de paradas",
        "map.stops_including": "paradas incluyendo origen y destino",
        "map.main_streets": "Calles Principales",
        "map.step_nav": "Navegación Paso a Paso",
        "map.prev": "Anterior",
        "map.next_step": "Siguiente Paso",
        "map.finish": "Finalizar",
        "map.starting_point": "Punto de Partida",
        "map.transfer_point": "Punto de Transbordo",
        "map.destination": "Destino",

        // ============================
        // 404 PAGE
        // ============================
        "error.title": "404",
        "error.subtitle": "¡Ruta perdida!",
        "error.message": "Parece que el bus tomó un desvío. La parada que buscas no existe o ha sido movida.",
        "error.back": "🔙 Regresar al Buscador",

        // ============================
        // LANGUAGE SWITCHER
        // ============================
        "lang.current": "Español",
        "lang.es": "Español",
        "lang.en": "English",
    },

    en: {
        // ============================
        // LOGIN PAGE
        // ============================
        "login.title": "RutaMedellín",
        "login.subtitle": "Your university transport guide",
        "login.email_label": "Email address",
        "login.email_placeholder": "youremail@gmail.com",
        "login.password_label": "Password",
        "login.password_placeholder": "••••••••",
        "login.submit": "Log in",
        "login.no_account": "Don't have an account?",
        "login.register_link": "Register here",
        "login.tagline": "Travel hassle-free: Find the easiest routes from EAFIT to Medellín and back with just one click.",

        // ============================
        // REGISTRO PAGE
        // ============================
        "register.title": "Create your account",
        "register.subtitle": "Join the RutaMedellín community",
        "register.name_label": "Full name",
        "register.name_placeholder": "e.g. John Doe",
        "register.email_label": "Email address",
        "register.email_placeholder": "youremail@gmail.com",
        "register.password_label": "Password",
        "register.password_placeholder": "Minimum 8 characters",
        "register.confirm_label": "Confirm password",
        "register.confirm_placeholder": "Repeat your password",
        "register.submit": "Start traveling",
        "register.has_account": "Already have an account?",
        "register.login_link": "Log in here",

        // ============================
        // INICIO / BUSCADOR PAGE
        // ============================
        "nav.route_finder": "Route Finder",
        "nav.subtitle": "Medellín Public Transport",
        "nav.logout": "Log out",
        "search.where_from": "Where from?",
        "search.where_to": "Where to?",
        "search.prefer_label": "Prefer routes that are:",
        "search.reset_filters": "Reset Filters",
        "search.fastest": "⚡ Fastest",
        "search.fastest_desc": "Shortest time",
        "search.direct": "🛤️ Direct",
        "search.direct_desc": "Fewer changes",
        "search.cheapest": "💰 Cheapest",
        "search.cheapest_desc": "Best price",
        "search.find_routes": "🔍 Find Routes",
        "search.invalid_title": "Invalid search",
        "search.routes_available": "Routes Available",
        "search.no_routes": "No routes found matching your criteria.",
        "search.clear_filters": "Clear Filters",
        "search.select_route": "Select This Route",
        "search.view_details": "View Route Details",
        "search.mixed_route": "Mixed Route",
        "search.transfer_at": "Transfer at",
        "search.best": "⭐ BEST",

        // ============================
        // DETALLES PAGE
        // ============================
        "detail.your_route": "Your Selected Route",
        "detail.transport_system": "Medellín Transportation System",
        "detail.back_search": "Back to search",
        "detail.from": "FROM",
        "detail.to": "TO",
        "detail.route_details": "Route Details",
        "detail.total_time": "Total Time",
        "detail.total_fare": "Total Fare",
        "detail.departure": "DEPARTURE",
        "detail.arrival": "ARRIVAL",
        "detail.ai_tip_title": "AI Advisor Tip",
        "detail.open_map": "Open Interactive Map",
        "detail.all_stops": "All Stops Along Route",
        "detail.time": "Time",
        "detail.other_departures": "Other Available Departures",
        "detail.other_departures_desc": "Choose a different time or bus type for the same destination",
        "detail.selected": "Selected",
        "detail.current": "Current",

        // ============================
        // MAPA PAGE
        // ============================
        "map.route_to": "Route to",
        "map.from": "From",
        "map.route_info": "Route Information",
        "map.route_from_to": "Route from",
        "map.to": "to",
        "map.buses_title": "Buses to Take",
        "map.buses_desc": "These buses will take you from",
        "map.trip_costs": "Trip Costs",
        "map.total_fare": "Total Fare:",
        "map.route_details": "Route Details",
        "map.estimated_duration": "Estimated duration",
        "map.total_stops": "Total stops",
        "map.stops_including": "stops including origin and destination",
        "map.main_streets": "Main Streets",
        "map.step_nav": "Step-by-Step Navigation",
        "map.prev": "Prev",
        "map.next_step": "Next Step",
        "map.finish": "Finish",
        "map.starting_point": "Starting Point",
        "map.transfer_point": "Transfer Point",
        "map.destination": "Destination",

        // ============================
        // 404 PAGE
        // ============================
        "error.title": "404",
        "error.subtitle": "Route not found!",
        "error.message": "It seems the bus took a detour. The stop you're looking for doesn't exist or has been moved.",
        "error.back": "🔙 Back to Search",

        // ============================
        // LANGUAGE SWITCHER
        // ============================
        "lang.current": "English",
        "lang.es": "Español",
        "lang.en": "English",
    }
};

/**
 * Obtiene el idioma actual del localStorage o devuelve 'es' por defecto
 */
function getCurrentLang() {
    return localStorage.getItem('rutaseafit_lang') || 'es';
}

/**
 * Aplica las traducciones a todos los elementos con data-i18n
 */
function applyTranslations(lang) {
    const dict = translations[lang];
    if (!dict) return;

    // Traducir contenido de texto
    document.querySelectorAll('[data-i18n]').forEach(el => {
        const key = el.getAttribute('data-i18n');
        if (dict[key]) {
            el.textContent = dict[key];
        }
    });

    // Traducir placeholders de inputs
    document.querySelectorAll('[data-i18n-placeholder]').forEach(el => {
        const key = el.getAttribute('data-i18n-placeholder');
        if (dict[key]) {
            el.placeholder = dict[key];
        }
    });

    // Traducir atributos title
    document.querySelectorAll('[data-i18n-title]').forEach(el => {
        const key = el.getAttribute('data-i18n-title');
        if (dict[key]) {
            el.title = dict[key];
        }
    });

    // Actualizar el atributo lang del html
    document.documentElement.lang = lang === 'es' ? 'es' : 'en';

    // Actualizar el texto del botón del selector de idioma
    const langBtnText = document.getElementById('lang-btn-text');
    if (langBtnText) {
        langBtnText.textContent = dict['lang.current'];
    }

    // Marcar el idioma activo en el dropdown
    document.querySelectorAll('.lang-option').forEach(opt => {
        const optLang = opt.getAttribute('data-lang');
        const checkmark = opt.querySelector('.lang-check');
        if (checkmark) {
            checkmark.style.opacity = optLang === lang ? '1' : '0';
        }
    });
}

/**
 * Cambia el idioma y lo guarda en localStorage
 */
function setLanguage(lang) {
    localStorage.setItem('rutaseafit_lang', lang);
    applyTranslations(lang);
    // Cerrar el dropdown
    const dropdown = document.getElementById('lang-dropdown');
    if (dropdown) {
        dropdown.classList.add('lang-dropdown-hidden');
    }
}

/**
 * Alterna la visibilidad del dropdown de idioma
 */
function toggleLangDropdown(event) {
    event.stopPropagation();
    const dropdown = document.getElementById('lang-dropdown');
    if (dropdown) {
        dropdown.classList.toggle('lang-dropdown-hidden');
    }
}

/**
 * Inicialización automática al cargar la página
 */
document.addEventListener('DOMContentLoaded', function () {
    const lang = getCurrentLang();
    applyTranslations(lang);

    // Cerrar dropdown al hacer click fuera
    document.addEventListener('click', function (e) {
        const dropdown = document.getElementById('lang-dropdown');
        const btn = document.getElementById('lang-switcher-btn');
        if (dropdown && btn && !btn.contains(e.target) && !dropdown.contains(e.target)) {
            dropdown.classList.add('lang-dropdown-hidden');
        }
    });
});
