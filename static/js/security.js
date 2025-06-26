// Script de seguridad para prevenir navegación hacia atrás después del logout
(function() {
    'use strict';
    
    // Función para verificar si el usuario está autenticado
    function checkAuthentication() {
        // Hacer una petición AJAX para verificar la sesión
        fetch('/check-auth', {
            method: 'GET',
            credentials: 'same-origin'
        })
        .then(response => {
            if (response.status === 401) {
                // Si no está autenticado, redirigir al login (sin mostrar alertas)
                window.location.href = '/login';
                return;
            }
            // Si hay otro error, simplemente no hacer nada aquí
        })
        .catch(error => {
            // No mostrar ninguna alerta, solo loguear en consola si es necesario
            console.error('Error al verificar autenticación:', error);
        });
    }
    
    // Prevenir navegación hacia atrás
    function preventBackNavigation() {
        // Agregar listener para el evento popstate (navegación hacia atrás/adelante)
        window.addEventListener('popstate', function(event) {
            // Verificar autenticación cuando se navega hacia atrás
            checkAuthentication();
        });
        
        // Agregar listener para el evento beforeunload
        window.addEventListener('beforeunload', function(event) {
            // Limpiar cualquier caché local si es necesario
            sessionStorage.removeItem('cachedData');
        });
        
        // Verificar autenticación al cargar la página
        checkAuthentication();
        
        // Verificar autenticación periódicamente (cada 30 segundos)
        setInterval(checkAuthentication, 30000);
    }
    
    // Prevenir almacenamiento en caché del navegador
    function preventCaching() {
        // Agregar timestamp a las URLs para evitar caché
        if (window.location.search.indexOf('_t=') === -1) {
            const separator = window.location.search ? '&' : '?';
            const newUrl = window.location.href + separator + '_t=' + Date.now();
            window.history.replaceState({}, document.title, newUrl);
        }
    }
    
    // Función para limpiar caché al hacer logout
    function clearCacheOnLogout() {
        // Limpiar sessionStorage
        sessionStorage.clear();
        
        // Limpiar localStorage si es necesario
        localStorage.removeItem('userData');
        
        // Forzar recarga sin caché
        window.location.reload(true);
    }
    
    // Función para manejar logout con limpieza de caché
    function handleLogout() {
        // Limpiar caché local
        clearCacheOnLogout();
        
        // Hacer logout en el servidor
        fetch('/logout', {
            method: 'GET',
            credentials: 'same-origin'
        })
        .then(() => {
            // Redirigir al login
            window.location.href = '/login';
        })
        .catch(error => {
            console.error('Error en logout:', error);
            window.location.href = '/login';
        });
    }
    
    // Agregar event listeners a botones de logout
    function setupLogoutButtons() {
        const logoutButtons = document.querySelectorAll('a[href="/logout"], button[onclick*="logout"]');
        logoutButtons.forEach(button => {
            button.addEventListener('click', function(e) {
                e.preventDefault();
                handleLogout();
            });
        });
    }
    
    // Inicializar cuando el DOM esté listo
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', function() {
            preventBackNavigation();
            preventCaching();
            setupLogoutButtons();
        });
    } else {
        preventBackNavigation();
        preventCaching();
        setupLogoutButtons();
    }
    
    // Exponer función para logout
    window.securityUtils = {
        clearCacheOnLogout: clearCacheOnLogout,
        handleLogout: handleLogout
    };
    
})(); 