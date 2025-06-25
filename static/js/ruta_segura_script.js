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

    startButton.addEventListener('click', function () {
        selectionMode = 'start';
        alert('Ahora haz clic en el mapa para seleccionar el punto de inicio');
    });

    endButton.addEventListener('click', function () {
        selectionMode = 'end';
        alert('Ahora haz clic en el mapa para seleccionar el punto de destino');
    });

    map.on('click', function (e) {
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
    fetch('http://localhost:5000/zonas_peligrosas')
        .then(response => response.json())
        .then(data => {
            peligrosLayer = L.geoJSON(data, {
                style: {
                    color: "#FF0000",
                    weight: 2,
                    opacity: 0.8,
                    fillOpacity: 0.3
                },
                onEachFeature: function (feature, layer) {
                    layer.bindPopup(`<b>Zona Peligrosa:</b> ${feature.properties.nombre}`);
                }
            }).addTo(map);
        });

    fetch('http://localhost:5000/zonas_seguridad')
        .then(response => response.json())
        .then(data => {
            zonasSegurasLayer = L.geoJSON(data, {
                style: {
                    color: "#00FF00",
                    weight: 2,
                    opacity: 0.8,
                    fillOpacity: 0.3
                },
                onEachFeature: function (feature, layer) {
                    layer.bindPopup(`<b>Zona Segura:</b> ${feature.properties.nombre}`);
                }
            }).addTo(map);
        });

    fetch('http://localhost:5000/incidentes')
        .then(response => response.json())
        .then(data => {
            markersCluster = L.markerClusterGroup();

            incidentesLayer = L.geoJSON(data, {
                pointToLayer: function (feature, latlng) {
                    return L.circleMarker(latlng, {
                        radius: 6,
                        fillColor: "#FFA500",
                        color: "#000",
                        weight: 1,
                        opacity: 1,
                        fillOpacity: 0.8
                    });
                },
                onEachFeature: function (feature, layer) {
                    layer.bindPopup(`<b>Incidente:</b> ${feature.properties.tipo}`);
                }
            });

            markersCluster.addLayer(incidentesLayer);
            map.addLayer(markersCluster);
        });
}

// Calcular ruta segura
function calculateSafeRoute() {
    document.getElementById('loading-message').style.display = 'block';

    // Limpiar ruta anterior si existe
    if (routingControl) {
        map.removeControl(routingControl);
    }

    // Simulación de cálculo de ruta segura
    // En una implementación real, aquí llamarías a un servicio que considere las zonas peligrosas
    setTimeout(function () {
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
            createMarker: function () { return null; } // No mostrar marcadores adicionales
        }).addTo(map);

        document.getElementById('loading-message').style.display = 'none';

        // Simular desviación de zonas peligrosas (en realidad necesitarías un algoritmo más sofisticado)
        simulateRouteSafetyAnalysis();
    }, 1500);
}

// Simular análisis de seguridad de la ruta (ejemplo)
function simulateRouteSafetyAnalysis() {
    // En una implementación real, esto analizaría la ruta contra las zonas peligrosas
    alert("Ruta calculada intentando evitar zonas peligrosas. En una implementación completa, esto usaría un algoritmo de planificación de ruta que penalice las zonas peligrosas.");
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
document.addEventListener('DOMContentLoaded', initMap);