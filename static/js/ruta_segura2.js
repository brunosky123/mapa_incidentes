// Variables globales
var map;
var startMarker, endMarker;
var startPoint = null, endPoint = null;
var routingControl = null;
var peligrosLayer;
var incidentesLayer;
var zonasSegurasLayer;
var markersCluster;

// Inicializar el mapa
function initMap() {
    // Verificar que Leaflet esté cargado
    if (!window.L) {
        console.error('Leaflet no está cargado');
        return;
    }

    map = L.map('map').setView([-12.0600, -77.0300], 13);

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 19,
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
    }).addTo(map);

    // Configurar eventos para selección de puntos
    setupPointSelection();

    // Cargar datos de zonas peligrosas y seguras
    loadSafetyData();
}

// Configurar selección de puntos de inicio y destino
function setupPointSelection() {
    var startButton = document.getElementById('set-start');
    var endButton = document.getElementById('set-end');
    var calculateButton = document.getElementById('calculate-route');
    var clearButton = document.getElementById('clear-route');

    var selectionMode = null;

    startButton.addEventListener('click', function() {
        selectionMode = 'start';
        alert('Ahora haz clic en el mapa para seleccionar el punto de inicio');
    });

    endButton.addEventListener('click', function() {
        selectionMode = 'end';
        alert('Ahora haz clic en el mapa para seleccionar el punto de destino');
    });

    map.on('click', function(e) {
        if (selectionMode === 'start') {
            setStartPoint(e.latlng);
            selectionMode = null;
        } else if (selectionMode === 'end') {
            setEndPoint(e.latlng);
            selectionMode = null;
        }
    });

    calculateButton.addEventListener('click', calculateSafeRoute);
    clearButton.addEventListener('click', clearRoute);
}

// Establecer punto de inicio
function setStartPoint(latlng) {
    if (startMarker) {
        map.removeLayer(startMarker);
    }

    startPoint = latlng;
    startMarker = L.marker(latlng, {
        icon: L.divIcon({
            className: 'start-marker',
            html: '<div style="background-color: #4CAF50; width: 20px; height: 20px; border-radius: 50%; border: 2px solid white;"></div>',
            iconSize: [24, 24]
        })
    }).addTo(map);

    document.getElementById('start-coords').textContent = 
        `Lat: ${latlng.lat.toFixed(4)}, Lng: ${latlng.lng.toFixed(4)}`;

    checkCalculateButton();
}

// Establecer punto de destino
function setEndPoint(latlng) {
    if (endMarker) {
        map.removeLayer(endMarker);
    }

    endPoint = latlng;
    endMarker = L.marker(latlng, {
        icon: L.divIcon({
            className: 'end-marker',
            html: '<div style="background-color: #FF0000; width: 20px; height: 20px; border-radius: 50%; border: 2px solid white;"></div>',
            iconSize: [24, 24]
        })
    }).addTo(map);

    document.getElementById('end-coords').textContent = 
        `Lat: ${latlng.lat.toFixed(4)}, Lng: ${latlng.lng.toFixed(4)}`;

    checkCalculateButton();
}

// Habilitar botón de calcular cuando ambos puntos estén seleccionados
function checkCalculateButton() {
    document.getElementById('calculate-route').disabled = !(startPoint && endPoint);
}

// Cargar datos de seguridad
function loadSafetyData() {
    // Simulación de carga de datos - en producción usarías fetch a tu API
    console.log("Cargando datos de seguridad...");
    
    // Ejemplo con datos estáticos (en una app real estos vendrían de tu backend)
    var peligrosData = {
        "type": "FeatureCollection",
        "features": []
    };
    
    var seguridadData = {
        "type": "FeatureCollection",
        "features": []
    };
    
    var incidentesData = {
        "type": "FeatureCollection",
        "features": []
    };
    
    // Aquí procesarías los datos reales
    peligrosLayer = L.geoJSON(peligrosData, {
        style: {
            color: "#FF0000",
            weight: 2,
            opacity: 0.8,
            fillOpacity: 0.3
        },
        onEachFeature: function(feature, layer) {
            layer.bindPopup(`<b>Zona Peligrosa:</b> ${feature.properties?.nombre || 'Desconocido'}`);
        }
    }).addTo(map);

    zonasSegurasLayer = L.geoJSON(seguridadData, {
        style: {
            color: "#00FF00",
            weight: 2,
            opacity: 0.8,
            fillOpacity: 0.3
        },
        onEachFeature: function(feature, layer) {
            layer.bindPopup(`<b>Zona Segura:</b> ${feature.properties?.nombre || 'Desconocido'}`);
        }
    }).addTo(map);

    if (L.markerClusterGroup) {
        markersCluster = L.markerClusterGroup();
        
        incidentesLayer = L.geoJSON(incidentesData, {
            pointToLayer: function(feature, latlng) {
                return L.circleMarker(latlng, {
                    radius: 6,
                    fillColor: "#FFA500",
                    color: "#000",
                    weight: 1,
                    opacity: 1,
                    fillOpacity: 0.8
                });
            },
            onEachFeature: function(feature, layer) {
                layer.bindPopup(`<b>Incidente:</b> ${feature.properties?.tipo || 'Desconocido'}`);
            }
        });

        markersCluster.addLayer(incidentesLayer);
        map.addLayer(markersCluster);
    } else {
        console.warn('Leaflet.markercluster no está disponible');
    }
}

// Calcular ruta segura
function calculateSafeRoute() {
    if (!window.L.Routing) {
        alert('El plugin de enrutamiento no está disponible');
        return;
    }

    document.getElementById('loading-message').style.display = 'block';

    // Limpiar ruta anterior si existe
    if (routingControl) {
        map.removeControl(routingControl);
    }

    // Configurar la ruta
    routingControl = L.Routing.control({
        waypoints: [
            L.latLng(startPoint.lat, startPoint.lng),
            L.latLng(endPoint.lat, endPoint.lng)
        ],
        routeWhileDragging: false,
        showAlternatives: false,
        lineOptions: {
            styles: [{ color: '#4CAF50', opacity: 0.8, weight: 6 }]
        },
        createMarker: function() { return null; }
    }).addTo(map);

    routingControl.on('routesfound', function(e) {
        document.getElementById('loading-message').style.display = 'none';
        // Aquí podrías añadir lógica para analizar la ruta contra zonas peligrosas
        console.log('Ruta calculada:', e.routes[0]);
    });

    routingControl.on('routingerror', function(e) {
        document.getElementById('loading-message').style.display = 'none';
        alert('Error al calcular la ruta: ' + e.error.message);
    });
}

// Limpiar ruta y selección
function clearRoute() {
    if (routingControl) {
        map.removeControl(routingControl);
        routingControl = null;
    }

    if (startMarker) {
        map.removeLayer(startMarker);
        startMarker = null;
        startPoint = null;
        document.getElementById('start-coords').textContent = 'No seleccionado';
    }

    if (endMarker) {
        map.removeLayer(endMarker);
        endMarker = null;
        endPoint = null;
        document.getElementById('end-coords').textContent = 'No seleccionado';
    }

    document.getElementById('calculate-route').disabled = true;
}

// Inicializar el mapa cuando el DOM esté listo
document.addEventListener('DOMContentLoaded', function() {
    // Verificar dependencias antes de inicializar
    if (!window.L || !window.L.Routing) {
        console.error('Faltan dependencias necesarias');
        alert('Algunos componentes necesarios no se cargaron correctamente. Recarga la página.');
        return;
    }
    
    initMap();
});